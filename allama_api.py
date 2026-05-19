import json
import httpx
import ollama

class OllamaBrain:
    def __init__(self, model_name="llama3.1:8B"):
        self.url = "http://localhost:11434/api/generate"
        self.model = model_name

    def comunicar_sincrono(self, prompt):
        response = ollama.generate(model=self.model, prompt=prompt)
        return response['response']

    async def comunicar(self, prompt_completo):
        payload = {
            "model": self.model,
            "prompt": prompt_completo,
            "stream": False, 
            "options": {
                "temperature": 1.1,
                "num_thread": 8,
                "num_predict": 50,
                "top_k": 20,
                "top_p": 0.9,
                "repeat_penalty": 1.2,
                "stop": ["oi", "Oi", "Olá", "Matyan", "\n", "User:"]
            }
        }

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(self.url, json=payload)
            if response.status_code == 200:
                dados = response.json()
                return dados.get('response', "n consigo pensar em nada... (._.) ")
            else:
                return f"erro no motor: status {response.status_code}"
                
        except Exception as e:
            return f"Erro de conexão: {str(e)}"