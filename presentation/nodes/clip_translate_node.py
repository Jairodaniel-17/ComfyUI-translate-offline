from infrastructure.di_container import translation_usecase


class CLIPTextTranslateNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP",),
                "text": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "src_lang": (["es", "en", "fr", "de"], {"default": "es"}),
                "tgt_lang": (["en", "es", "fr", "de"], {"default": "en"}),
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "conditioning"

    def encode(self, clip, text: str, src_lang: str, tgt_lang: str):
        try:
            result = translation_usecase.execute(text, src_lang, tgt_lang)
            print(
                f"[CLIP Translator] {src_lang}→{tgt_lang}: '{result.translated_text[:200]}'"
            )
            cond, pooled = clip.encode_from_tokens(
                clip.tokenize(result.translated_text), return_pooled=True
            )
            return ([[cond, {"pooled_output": pooled}]],)
        except Exception as e:
            print(f"[CLIP Translator] error: {e}")
            # fallback: usar texto original
            cond, pooled = clip.encode_from_tokens(
                clip.tokenize(text), return_pooled=True
            )
            return ([[cond, {"pooled_output": pooled}]],)
