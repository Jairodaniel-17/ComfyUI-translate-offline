import os
import sys

sys.path.append(os.path.dirname(__file__))

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
