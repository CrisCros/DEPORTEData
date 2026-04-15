# deporte-qwen-train

Scaffold mínimo para una primera prueba local de fine-tuning QLoRA sobre **Qwen/Qwen2.5-1.5B-Instruct**.

## 1) Crear entorno virtual

```bash
cd deporte-qwen-train
python3 -m venv .venv
source .venv/bin/activate
```

## 2) Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Validar dataset

```bash
cd scripts
python3 prepare_dataset.py --train ../data/train.jsonl --val ../data/val.jsonl
```

## 4) Lanzar entrenamiento (QLoRA)

> Funciona en CPU o GPU. En CPU será más lento; en GPU usará fp16 automáticamente.

```bash
cd scripts
python3 train_local.py \
  --model_name Qwen/Qwen2.5-1.5B-Instruct \
  --train_file ../data/train.jsonl \
  --val_file ../data/val.jsonl \
  --output_dir ../outputs
```

## 5) Probar inferencia

```bash
cd scripts
python3 test_inference.py \
  --model_name Qwen/Qwen2.5-1.5B-Instruct \
  --adapter_path ../outputs \
  --question "Explica la diferencia entre variación absoluta y porcentual en empleo deportivo"
```

---


## 6) Fusionar LoRA + base (modelo standalone)

```bash
cd scripts
python3 merge_model.py \
  --model_name Qwen/Qwen2.5-1.5B-Instruct \
  --adapter_path ../outputs \
  --merged_output_path ../merged_model
```

El resultado en `../merged_model` ya no requiere PEFT para inferencia.

## Comando exacto (pipeline básico)

```bash
cd deporte-qwen-train/scripts && python3 prepare_dataset.py --train ../data/train.jsonl --val ../data/val.jsonl && python3 train_local.py --model_name Qwen/Qwen2.5-1.5B-Instruct --train_file ../data/train.jsonl --val_file ../data/val.jsonl --output_dir ../outputs && python3 test_inference.py --model_name Qwen/Qwen2.5-1.5B-Instruct --adapter_path ../outputs --question "Resume la evolución interanual del empleo deportivo"
```
