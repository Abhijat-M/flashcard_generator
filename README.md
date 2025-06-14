# AI-Powered Flashcard Generator

This project provides a Flask-based web service that uses the `microsoft/phi-3-mini-4k-instruct` language model via the Hugging Face `transformers` library to automatically generate flashcards (Question/Answer pairs) from uploaded **PDF documents**.

## Features

* Accepts PDF file uploads via a POST request.
* Uses Phi-3 Mini Instruct model for generating concise and relevant flashcards from extracted text.
* Outputs flashcards in a structured JSON format.
* Includes basic error handling and logging.
* Provides a health check endpoint.

## Prerequisites

* Python 3.8+
* `pip` (Python package installer)
* Access to the internet to download the Hugging Face model.
* (Recommended) A CUDA-enabled GPU with appropriate drivers installed for faster inference. PyTorch needs to be installed with CUDA support if using a GPU. Check [PyTorch installation instructions](https://pytorch.org/get-started/locally/).

## Setup

1. **Clone the repository (if applicable) or place the files in a directory:**

    ```bash
    git clone <your-repo-url>
    cd ai-flashcard-generator
    ```

    Or simply create a directory and place `app.py`, `flashcard_gen.py`, `requirements.txt`, and `.gitignore` inside it.

2. **Create and activate a virtual environment (Recommended):**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies:**
    Make sure your `requirements.txt` file includes `pypdf`.

    ```bash
    pip install -r requirements.txt
    ```

    *Note: This will download PyTorch, Transformers, Flask, Accelerate, **pypdf**, and their dependencies. It might also download the Phi-3 model files (~gigabytes) on the first run.*

## Running the Application

1. **Start the Flask server:**
    The application uses `waitress` as a production-ready WSGI server.

    ```bash
    python app.py
    ```

    The server will start, typically on `http://0.0.0.0:5001`. The first time you run it, downloading and initializing the model might take several minutes depending on your internet speed and hardware.

## API Usage

### Generate Flashcards from PDF

* **Endpoint:** `/generate`
* **Method:** `POST`
* **Body:** Form data containing the PDF file. The key for the file must be `file`.
* **Success Response (200 OK):**

    ```json
    {
      "flashcards": [
        {
          "question": "...",
          "answer": "..."
        },
        {
          "question": "...",
          "answer": "..."
        }
      ]
    }
    ```

* **Error Responses:**
  * `400 Bad Request`: If no file is uploaded, the file key is incorrect, the file is not a PDF, or text extraction fails.
  * `500 Internal Server Error`: If the model fails to initialize or an unexpected error occurs during processing or generation.

**Example using `curl`:**

Replace `path/to/your/document.pdf` with the actual path to your PDF file.

```bash
curl -X POST http://localhost:5001/generate \
     -F "file=@path/to/your/document.pdf"
