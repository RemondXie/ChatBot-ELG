import openai

from textbase.message import Message

class OpenAI:
    api_key = None

    @classmethod
    def generate(
        cls,
        system_prompt: str,
        message_history: list[Message],
        model="gpt-4o-mini",
        max_tokens=3000,
        temperature=0.7,
    ):
        assert cls.api_key is not None, "OpenAI API key is not set"
        client = openai.Client(api_key=cls.api_key)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                *map(dict, message_history),
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content
