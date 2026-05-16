from groq import Groq
import os

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def get_groq_response(messages:list, model : str="llama-3.3-70b-versatile")->str:

    completion = client.chat.completions.create(
        messages=messages,
        model= model
    )

    return completion.choices[0].message.content


    

