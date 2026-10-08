"""Gera corujinha-merch.html: página completa em um único arquivo, com as fotos de imagens/ embutidas.
Uso: python3 merch/build.py"""
import base64, os, re
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, "index.html"), encoding="utf-8").read()
mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}

def find(base):
    for ext in mime:
        p = os.path.join(here, base + "." + ext)
        if os.path.exists(p):
            return p, mime[ext]
    return None, None

def embed(m):
    attr, base = m.group(1), m.group(2)
    p, t = find(base)
    if not p:
        return m.group(0)
    data = base64.b64encode(open(p, "rb").read()).decode()
    print("embutida:", os.path.relpath(p, here))
    return f'{attr}="{base}" data-src="data:{t};base64,{data}"'

body = re.sub(r'(data-img)="(imagens/[\w-]+)"', embed, src)
head, rest = body.split("</style>", 1)
out = ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + "</style>\n</head>\n<body>\n" + rest.lstrip("\n") + "</body>\n</html>\n")
open(os.path.join(here, "corujinha-merch.html"), "w", encoding="utf-8").write(out)
print("corujinha-merch.html:", round(len(out) / 1024), "KB")
