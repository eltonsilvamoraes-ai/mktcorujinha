"""Gera as versões publicáveis da página a partir de index.html.

- corujinha-merch.html: arquivo único, com as fotos embutidas (para enviar ou visualizar).
- site/ + personalizados-site.zip: pasta para subir no servidor (KingHost), com index.html,
  imagens/, robots.txt e sitemap.xml. Fotos como arquivos normais, indexáveis pelo Google.

Nos dois casos as fotos entram direto no HTML como <img> com alt (sem depender do JavaScript).
Uso: python3 merch/build.py"""
import base64, html, os, re, shutil, zipfile
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://personalizados.amarcadacorujinha.com.br/"
src = open(os.path.join(here, "index.html"), encoding="utf-8").read()
mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
EXTRA = ["og.jpg", "favicon.svg", "apple-touch-icon.png"]  # usados no <head>, não nos espaços de foto


def find(base):
    for ext in mime:
        p = os.path.join(here, base + "." + ext)
        if os.path.exists(p):
            return p, mime[ext]
    return None, None


def with_photos(page, embed):
    """Coloca um <img> dentro de cada espaço data-img que tem foto em imagens/."""
    used = []

    def put(m):
        tag, base = m.group(0), m.group(2)
        p, t = find(base)
        if not p:
            return tag
        cap = re.search(r"<figcaption>Foto:\s*(.*?)</figcaption>", page[m.end():])
        alt = html.escape(html.unescape(cap.group(1)), quote=True) if cap else ""
        w, h = Image.open(p).size
        pos = re.search(r'data-pos="([^"]+)"', tag)
        style = f' style="object-position:{pos.group(1)}"' if pos else ""
        if embed:
            url = f"data:{t};base64," + base64.b64encode(open(p, "rb").read()).decode()
        else:
            url = os.path.relpath(p, here).replace(os.sep, "/")
            used.append(url)
        tag = re.sub(r'class="ph\b', 'class="ph has-img', tag, count=1)
        return f'{tag}<img class="ph-img" src="{url}" alt="{alt}" width="{w}" height="{h}" loading="lazy" decoding="async"{style}>'

    out = re.sub(r'<(div|figure) data-img="(imagens/[\w-]+)"[^>]*>', put, page)
    return out, used


def document(page):
    head, rest = page.split("</style>", 1)
    return ('<!doctype html>\n<html lang="pt-BR">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head + "</style>\n</head>\n<body>\n" + rest.lstrip("\n") + "</body>\n</html>\n")


# 1) arquivo único
single, _ = with_photos(src, embed=True)
single = document(single)
open(os.path.join(here, "corujinha-merch.html"), "w", encoding="utf-8").write(single)
print("corujinha-merch.html:", round(len(single) / 1024), "KB")

# 2) pasta do site
site = os.path.join(here, "site")
shutil.rmtree(site, ignore_errors=True)
os.makedirs(os.path.join(site, "imagens"))
page, used = with_photos(src, embed=False)
for rel in used + ["imagens/" + f for f in EXTRA if os.path.exists(os.path.join(here, "imagens", f))]:
    shutil.copy(os.path.join(here, rel), os.path.join(site, rel))
open(os.path.join(site, "index.html"), "w", encoding="utf-8").write(document(page))
open(os.path.join(site, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}sitemap.xml\n")
open(os.path.join(site, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"  <url><loc>{SITE_URL}</loc></url>\n</urlset>\n")
zpath = os.path.join(here, "personalizados-site.zip")
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(site):
        for f in sorted(files):
            full = os.path.join(root, f)
            z.write(full, os.path.relpath(full, site))
print("site/:", ", ".join(sorted(os.listdir(site))), "| imagens:", ", ".join(sorted(os.listdir(os.path.join(site, "imagens")))))
print("personalizados-site.zip:", round(os.path.getsize(zpath) / 1024), "KB")
