# 开发时间：2024/7/5 20:13
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="sk-lprUsAm4UM4pmCQpFaRtFy9T6IMTNcqqN4gqX41YoJccCbpO",
    base_url="https://api.chatanywhere.tech/v1"
)


def decoder_for_gpt(args,input:list):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=input
    )
    return completion.choices[0].message.content


def get_answer(args,inputs:list):
    get_result = False
    pred = ''
    while not get_result:
        pred = decoder_for_gpt(args,inputs)
        get_result = True

    return get_result,pred