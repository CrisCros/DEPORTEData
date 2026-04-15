import chromadb
import sys

def consultar_datos():
    # Nos conectamos a la BD guardada
    client = chromadb.PersistentClient(path="./mi_bd_chroma")
    
    try:
        collection = client.get_collection(name="datos_deportivos")
    except Exception:
        print("❌ La colección no existe. Debes crearla e ingestar datos primero.")
        sys.exit(1)
        
    # ¿Qué queremos buscar?
    query_texto = "¿Cuántos son en total de 2025-1T?"
    print(f"🔍 Búsqueda: '{query_texto}'\n")
    
    # Realizamos la consulta a Chroma
    resultados = collection.query(
        query_texts=[query_texto],
        n_results=3 # Queremos los 3 resultados más relevantes
    )
    
    # Mostramos los resultados
    print("✨ Resultados encontrados:\n")
    
    for i in range(len(resultados['ids'][0])):
        distancia = resultados['distances'][0][i]
        documento = resultados['documents'][0][i]
        
        print(f"Opción {i+1} (Relevancia heurística/Distancia: {distancia:.4f}):")
        print(f"📄 {documento}")
        print("-" * 50)

if __name__ == "__main__":
    consultar_datos()
