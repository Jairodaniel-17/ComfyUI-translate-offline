# Lazy loader + adapter para modelos ONNX (Marian via optimum)
import traceback

import torch
from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import MarianTokenizer


class LazyONNXTranslatorAdapter:
    """
    Adapter perezoso: no carga el tokenizador/modelo hasta la primera traducción.
    model_name: nombre del repo HF (ej. Xenova/opus-mt-es-en)
    """

    def __init__(self, model_name):
        self.model_name = model_name
        self._loaded = False
        self.tokenizer = None
        self.model = None

    def _load(self):
        if self._loaded:
            return
        try:
            self.tokenizer = MarianTokenizer.from_pretrained(self.model_name)
            self.model = ORTModelForSeq2SeqLM.from_pretrained(self.model_name)
            self._loaded = True
            print(f"[ONNX Adapter] Modelo cargado: {self.model_name}")
        except Exception as e:
            print(f"[ONNX Adapter] Error cargando {self.model_name}: {e}")
            traceback.print_exc()
            raise

    def translate_chunk(self, chunk: str) -> str:
        self._load()
        try:
            inputs = self.tokenizer(
                [chunk], return_tensors="pt", padding=True, truncation=True
            )
            with torch.inference_mode():
                outputs = self.model.generate(**inputs)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"[ONNX Adapter] Error en inferencia ({self.model_name}): {e}")
            traceback.print_exc()
            # Devolver chunk original si falla
            return chunk
