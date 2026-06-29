import unicodedata
import re

def limpar(txt):

    if not txt:
        return ""

    txt = str(txt).lower()

    txt = unicodedata.normalize(
        "NFKD",
        txt
    )

    txt = "".join(
        c for c in txt
        if not unicodedata.combining(c)
    )

    txt = re.sub(
        r"[^a-z0-9 ]",
        " ",
        txt
    )

    txt = re.sub(
        r"\s+",
        " ",
        txt
    ).strip()

    return txt