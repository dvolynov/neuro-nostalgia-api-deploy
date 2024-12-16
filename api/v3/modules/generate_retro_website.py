import openai, requests, bs4, io, json


class NamedBytesIO(io.BytesIO):
    def __init__(self, content=b'', name=None):
        super().__init__(content)
        self.name = name


def generate_retro_website(url, api_key, assistant_id):
    response = requests.get(url)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    html = str(soup)

    path = "api/v3/cache/file.txt"

    with open(path, 'w') as file:
        file.write(html)

    client = openai.OpenAI(api_key=api_key)

    file = client.files.create(file=open(path, "rb"), purpose='assistants')
    assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)

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

        html_file_id = messages.data[0].attachments[0].file_id
        content = client.files.with_raw_response.retrieve_content(html_file_id).content.decode('utf-8')

        client.files.delete(file.id)
        client.files.delete(html_file_id)

        return content
    else:
        raise RuntimeError("Schema was not generated")
