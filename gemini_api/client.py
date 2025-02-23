import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api)

def car_gemini_ai(model, brand, year):
    message = ''' Elabore um resumo sobre o carro {} da marca {} do ano {} com 200 caracteres. Forneça mais detalhes técnicos. Aborde uma linguagem mais simples.'''
    message = message.format(model, brand, year)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content( message, generation_config = genai.GenerationConfig( max_output_tokens=300, ) )
    return response.text
