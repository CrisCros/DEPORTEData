#!/usr/bin/env python3
"""Fusiona un adapter LoRA con el modelo base y guarda un modelo standalone."""

from __future__ import annotations

import argparse
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge base model + LoRA adapter")
    parser.add_argument("--model_name", default="Qwen/Qwen2.5-1.5B-Instruct")
    parser.add_argument("--adapter_path", default="../outputs")
    parser.add_argument("--merged_output_path", default="../merged_model")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    base_dir = Path(__file__).resolve().parent
    adapter_path = base_dir.joinpath(args.adapter_path).resolve()
    merged_output_path = base_dir.joinpath(args.merged_output_path).resolve()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    print(f"Cargando modelo base: {args.model_name}")
    print(f"Cargando adapter LoRA desde: {adapter_path}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_name, use_fast=True)
    base_model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=dtype,
        trust_remote_code=True,
    ).to(device)

    model = PeftModel.from_pretrained(base_model, str(adapter_path))

    print("Fusionando adapter LoRA con el modelo base...")
    merged_model = model.merge_and_unload()

    merged_output_path.mkdir(parents=True, exist_ok=True)
    merged_model.save_pretrained(str(merged_output_path))
    tokenizer.save_pretrained(str(merged_output_path))

    print(f"Modelo fusionado guardado en: {merged_output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
