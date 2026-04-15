import time
import os
import ray

# Inicializamos el entorno de Ray.
# Cuando ejecutas esto con 'ray job submit', Ray ya estará configurado por el clúster.
ray.init(ignore_reinit_error=True)

# La decoración @ray.remote indica que esta función será ejecutada asíncronamente
# por un worker en el clúster de Ray.
@ray.remote
def entrenar_modelo(id_tarea, epocas=5):
    print(f"[Worker {id_tarea}] Iniciando el entrenamiento...")
    
    resultado_mock = {}
    
    for epoch in range(1, epocas + 1):
        # Simulamos carga computacional
        time.sleep(1)
        loss = 1.0 / (epoch + id_tarea)
        
        print(f"[Worker {id_tarea}] Época {epoch}/{epocas} completada. Loss: {loss:.4f}")
        resultado_mock['final_loss'] = loss

    print(f"[Worker {id_tarea}] Entrenamiento finalizado.")
    return resultado_mock

if __name__ == "__main__":
    print("🚀 Iniciando el Job de Ray (Script de Base)")
    
    # Supongamos que queremos entrenar varios modelos o realizar validación cruzada en paralelo
    num_experimentos = 3
    print(f"Lanzando {num_experimentos} experimentos en paralelo...")
    
    # Lanzamos las tareas (fíjate que llamamos a .remote)
    futuros = [entrenar_modelo.remote(id_tarea=i) for i in range(num_experimentos)]
    
    # ray.get bloquea la ejecución hasta que todos los workers terminan y te devuelve los resultados
    resultados = ray.get(futuros)
    
    print("\n✅ Todos los entrenamientos finalizaron con éxito.")
    for i, res in enumerate(resultados):
        print(f"Experimento {i}: {res}")
    
    # Ejemplo simulado de guardado local
    print("\nSimulando guardado del modelo en el directorio de trabajo...")
    os.makedirs("modelos_guardados", exist_ok=True)
    with open("modelos_guardados/metricas.txt", "w") as f:
        f.write(str(resultados))
    print("Datos guardados en ./modelos_guardados/metricas.txt")
