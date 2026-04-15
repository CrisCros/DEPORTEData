# llm.py
import ollama

class GeneradorLLM:
    def __init__(self, model_id="qwen2.5:0.5b"):
        self.model_id = model_id
        print(f"✅ Conectado a Ollama listo para usar {self.model_id}.")

    def generar(self, prompt_texto):
        """Envía el prompt a Ollama y devuelve la respuesta."""
        
        respuesta = ollama.chat(model=self.model_id, messages=[
            {
                'role': 'user',
                'content': prompt_texto,
            },
        ])
        
        return respuesta['message']['content']

# Pequeña prueba si ejecutas este archivo directamente
if __name__ == "__main__":
    mi_llm = GeneradorLLM()
    print("🤖 Generando respuesta...")
    print(mi_llm.generar("Hola, dime algo muy breve."))