import chromadb

def configurar_base_datos():
    # Creamos un cliente persistente que guardará la BD en la carpeta "mi_bd_chroma"
    # Esta carpeta se creará automáticamente en este directorio.
    client = chromadb.PersistentClient(path="./mi_bd_chroma")
    
    # Creamos una colección (es como una tabla en una base de datos)
    # Si ya existe, la podemos eliminar primero o simplemente obtenerla.
    # Aquí vamos a crearla desde cero:
    try:
        client.delete_collection(name="datos_deportivos")
        print("🗑️ Colección anterior eliminada.")
    except Exception:
        pass # Si no existía, ignoramos el error.
        
    collection = client.create_collection(
        name="datos_deportivos",
        metadata={"hnsw:space": "cosine"} # Especificamos la métrica para buscar similitudes
    )
    
    print("✅ Base de datos configurada y colección 'datos_deportivos' creada.")
    print("Directorio de la base de datos: ./mi_bd_chroma")

if __name__ == "__main__":
    configurar_base_datos()
