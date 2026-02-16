from ollama import AsyncClient
import time

async def invoke_genai(prompt, provider, model_id, temperature):
    
    if provider == 'ollama':
        message = {'role': 'user', 'content': prompt}
        
        try:
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

            return {'status': 200, 'response': response, 'time_taken': time_taken}
            
        except Exception as e:
            print(f"An error occurred: {e}")

            return {'status': 200, 'response': None, 'time_taken': None}
