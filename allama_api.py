import ollama

class OllamaBrain:
    def __init__(self, model_name="qwen2.5:3b"):
        self.model = model_name
        self.options = {
            "temperature": 1.1,
            "num_thread": 4,
            "num_predict": 80,
            "top_k": 20,
            "top_p": 0.9,
            "repeat_penalty": 1.2,
            "stop": ["User:", "\nUser", "\n\n", "Human:"]
        }

    def comunicar_sincrono(self, system_prompt, user_message):
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            options=self.options
        )
        return response['message']['content']

    async def comunicar(self, system_prompt, user_message):
        import asyncio
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: ollama.chat(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    options=self.options
                )
            )
            return response['message']['content']
        except Exception as e:
            return f"n consigo pensar em nada... (._.) "