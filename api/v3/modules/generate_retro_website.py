import openai, requests, bs4, io, re


class NamedBytesIO(io.BytesIO):
    def __init__(self, content=b'', name=None):
        super().__init__(content)
        self.name = name


def generate_retro_website(url, api_key, assistant_id, topP, temperature):
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    html = str(soup)

    path = "api/cache/file.txt"

    with open(path, 'w') as file:
        file.write(html)

    client = openai.OpenAI(api_key=api_key)

    file = client.files.create(file=open(path, "rb"), purpose='assistants')
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        top_p=topP,
        temperature=temperature
    )

    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": open("api/v3/instructions/html.txt").read(),
                "attachments": [
                    {
                        "file_id": file.id,
                        "tools": [{"type": "code_interpreter"}]
                    }
                ]
            }
        ]
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread.id)

        print(messages)

        if len(messages.data[0].attachments):
            html_file_id = messages.data[0].attachments[0].file_id
            css = client.files.with_raw_response.retrieve_content(html_file_id).content.decode('utf-8')
            try:
                client.files.delete(file.id)
                client.files.delete(html_file_id)
            except:
                pass
        else:
            css = messages.data[0].content[0].text.value
            css = css[css.find("```css") + 6:css.rfind("```")]

        css = css.replace(";", " !important;")
        css = css.replace("```css", "")
        css = css.replace("```", "")
        css = css.replace("<style>", "")
        css = css.replace("</style>", "")
        css = "<style>*{border-radius: 0 !important;}" + f"\n{css}\n</style>"

        body_opening_tag_pattern = r"(<body[^>]*>)"

        html = re.sub(
            body_opening_tag_pattern,
            r"\1\n" + css,
            html,
            count=1
        )

        return html
    else:
        print(run)
        print(run.status)
        raise RuntimeError("Schema was not generated")
