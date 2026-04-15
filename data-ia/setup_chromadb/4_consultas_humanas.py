import chromadb
import sys

def realizar_consultas_humanas():
    # 1. Nos conectamos a la BD de ChromaDB guardada en local
    client = chromadb.PersistentClient(path="./mi_bd_chroma")
    
    try:
        collection = client.get_collection(name="datos_deportivos")
    except Exception:
        print("❌ La colección no existe. Asegúrate de que el path y el nombre sean correctos.")
        sys.exit(1)
        
    # 2. Batería de preguntas con contexto completo (Humanizadas)
    preguntas_mejoradas = [
        "¿Cuál fue el total de personas empleadas en el sector deportivo en el periodo de 2025-1T a 2025-4T?",
        "¿Qué porcentaje del empleo vinculado al deporte correspondió a hombres en el periodo de 2025-1T hasta 2025-4T?",
        "¿Qué porcentaje de los empleados en el deporte tienen entre 16 y 24 años en el periodo de 2025-1T hasta 2025-4T?",
        "Del total de personas que trabajan en el deporte, ¿qué proporción tiene educación superior o equivalente?"
    ]
    
    print("🤖 Iniciando batería de consultas contextualizadas...\n" + "="*60)
    
    # 3. Ejecutamos cada pregunta
    for i, query_texto in enumerate(preguntas_mejoradas, 1):
        print(f"\n🔍 Búsqueda {i}: '{query_texto}'")
        
        # Realizamos la consulta pidiendo los 2 resultados más relevantes
        resultados = collection.query(
            query_texts=[query_texto],
            n_results=2 
        )
        
        print("✨ Resultados encontrados:")
        
        # Comprobamos si hay resultados
        if not resultados['ids'][0]:
            print("   ⚠️ No se encontraron resultados relevantes.")
            continue
            
        # Imprimimos los resultados de forma limpia
        for j in range(len(resultados['ids'][0])):
            distancia = resultados['distances'][0][j]
            documento = resultados['documents'][0][j]
            
            # Una distancia más cercana a 0 significa mayor similitud semántica
            print(f"   Opción {j+1} (Distancia: {distancia:.4f}):")
            print(f"   📄 {documento}\n")
            
        print("-" * 60)

if __name__ == "__main__":
    realizar_consultas_humanas()