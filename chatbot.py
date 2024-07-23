from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import nest_asyncio
import fitz  # PyMuPDF library
import openai  # Ensure you have installed OpenAI Python SDK: pip install openai

# Initialize FastAPI app
app = FastAPI()

# Initialize OpenAI API (replace with your API key)
openai.api_key = "############################################"

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    try:
        # Open the PDF file using PyMuPDF
        pdf_document = fitz.open(stream=pdf_file.file.read(), filetype="pdf")
        # Iterate through each page and extract text
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pdf_text += page.get_text()
        return pdf_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text from PDF: {str(e)}")

# Endpoint to upload PDF and get AI response
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Check if file is PDF
    if file.filename.endswith('.pdf'):
        # Process PDF (extract text using the function)
        pdf_text = extract_text_from_pdf(file)
        
        # Call OpenAI API to generate response based on user query
        user_query = "What can you tell me about this PDF?"
        ai_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_query,
            max_tokens=150
        )
        
        return {
            "query": user_query,
            "pdf_text": pdf_text,
            "ai_response": ai_response['choices'][0]['text'].strip()
        }
    else:
        raise HTTPException(status_code=400, detail="File must be a PDF")

nest_asyncio.apply()

# Function to start ngrok tunnel
def start_ngrok():
    from pyngrok import ngrok
    public_url = ngrok.connect(port=8000)
    print('Public URL:', public_url)

# Start FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=9000)

# Start ngrok tunneling
start_ngrok()
