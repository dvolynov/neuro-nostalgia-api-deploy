import requests, bs4, json

from .gemini_chat import generate


def create_schema(url, api_key, model_name, max_output_tokens, temperature):
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    html = str(soup)

    schema = generate(
        content = html,
        api_key=api_key,
        model_name=model_name,
        max_output_tokens=max_output_tokens,
        temperature=temperature,
        system_instruction = open("api/v1/instructions/schema.txt").read().replace("<URL>", url)
    )
    return schema