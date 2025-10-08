from infrastructure.di_container import translation_usecase


class PromptTextTranslateNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True}),
                "src_lang": (["es", "en", "fr", "de"], {"default": "es"}),
                "tgt_lang": (["en", "es", "fr", "de"], {"default": "en"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "get_value"
    CATEGORY = "conditioning"

    def get_value(self, prompt: str, src_lang: str, tgt_lang: str):
        try:
            result = translation_usecase.execute(prompt, src_lang, tgt_lang)
            print(
                f"[Prompt Translator] {src_lang}→{tgt_lang}: '{result.translated_text[:200]}'"
            )
            return (result.translated_text,)
        except Exception as e:
            print(f"[Prompt Translator] error: {e}")
            return (prompt,)
