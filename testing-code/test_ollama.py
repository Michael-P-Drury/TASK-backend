import asyncio
from ollama import AsyncClient
import time

async def say_hello(prompt, model_id):
    message = {'role': 'user', 'content': prompt}
    
    try:
        start = time.time()
        response = await AsyncClient().chat(
            model= model_id,
            messages=[message],
            options={
                'temperature': 0.7
            }
        )
        end = time.time()

        print(f'response time: {end - start}')
        
        print("Model Response:")
        print(response['message']['content'])
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    prompt = 'give me 200 words about your penguins'
    model_id = 'llama3.2:1b'

    asyncio.run(say_hello(prompt, model_id))

