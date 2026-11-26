import re
import unicodedata


def normalize_answer(text: str) -> str:
    """Minúsculas, sem acentos e com espaços colapsados, para comparar respostas."""
    decomposed = unicodedata.normalize("NFKD", text)
    without_accents = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", without_accents).strip().lower()
