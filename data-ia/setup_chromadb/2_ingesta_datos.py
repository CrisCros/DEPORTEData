import os
import sys
import glob
import json
import chromadb

def ingestar_datos_desde_json():
    # 1. Definir rutas basándonos en la raíz del proyecto
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DIR_JSON = os.path.join(BASE_DIR, "data_json")
    DB_PATH = os.path.join(BASE_DIR, "mi_bd_chroma")
    
    print(f"📦 Buscando archivos JSON a ingestar en: {DIR_JSON}")
    archivos_json = glob.glob(os.path.join(DIR_JSON, "*.json"))
    
    if not archivos_json:
        print(f"❌ Error: No se encontraron archivos JSON en {DIR_JSON}. Ejecuta primero tu script de extracción.")
        sys.exit(1)

    # 2. Conectamos al cliente persistente de ChromaDB
    print(f"🔗 Conectando a local ChromaDB en: {DB_PATH}")
    client = chromadb.PersistentClient(path=DB_PATH)
    nombre_coleccion = "datos_deportivos"
    
    # Limpiar tabla anterior si existe, para que las inserciones sean siempre 'frescas' sin duplicados
    try:
        client.delete_collection(name=nombre_coleccion)
        print("🧹 Colección antigua borrada para una ingesta limpia.")
    except Exception:
        pass 
        
    coleccion = client.create_collection(name=nombre_coleccion)

    documentos = []
    metadatos = []
    ids = []
    
    print("⏳ Leyendo JSON y preparando vectores...")
    
    # 3. Leer cada archivo JSON y recoger todos los fragmentos
    for ruta_archivo in archivos_json:
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            datos = json.load(f)
            chunks = datos.get("chunks", [])
            
            for chunk in chunks:
                documentos.append(chunk["texto"])
                ids.append(chunk["chunk_id"])
                # Conservamos el origen (el nombre del PDF del que salió) como metadato crucial
                metadatos.append({"fuente": chunk["fuente"]})

    # 4. Inserción masiva en ChromaDB
    total_chunks = len(documentos)
    if total_chunks > 0:
        print(f"💾 Vectorizando e insertando {total_chunks} fragmentos (puede tardar unos segundos)...")
        coleccion.add(
            documents=documentos,
            metadatas=metadatos,
            ids=ids
        )
        print("🚀 ¡Ingesta de JSON finalizada con éxito! Los datos ya son consultables vía embeddings.")
    else:
        print("⚠️ No se encontraron fragmentos (chunks) dentro de los JSON.")

if __name__ == "__main__":
    ingestar_datos_desde_json()