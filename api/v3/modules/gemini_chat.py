import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import io


def generate(content: str, api_key: str, model_name: str, max_output_tokens: int, temperature: float, system_instruction: str):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=genai.GenerationConfig(
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            response_mime_type="text/plain",
        ),
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        },
        system_instruction=system_instruction,

    )
    file_buffer = io.BytesIO(content.encode('utf-8'))
    file_buffer.name = "index.html"
    file = genai.upload_file(file_buffer, mime_type="text/plain")
    response = model.generate_content(["File:", file])
    text = response.text.replace("  ", " ")
    return text