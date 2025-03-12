import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()
gemini_api = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api)

def car_gemini_ai(functionality, description):
    message = ''' Elabore um resumo sobre a funcionalidade {}, que tem o seguinte conteúdo: {}. Forneça uma explicação simples e descritiva ao usuário de como usá-la.'''
    message = message.format(functionality, description)
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content( message, generation_config = genai.GenerationConfig( max_output_tokens=300, ) )
    return response.text
