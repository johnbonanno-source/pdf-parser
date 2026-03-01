from google import genai
from io import BytesIO
from prompts import baseprompt
from typing import BinaryIO
from protocol_repository import save_protocol_parse


_client = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client()
    return _client


def parse_protocol(uploaded_file: BinaryIO, filename:str, file_mime_type:str) -> str:
    client = get_client()
    file_bytes = uploaded_file.read()

    sample_file = client.files.upload(
        file=BytesIO(file_bytes),
        config={"mime_type": file_mime_type, "display_name": filename}
    )
    prompt = baseprompt
    response = client.models.generate_content(
        model="gemini-3-flash-preview", # you can also try gemini-3-pro-preview , or gemini-3-pro-image-preview. https://ai.google.dev/gemini-api/docs/pricing
        contents=[sample_file, prompt])

    save_protocol_parse(
        file_bytes=file_bytes,
        filename=filename,
        file_mime_type=file_mime_type,
        model_name="gemini-3-flash-preview",
        prompt_text=prompt,
        protocol_markdown=response.text,
        usage_metadata='hi'#response.usage_metadata.to_dict() if response.usage_metadata else None
    )
    return response.text
