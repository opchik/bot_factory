import os
from openai import ChatCompletion


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ChatCompletion.api_key = OPENAI_API_KEY


async def generate_post(theme):
    prompt = f"""
    Напиши пост на тему "{theme}" в следующем формате:
    1. Заголовок: краткий и привлекающий внимание.
    2. Основной текст: 2-3 абзаца, информативно и интересно.
    3. Заключение: призыв к действию или интересный вывод.
    """
    response = ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']
