import os
import sys

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

loaded_infra = sys.modules.get("infrastructure")
if loaded_infra is not None:
    infra_path = getattr(loaded_infra, "__file__", "") or ""
    if not infra_path.startswith(ROOT_DIR):
        for name in list(sys.modules):
            if name == "infrastructure" or name.startswith("infrastructure."):
                del sys.modules[name]

from presentation.nodes.clip_translate_node import CLIPTextTranslateNode
from presentation.nodes.prompt_translate_node import PromptTextTranslateNode

NODE_CLASS_MAPPINGS = {
    "CLIPTextTranslateNode": CLIPTextTranslateNode,
    "PromptTextTranslateNode": PromptTextTranslateNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CLIPTextTranslateNode": "Traductor: CLIP Texto (Multi-Idioma)",
    "PromptTextTranslateNode": "Traductor: Prompt Texto (Multi-Idioma)",
}

print(
    "[✅ translator_node] Nodo cargado: soporte multi-idioma con pivot vía EN. Añade modelos en di_container.MODELS"
)
