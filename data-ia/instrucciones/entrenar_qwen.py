from unsloth import FastLanguageModel
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset

# 1. Configuración del modelo (Qwen 7B es ideal para 60GB VRAM)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen2.5-7B-bnb-4bit", # Cargamos en 4bit para ir volando
    max_seq_length = 2048,
    load_in_4bit = True,
)

# 2. Añadir adaptadores LoRA (Esto es lo que el modelo "aprenderá")
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, 
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha = 16,
    lora_dropout = 0,
)

# 3. Cargar tu dataset
dataset = load_dataset("json", data_files="dataset_entrenamiento.jsonl", split="train")

# 4. Configurar el entrenamiento
trainer = SFTTrainer(
    model = model,
    train_dataset = dataset,
    dataset_text_field = "input", # Aquí lee tus JSONs
    max_seq_length = 2048,
    args = TrainingArguments(
        per_device_train_batch_size = 4,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 60, # Puedes subirlo a 300 para un aprendizaje profundo
        learning_rate = 2e-4,
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        logging_steps = 1,
        output_dir = "outputs",
    ),
)

# 5. ¡A ENTRENAR!
trainer.train()

# 6. Guardar para subir a Hugging Face
model.save_pretrained("mi_qwen_deportivo")
tokenizer.save_pretrained("mi_qwen_deportivo")
print("🎉 Entrenamiento finalizado. Modelo guardado en la carpeta 'mi_qwen_deportivo'")