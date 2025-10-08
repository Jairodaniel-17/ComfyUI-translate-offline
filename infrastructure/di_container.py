# Contenedor simple: mapea pares de idiomas a modelos y provee translation_usecase
from application.translation_usecase import TranslationUseCase
from domain.translation_service import TranslationService
from infrastructure.adapters.onnx_translator_adapter import LazyONNXTranslatorAdapter
from infrastructure.cache_service import CacheService
from infrastructure.nltk_sentence_splitter import NLTKSentenceSplitter

# ===================================
# MAPA DE MODELOS (agrega pares aquí)
# ===================================
# Para escalar: añade pares (src,tgt): "HF/model-name"
MODELS = {
    ("es", "en"): "Xenova/opus-mt-es-en",
    ("en", "es"): "Xenova/opus-mt-en-es",
    ("fr", "en"): "Helsinki-NLP/opus-mt-fr-en",
    ("en", "fr"): "Helsinki-NLP/opus-mt-en-fr",
    ("de", "en"): "Helsinki-NLP/opus-mt-de-en",
    ("en", "de"): "Helsinki-NLP/opus-mt-en-de",
    # añade más pares aquí
}

# Creamos adaptadores perezosos para cada par
_translators = {
    pair: LazyONNXTranslatorAdapter(model) for pair, model in MODELS.items()
}

# Sentence splitter y servicio de dominio
_splitter = NLTKSentenceSplitter()
_service = TranslationService(_splitter, chunk_size=400)

# Cache service
_cache = CacheService()

# Instancia de caso de uso
translation_usecase = TranslationUseCase(_translators, _service, _cache)
