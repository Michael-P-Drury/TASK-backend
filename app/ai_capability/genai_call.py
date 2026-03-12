'''
holds functionality for genai calling
'''

from ollama import AsyncClient
import time
from cerebras.cloud.sdk import AsyncCerebras
import os
from dotenv import load_dotenv

load_dotenv()


async def invoke_genai(prompt: str, provider: str, model_id: str, temperature: float):
    '''
    inputs:
    prompt: str - sting for prompt to send to genai
    provider: str - provider for LLM
    model_id: str - model that you are trying to contact
    temperature: float - temperature for model (between 0 and 1)

    for invoking genai models
    '''

    run_count = 0

    rerun = True

    while run_count <= 100 and rerun:

        try:
        
            if provider == 'ollama':
                message = {'role': 'user', 'content': prompt}
                
                start = time.time()
                response = await AsyncClient().chat(
                    model= model_id,
                    messages=[message],
                    options={
                        'temperature': temperature
                    }
                )
                end = time.time()
                time_taken = end - start

                response = response['message']['content']
                
            elif provider == 'cerebras':
                start = time.time()
                
                client = AsyncCerebras(api_key=os.getenv('CEREBRAS_API_KEY'))

                response = await client.chat.completions.create(
                    model=model_id,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=temperature
                )

                response = response.choices[0].message.content

                end = time.time()
                time_taken = end - start

            else:
                return {'status': 200, 'response': None, 'time_taken': None}

            return {'status': 200, 'response': response, 'time_taken': time_taken}

        except Exception as e:
            print(f"An error occurred: {e}")

    return {'status': 200, 'response': None, 'time_taken': None}
