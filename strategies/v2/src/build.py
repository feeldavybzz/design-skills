"""Arma v2/index.html a partir de template.html y los logos generados por logos.py."""
import base64, json, pathlib, re
from fontTools.ttLib import TTFont
import logos

HERE = pathlib.Path(__file__).parent
A = logos.ASSETS

def render(html):
    symbols = "".join(f'<symbol id="{k}" viewBox="{vb}">{body}</symbol>' for k, (vb, body) in A.items())
    html = html.replace("{{SYMBOLS}}", f'<svg width="0" height="0" style="position:absolute" aria-hidden="true">{symbols}</svg>')

    def dims(k):
        _, _, w, h = A[k][0].split(); return w, h
    html = re.sub(r"\[\[([\w-]+)\]\]", lambda m: 'viewBox="0 0 %s %s" data-u="%s" role="img" aria-label="Strategies"' % (*dims(m[1]), m[1]), html)
    html = re.sub(r'(<svg[^>]*data-u="([\w-]+)"[^>]*>)</svg>', r'\1<use href="#\2"/></svg>', html)

    vb, body = A["wm"]
    body = body.replace('<path d="M', '<path class="draw" d="M', 1).replace("<circle ", '<circle class="pop" ', 1)
    html = html.replace("{{WM_VB}}", vb).replace("{{WM_ANIM}}", body)
    html = html.replace("{{PLAIN_S}}", f'<path d="{logos.glyph(TTFont(logos.FONT), "S", 0)}" fill="currentColor"/>')

    foto = base64.b64encode((HERE / "foto-escritorio.jpg").read_bytes()).decode()
    html = html.replace("{{FOTO}}", "data:image/jpeg;base64," + foto)

    html = re.sub(r"\{\{([1-5])\}\}", lambda m: '<span class="dots" aria-hidden="true">%s</span>%s' % (
        "".join('<i class="f"></i>' if i < int(m[1]) else "<i></i>" for i in range(5)), m[1]), html)
    html = re.sub(r"\{\{SCALE:(\w+)\}\}", lambda m: "".join(
        f'<label><input type="radio" name="{m[1]}" id="{m[1]}{i}" value="{i}" aria-label="{i} de 5"></label>' for i in range(1, 6)), html)

    assert "{{" not in html and "[[" not in html, "quedó un marcador sin reemplazar"
    return html

for src, dst in [("template.html", "index.html"), ("template-inversion.html", "inversion.html")]:
    out = render((HERE / src).read_text())
    (HERE.parent / dst).write_text(out)
    print("ok", dst, len(out) // 1024, "KB")
