from .gemini_chat import generate


def generate_webpage(schema, api_key, model_name, max_output_tokens, temperature):
    html = generate(
        content            = schema,
        api_key            = api_key,
        model_name         = model_name,
        max_output_tokens  = max_output_tokens,
        temperature        = temperature,
        system_instruction = open("api/v1/instructions/html.txt").read(),
    )
    return html
