"""O CÉU NÃO ESQUECE OS SEUS (Mt 6:26) — prévia do lettering (parte 1).

Camiseta branca/off-white. Paleta inspirada na referência (vermelho +
azuis), com o vermelho da marca. A ilustração (pardal + ramo de trigo) entra
depois; aqui ela aparece como área reservada.

uso: python3 make_ceu_lettering.py <opcao> <saida.svg>
  1 = Berkshire Swash (caixa alta com caudas/swash — a mais próxima da ref.)
  2 = Lobster (pincel grosso, contraste forte)
  3 = Norican (traço de tatuagem/vintage)
O lettering da referência é desenhado à mão (não existe como fonte);
usamos a fonte livre mais parecida, sem copiar as letras do artista.
"""
import sys

from corujinha_art import Font, Text, cm, document, logo_svg

RED = "#C83438"
NAVY = "#1E3558"
SKY = "#4E9FD8"
PAPER = "#FFFFFF"

W, H = round(cm(27)), round(cm(32))
FONTS = {1: "BerkshireSwash-Regular", 2: "Lobster-Regular", 3: "Norican-Regular"}
CREAM = "#F4EEDD"  # contorno claro em volta das letras, como na referência

# (texto, deslocamento x relativo, escala) — linhas escalonadas como na ref.
LINES = [("O CÉU NÃO", -0.06, 1.00), ("ESQUECE", 0.05, 1.12), ("OS SEUS", -0.02, 1.05)]


def lettering(font, cx, top, width):
    f = Font(font)
    base = 1000
    ws = [f.ink(t, base * s)[2] - f.ink(t, base * s)[0] for t, _, s in LINES]
    size = base * width / max(ws)
    cap = (lambda b: b[3] - b[1])(f.ink("C", 1000)) / 1000
    out_w = size * 0.075            # contorno branco que separa as linhas
    shadow = (size * 0.035, size * 0.045)
    parts, y = [], top
    for (t, dx, s), w in zip(LINES, ws):
        sz = size * s
        y += sz * cap
        tx = Text(f, t, sz, RED)
        tx.place(cx=cx + dx * width)
        tx.dy = y
        d = f.layout(t, sz, 0, tx.dx, tx.dy)[0]
        sx, sy = shadow
        parts.append(
            f'<path fill="{CREAM}" stroke="{CREAM}" stroke-width="{out_w*2:.1f}" '
            f'stroke-linejoin="round" d="{d}"/>'
            f'<path fill="{RED}" d="{d}"/>')
        y += sz * cap * 0.18        # entrelinha curta: as linhas se encaixam (como na ref.)
    return parts, y


ILLUS = None  # caminho do PNG da ilustração (prévia); None = área reservada


def illustration(cx, top, height):
    """Prévia: embute o PNG da ilustração recortado na área desenhada."""
    import base64, io
    from PIL import Image
    im = Image.open(ILLUS).convert("RGB")
    mask = im.convert("L").point(lambda v: 255 if v < 235 else 0)
    im = im.crop(mask.getbbox())
    buf = io.BytesIO(); im.save(buf, "PNG")
    w = height * im.width / im.height
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f'<image x="{cx - w/2:.1f}" y="{top:.1f}" width="{w:.1f}" height="{height:.1f}" '
            f'href="data:image/png;base64,{b64}"/>')


def build(opt, out):
    cx = W / 2
    body = []
    # referência no topo
    top = Font(FONTS[opt])
    ref = Text(top, "Mt 6:26", cm(1.8), RED).place(cx=cx, top=cm(2.0))
    body.append(ref.svg())
    b = ref.box()
    # traço/flourish embaixo da referência, como o da referência visual
    y = b[3] + cm(0.35)
    body.append(
        f'<path fill="none" stroke="{RED}" stroke-width="{cm(0.16):.1f}" stroke-linecap="round" '
        f'd="M{b[0]-cm(0.6):.1f} {y+cm(0.25):.1f} Q{cx:.1f} {y-cm(0.45):.1f} {b[2]+cm(1.2):.1f} {y:.1f}"/>')
    if ILLUS:
        body.append(illustration(cx, cm(4.6), cm(16.2)))
    else:
        ix0, iy0, ix1, iy1 = cm(3), cm(5.2), W - cm(3), cm(18.5)
        body.append(
        f'<rect x="{ix0:.1f}" y="{iy0:.1f}" width="{ix1-ix0:.1f}" height="{iy1-iy0:.1f}" '
        f'rx="{cm(1):.1f}" fill="#EEF4FA" stroke="{SKY}" stroke-width="6" stroke-dasharray="30 22"/>')
        lab = Text(Font("Montserrat-600"), "ILUSTRAÇÃO: PARDAL + RAMO DE TRIGO",
                   cm(0.75), SKY, tracking=120).place(cx=cx, cy=(iy0 + iy1) / 2)
        body.append(lab.svg())
    # lettering principal, sobrepondo levemente a base da ilustração
    parts, yb = lettering(FONTS[opt], cx, cm(17.0), cm(18))
    body.append(f'<g transform="rotate(-6 {cx:.1f} {cm(22.5):.1f})">' + "".join(parts) + "</g>")
    # corujinha da marca embaixo do lettering
    body.append(logo_svg(cx, yb + cm(2.0), cm(2.2), NAVY)[0])
    open(out, "w").write(document("\n".join(body), W, H))


if __name__ == "__main__":
    if len(sys.argv) > 3:
        ILLUS = sys.argv[3]
    build(int(sys.argv[1]), sys.argv[2])
