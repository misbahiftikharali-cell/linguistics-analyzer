import os
import json
import google.generativeai as genai

# Try to load API key from environment variable, then Streamlit secrets
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    try:
        import streamlit as st
        if hasattr(st, "secrets") and "GEMINI_API_KEY" in st.secrets:
            GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        pass

# Fallback: manually parse .streamlit/secrets.toml if running raw Python scripts locally
if not GEMINI_API_KEY:
    try:
        secrets_path = os.path.join(".streamlit", "secrets.toml")
        if os.path.exists(secrets_path):
            with open(secrets_path, "r", encoding="utf-8") as f:
                for line in f:
                    if "GEMINI_API_KEY" in line and "=" in line:
                        parts = line.split("=", 1)
                        val = parts[1].strip().strip('"').strip("'")
                        if val:
                            GEMINI_API_KEY = val
                            break
    except Exception:
        pass

def call_openai_json(prompt: str) -> dict:
    """
    Function name kept for compatibility with existing agents.
    Now routes calls to Google Gemini Flash Lite for optimal quota availability.
    """

    if not GEMINI_API_KEY:
        print("Error: No Gemini API key provided.")
        return {"error": "Missing API Key"}
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Using gemini-flash-lite-latest for maximum quota availability
        model = genai.GenerativeModel(
            model_name='gemini-flash-lite-latest',
            system_instruction="You are a specialized forensic linguistic AI assistant that always outputs strictly valid JSON."
        )


        
        # Generate content with JSON constraint and high token limit
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                temperature=0.1,
                max_output_tokens=8192
            )
        )
        
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        
        # Try to find the first '{' or '[' and the last '}' or ']'
        start_idx = min(text.find('{') if text.find('{') != -1 else len(text), text.find('[') if text.find('[') != -1 else len(text))
        end_idx = max(text.rfind('}') if text.rfind('}') != -1 else -1, text.rfind(']') if text.rfind(']') != -1 else -1)
        
        try:
            decoder = json.JSONDecoder()
            # Find the first potential JSON start
            start_idx = min(text.find('{') if text.find('{') != -1 else len(text), 
                           text.find('[') if text.find('[') != -1 else len(text))
            if start_idx < len(text):
                obj, index = decoder.raw_decode(text[start_idx:])
                return obj
            return json.loads(text)
        except Exception as json_err:
            raise json_err
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return {"error": str(e)}
