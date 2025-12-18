import os
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import google.generativeai as genai
from openai import OpenAI
import uvicorn

app = FastAPI(title="RCA Transformer")

# Setup templates
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        import traceback
        return HTMLResponse(content=f"<h1>Error</h1><pre>{traceback.format_exc()}</pre>", status_code=500)

@app.post("/generate", response_class=HTMLResponse)
async def generate_rca(
    request: Request,
    title: str = Form(...),
    date: str = Form(...),
    impact: str = Form(...),
    root_cause: str = Form(...),
    resolution: str = Form(...),
    reference_rca: Optional[str] = Form(None),
    provider: str = Form("gemini"),
    model_name: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None)
):
    
    style_instruction = ""
    if reference_rca and len(reference_rca.strip()) > 0:
        style_instruction = f"""
        ### STYLE GUIDE and TONE INSTRUCTIONS (CRITICAL)
        The user has provided a "Reference RCA" below. You MUST mimic the tone, vocabulary, sentence structure, and formatting level of this reference exactly.
        If the reference is apologetic, be apologetic. If it is direct and clinical, be direct and clinical. 
        
        Reference Example:
        \"\"\"
        {reference_rca}
        \"\"\"
        """

    prompt = f"""
    You are a Senior Customer Reliability Engineer at a major cloud provider. 
    Your job is to write a customer-facing Root Cause Analysis (RCA) document based on raw technical details input by an engineer.
    
    {style_instruction}
    
    The output MUST strictly follow this structure:
    # Incident: {title}
    **Date:** {date}

    ## 1. Summary of Impact
    (Rewrite the input impact to be customer-centric, focusing on user experience, downtime, and business impact. Avoid purely internal metrics unless relevant to customer experience.)

    ## 2. Root Cause
    (Explain the technical root cause provided in simple, transparent terms that a non-technical executive can understand. Focus on "what happened" and "why" without being overly defensive.)

    ## 3. Resolution
    (Describe how the immediate issue was fixed to restore service.)

    ## 4. Remediations
    (List the steps being taken to prevent this specific issue from recurring, based on the input.)

    ---
    
    **Input Data from Engineering:**
    - Impact: {impact}
    - Root Cause: {root_cause}
    - Resolution: {resolution}
    - Remediations: {remediations}

    Generate the customer-facing RCA in Markdown format.
    """

    generated_text = ""

    try:
        if provider == "gemini":
            # Configure Gemini
            key_to_use = api_key if api_key else os.environ.get("GEMINI_API_KEY")
            if not key_to_use:
                raise ValueError("No Gemini API Key provided. Please provide one in the form or set GEMINI_API_KEY environment variable.")
            
            genai.configure(api_key=key_to_use)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            generated_text = response.text

        elif provider == "github":
             # Configure GitHub Models (via OpenAI SDK)
            key_to_use = api_key if api_key else os.environ.get("GITHUB_TOKEN")
            if not key_to_use:
                raise ValueError("No GitHub Token provided. Please provide one in the form or set GITHUB_TOKEN environment variable.")
            
            # Initialize OpenAI client for GitHub Models
            client = OpenAI(
                base_url="https://models.inference.ai.azure.com",
                api_key=key_to_use,
            )
            
            # Use selected model or default to gpt-4o
            target_model = model_name if model_name else "gpt-4o"

            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=target_model,
                temperature=1.0,
                top_p=1.0,
                max_tokens=4000
            )
            generated_text = response.choices[0].message.content

    except Exception as e:
        generated_text = f"Error generating content: {str(e)}"

    return templates.TemplateResponse("result.html", {
        "request": request, 
        "rca_content": generated_text
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
