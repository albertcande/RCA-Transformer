# RCA Transformer

RCA Transformer is a tool designed to help Customer Reliability Engineers and DevOps professionals generate high-quality, customer-facing Root Cause Analysis (RCA) documents from raw technical inputs.

Leveraging the power of advanced AI models (Google Gemini, GPT-4o, Llama 3, etc.), this application transforms technical jargon into clear, professional, and empathetic communication suitable for stakeholders and customers.

## Features

-   **Multi-Model Support**: Choose between Google Gemini or GitHub Models (GPT-4o, Mistral, Llama 3, Phi-3).
-   **Style Matching**: Upload a reference RCA to ensure the generated output mimics your organization's specific tone, vocabulary, and formatting.
-   **Automated Structuring**: Automatically formats raw data into standard sections:
    -   Summary of Impact
    -   Root Cause
    -   Resolution
    -   Remediations
-   **Modern UI**: Features a sleek, dark-mode interface for a comfortable user experience.

## Prerequisites

-   Python 3.8+
-   API Key for **Google Gemini** (if using Gemini models)
-   API Key for **GitHub Models** (if using GitHub models)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/albertcande/rca-transformer.git
    cd rca-transformer
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup:**
    You can set your API keys as environment variables or enter them directly in the UI.
    
    **Windows (PowerShell):**
    ```powershell
    $env:GEMINI_API_KEY="your_gemini_key"
    $env:GITHUB_TOKEN="your_github_token"
    ```

    **Linux/macOS:**
    ```bash
    export GEMINI_API_KEY="your_gemini_key"
    export GITHUB_TOKEN="your_github_token"
    ```

## Usage

1.  **Start the application:**
    ```bash
    python main.py
    ```

2.  **Access the interface:**
    Open your browser and navigate to `http://127.0.0.1:8000`.

3.  **Generate an RCA:**
    -   Enter the Incident Title and Date.
    -   Provide raw technical details for Impact, Root Cause, Resolution, and Remediations.
    -   (Optional) Paste a previous RCA in the "Reference / Example RCA" field to match its style.
    -   Select your preferred AI provider and model.
    -   Click **Generate Draft**.

## Technologies Built With

-   **Frontend**: HTML5, CSS3, Jinja2
-   **Backend**: FastAPI, Python
-   **AI Integration**: `google-generativeai`, `openai` SDK (for GitHub Models)

## License

[MIT License](LICENSE)


