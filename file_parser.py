import io
import json
import pandas as pd
from PyPDF2 import PdfReader

def parse_file(uploaded_file):
    """Parses text out of uploaded txt, csv, json, or pdf files."""
    filename = uploaded_file.name.lower()
    
    try:
        if filename.endswith('.txt'):
            return uploaded_file.getvalue().decode('utf-8')
            
        elif filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
            # Combine all string columns into a single text body
            text_chunks = []
            for col in df.columns:
                text_chunks.extend(df[col].dropna().astype(str).tolist())
            return " ".join(text_chunks)
            
        elif filename.endswith('.json'):
            data = json.load(uploaded_file)
            # Flatten json values if it's a dict or list
            if isinstance(data, dict):
                return " ".join(str(v) for v in data.values() if isinstance(v, str))
            elif isinstance(data, list):
                return " ".join(str(v) for v in data if isinstance(v, str))
            return str(data)
            
        elif filename.endswith('.pdf'):
            reader = PdfReader(uploaded_file)
            text_chunks = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_chunks.append(text)
            return "\n".join(text_chunks)
            
        else:
            return "Unsupported file type."
    except Exception as e:
        return f"Error parsing file: {str(e)}"
