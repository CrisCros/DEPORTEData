import os
import sys
import glob
import json
import chromadb
from llm import GeneradorLLM
from prompt import RAG_TEMPLATE

def iniciar_asistente():
    # 1. Configurar ruta a los archivos JSON
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DIR_JSON = os.path.join(BASE_DIR, "data_json")
    
    print(f"📦 Preparando datos desde archivos JSON en: {DIR_JSON}")
    archivos_json = glob.glob(os.path.join(DIR_JSON, "*.json"))
    
    if not archivos_json:
        print(f"❌ Error: No se encontraron archivos JSON en {DIR_JSON}")
        sys.exit(1)

    # 2. Recrear la base de datos Vectorial EN MEMORIA
    # En lugar de usar la DB persistente antigua, cargamos los JSON en una 
    # base temporal que existirá solo mientras la terminal esté abierta.
    print("⏳ Cargando JSONs en el buscador vectorial en memoria...")
    client = chromadb.Client()  # Cliente efímero
    coleccion = client.create_collection(name="datos_json_directo")
    
    total_cargados = 0
    for ruta_archivo in archivos_json:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            chunks = datos.get("chunks", [])
            
            # Preparamos las listas requeridas por Chroma
            documentos = []
            ids = []
            metadatos = []
            
            for chunk in chunks:
                documentos.append(chunk["texto"])
                ids.append(chunk["chunk_id"])
                metadatos.append({"fuente": chunk["fuente"]})
                
            # Guardamos los fragmentos de este archivo en la memoria de la colección
            if documentos:
                coleccion.add(
                    documents=documentos,
                    ids=ids,
                    metadatas=metadatos
                )
                total_cargados += len(documentos)
                
    print(f"✅ Se han indexado {total_cargados} fragmentos de los JSONs para consulta rápida.")

    # 3. Inicializar Ollama
    print("🧠 Despertando a Ollama...")
    llm = GeneradorLLM() 
    
    print("\n" + "="*50)
    print("🏆 RAG DEPORTIVO ACTIVO (Fuente: /data_json/*.json)")
    print("="*50)

    # 4. Bucle Interactivo
    while True:
        try:
            pregunta = input("\n👤 Tu pregunta: ")
        except KeyboardInterrupt:
            break
            
        if pregunta.lower() in ['salir', 'exit', 'quit']:
            break
            
        if not pregunta.strip():
            continue

        # 5. RETRIEVAL: Buscar entre todo el texto indexado desde los JSON
        print("🔍 Consultando archivos JSON...")
        resultados = coleccion.query(query_texts=[pregunta], n_results=5)
        
        # Filtramos por si acaso no viniera ningún documento
        if resultados['documents'] and len(resultados['documents'][0]) > 0:
            contexto_unido = "\n--- Fragmento ---\n".join(resultados['documents'][0])
        else:
            contexto_unido = "No se ha encontrado contexto relevante de los archivos JSON."
            
        # --- DEBUG ---
        print("\n[INFO DEBUG] Textos que hemos pescado de los JSONs y que leerá Ollama:")
        print(contexto_unido)
        print("-" * 60)
        # -------------

        # 6. AUGMENTATION: Empaquetar
        prompt_final = RAG_TEMPLATE.format(
            contexto=contexto_unido,
            pregunta=pregunta
        )
        
        # 7. GENERATION
        print("\n🤖 Ollama está pensando...")
        try:
            respuesta = llm.generar(prompt_final)
            print(f"\n✨ RESPUESTA:\n{respuesta}")
        except Exception as e:
            print(f"\n⚠️ Hubo un error de Ollama al generar la respuesta: {e}")

if __name__ == "__main__":
    iniciar_asistente()