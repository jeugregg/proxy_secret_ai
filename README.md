# proxy_secret_ai

Create a proxy between secret AI and react web app# proxy_secret_ai: API Proxy for Secret AI and ReactJS Web Application

This project serves as an API proxy, acting as an intermediary between the Secret AI LLM (Large Language Model) and a ReactJS web application. It utilizes the Secret AI Python SDK to interact with the LLM and exposes RESTful API endpoints that the ReactJS application can consume. This proxy bridges the communication gap before a dedicated JavaScript SDK for Secret AI is available.

## Project Overview

The primary goal of `proxy_secret_ai` is to enable a ReactJS frontend to leverage the power of Secret AI's LLM without direct interaction. This is achieved through a Flask-based Python API that exposes two key functionalities:

1.  **Invoice Information Extraction (`/api/invoice`)**: This endpoint accepts raw invoice text and uses the Secret AI LLM to extract structured data, including invoice number, date, client name, description, total amount, tax amount, and currency.
2.  **Invoice Credibility Assessment (`/api/credibility`)**: This endpoint evaluates the credibility of an invoice against provided accounting data. It receives both the invoice text and an accounting row and utilizes the LLM to assess their consistency, providing a credibility score between 0 and 100.

## Technology Stack

*   **Backend:**
    *   Python 3
    *   Flask (web framework)
    *   Flask-CORS (for handling Cross-Origin Resource Sharing)
    *   Secret AI Python SDK (`secret_ai_sdk`)
    *   LangChain Core (`langchain_core`)
    * Pydantic
*   **LLM Interaction:** Secret AI's Large Language Model
*   **Frontend (not included in this project):** ReactJS (assumed to be interacting with this proxy)

## Installation and Setup

Follow these steps to get the proxy up and running:

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual repository URL
    cd proxy_secret_ai
    ```

2.  **Install Dependencies:**
    Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```
    Activate the environment :
    * on macOS or Linux:
    ```bash
    source venv/bin/activate
    ```
    * on Windows:
    ```bash
    venv\Scripts\activate
    ```
    Install the necessary Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Environment Variables:**

    *   Create a `.env` file in the root directory of the project.
    *   Add the following environment variable, replacing `YOUR-API-KEY` with your actual Secret AI API key:
        ```
        SECRET_AI_API_KEY=YOUR-API-KEY
        ```

4.  **Run the Flask Application:**

    ```bash
    python app.py
    ```

    This command starts the Flask development server. By default, it runs on `http://127.0.0.1:5000/`.

## API Endpoints

### `/api/invoice`

*   **Method:** `POST`
*   **Request Body (JSON):**
    ```json
    {
        "data": "Invoice text content here..."
    }
    ```
*   **Response Body (JSON):**
    ```json
    {
        "invoice_number": "INV-2023-123",
        "date": "2023-10-27",
        "client_name": "Acme Corp",
        "description": "Software development",
        "total_amount": "1500.00",
        "tax_amount": "300.00",
        "currency": "USD"
    }
    ```

### `/api/credibility`

*   **Method:** `POST`
*   **Request Body (JSON):**
    ```json
    {
        "accounting_row": {
            "invoice_number": "INV-2023-123",
            "date": "2023-10-27",
            "amount": "1500.00",
            "currency": "USD",
            "vendor" : "Acme Corp"
        },
        "invoice": "Invoice text content here..."
    }
    ```
*   **Response Body (JSON):**
    ```json
    {
        "credibility": 95
    }
    ```

## Usage

1.  **Frontend Interaction:** The ReactJS application should send `POST` requests to these endpoints with the appropriate JSON payloads.
2. **CORS enabled** : you can use the API without having error of CORS when the React app is running on a different port than the proxy one.

## Troubleshooting

*   **Environment Variables:** Ensure that the `SECRET_AI_API_KEY` environment variable is correctly set in your `.env` file.
*   **Dependencies:** If you encounter import errors, double-check that all the required packages are installed in your virtual environment (`requirements.txt`).
*   **API Key:** Verify that your Secret AI API key is valid and active.
* **virtual environment** : if you have problems runing the app ensure you activate the virtual environment before runing `python app.py`

## Future Improvements

*   **JavaScript SDK:** Once a dedicated JavaScript SDK for Secret AI is available, the need for this proxy may be reduced.
*   **Enhanced Error Handling:** Implement more robust error handling and logging.
*   **Authentication/Authorization:** Add authentication and authorization for enhanced security.
*   **Caching:** Implement caching to reduce the number of LLM calls and improve performance.

## Contact

For questions or issues, please open an issue in the project's repository.
