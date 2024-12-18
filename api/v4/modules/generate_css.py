import requests, bs4

from .gemini_chat import generate


def generate_css(url, api_key, model_name, max_output_tokens, temperature):
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    html = str(soup)

    css = generate(
        content            = html,
        api_key            = api_key,
        model_name         = model_name,
        max_output_tokens  = max_output_tokens,
        temperature        = temperature,
        system_instruction = open("api/v2/instructions/css.txt").read(),
    )

    css = css.replace(";", " !important;")
    css = css.replace("```css", "")
    css = css.replace("```", "")
    css = css.replace("<style>", "")
    css = css.replace("</style>", "")
    css = "<style>*{border-radius: 0 !important;}" + f"\n{css}\n</style>"

    return css, html
