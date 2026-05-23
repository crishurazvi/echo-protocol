
import base64
import html
import re
from pathlib import Path
from urllib.parse import unquote_plus

import streamlit as st
import streamlit.components.v1 as components


APP_DIR = Path(__file__).parent
ASSETS = APP_DIR / "assets"


st.set_page_config(
    page_title="Protocol ecocardiografie ECHOTIM",
    page_icon="🫀",
    layout="wide",
)


def b64_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


PAGE1_B64 = b64_image(ASSETS / "protocol_page1.png")
PAGE2_B64 = b64_image(ASSETS / "protocol_page2.png")


PAGE_DIMS = {
    1: (601, 871),
    2: (615, 855),
}


def norm_key(s: str) -> str:
    s = str(s or "").strip().lower()
    table = str.maketrans({
        "ă": "a", "â": "a", "î": "i", "ș": "s", "ş": "s", "ț": "t", "ţ": "t",
    })
    s = s.translate(table)
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


# Canonical keys accepted by the app.
# Values can come either from the short aliases or from HIPOCRATE field codes v238, v239 etc.
ALIASES = {
    # administrative
    "data": "data_exam", "dataexaminarii": "data_exam", "nume": "nume", "prenume": "prenume",
    "varsta": "varsta", "salon": "salon", "inaltime": "inaltime", "greutate": "greutate",
    "scorp": "scorp", "scorporala": "scorp", "calitate": "calitate",
    "ritm": "ritm", "fc": "fc", "frecventa": "fc", "ta": "ta", "tensiune": "ta",

    # parasternal / LV dimensions
    "aoinel": "aoinel", "aolainel": "aoinel", "aoasc": "aoasc", "aoascendenta": "aoasc",
    "sinusvals": "sinusvals", "aosinus": "sinusvals", "sinusurivalsalva": "sinusvals",
    "dao": "dao", "deschidereao": "dao", "deschiderevao": "dao",
    "va": "va", "valvaaortica": "va", "aspectvalvaaortica": "va",
    "as": "as", "diamas": "as", "atriustang": "as",
    "vd": "vd", "diamvd": "vd", "peretevd": "peretevd",
    "siv": "siv", "ivsd": "siv", "sept": "siv", "septiv": "siv",
    "dtdvs": "dtdvs", "ddvs": "dtdvs", "lvidd": "dtdvs",
    "dtsvs": "dtsvs", "dsvs": "dtsvs", "lvids": "dtsvs",
    "ppvs": "ppvs", "lvpw": "ppvs", "pw": "ppvs",
    "fs": "fs", "mpsiv": "mpsiv", "masavs": "masavs",
    "vm": "vm", "valvamitrala": "vm", "aspectvalvamitral": "vm",

    # apical / volumes
    "vtd": "vtd", "vtdidx": "vtdidx", "vts": "vts", "vtsidx": "vtsidx",
    "fe": "fevs", "fevs": "fevs", "ef": "fevs", "lvef": "fevs",
    "feplanimetric": "fevs", "feplanimetrica": "fevs",
    "suprafas": "suprafas", "laarea": "suprafas",
    "volas": "volas", "lavi": "volasidx", "volasidx": "volasidx",
    "mapse": "mapse",
    "dvs": "dvs", "dvd": "dvd", "dad": "dad", "das": "das",
    "fe2c": "fe2c", "fe2camere": "fe2c",
    "fd": "functiediastolica", "functiediastolica": "functiediastolica",

    # mitral flow / tissue Doppler
    "e": "e", "emitral": "e", "a": "a", "amitral": "a",
    "durataa": "durataa", "ea": "ea", "tde": "tde", "triv": "triv", "vp": "vp",
    "sprimlat": "sprimlat", "elat": "elat", "alat": "alat",
    "sprimsiv": "sprimsiv", "esiv": "esiv", "asiv": "asiv", "ee": "ee",

    # mitral valve disease
    "sm": "sm", "stenozamitrala": "sm", "pmmitral": "pmmitral", "pmedmitral": "pmmitral",
    "phtmitral": "phtmitral", "sphtmitral": "sphtmitral", "smitral": "smitral",
    "splanmitral": "splanmitral", "spisamitral": "spisamitral", "sfcontmitral": "sfcontmitral",
    "im": "im", "mr": "im", "insuficientamitrala": "im",
    "sorim": "sorim", "eroa": "sorim", "vrim": "vrim", "frim": "frim", "vcim": "vcim", "dpdt": "dpdt",
    "vps": "vps", "vpd": "vpd", "vpsd": "vpsd", "duratara": "duratara",

    # aortic
    "vmaxao": "vmaxao", "vaovmax": "vmaxao", "pmaxao": "pmaxao", "itvao": "itvao",
    "tevs": "tevs", "qao": "qao", "qs": "qao",
    "sa": "sa", "stenozaao": "sa", "stenozaaortica": "sa",
    "pmedao": "pmedao", "scontao": "scontao", "splanao": "splanao",
    "ia": "ia", "ar": "ia", "insuficientaaortica": "ia",
    "phtao": "phtao", "soria": "soria", "vria": "vria", "fria": "fria", "vcia": "vcia", "aortadesc": "aortadesc",

    # tricuspid
    "et": "et", "atricusp": "atricusp", "stricusp": "stricusp", "eprimtricuspid": "eprimtricuspid",
    "aprimtricuspid": "aprimtricuspid", "eetricuspid": "eetricuspid",
    "st": "st", "stenozatricuspidiana": "st", "pmedt": "pmedt", "phtt": "phtt", "sphtt": "sphtt",
    "it": "it", "tr": "it", "insuficientatricuspidiana": "it",
    "vmaxtr": "vmaxtr", "pmaxt": "pmaxt", "paps": "paps", "psap": "paps",

    # pulmonary
    "vmaxp": "vmaxp", "pmaxp": "pmaxp", "itvp": "itvp", "tevd": "tevd",
    "qp": "qp", "tacc": "tacc", "sp": "sp", "stenozapulmonara": "sp",
    "pmedp": "pmedp", "scontp": "scontp", "ip": "ip", "insuficientapulmonara": "ip",
    "phtp": "phtp", "pdap": "pdap",

    # page 2 structure
    "cinetica": "cinetica", "wallmotion": "cinetica", "wmsi": "wmsi", "gls": "gls",
    "fac": "fac", "fevd": "fevd", "tapse": "tapse", "fdvd": "fdvd",
    "formatiuniatriale": "formatiuniatriale", "descformatiuniatriale": "descformatiuniatriale",
    "formatiuniventriculare": "formatiuniventriculare", "descformatiuniventriculare": "descformatiuniventriculare",
    "pericard": "pericard", "lichidpericardic": "pericard", "cantitatepericard": "cantitatepericard",
    "pericardant": "pericardant", "pericardpost": "pericardpost", "aspectpericard": "aspectpericard",
    "vci": "vci", "diamvci": "vci", "ivc": "vci", "colapsvci": "colapsvci",
    "observatii": "observatii", "altemasuratori": "observatii",
    "concluzie": "concluzie", "concluzii": "concluzie", "medic": "medic", "examinator": "medic",
}


# Mapping from HIPOCRATE field codes to the protocol keys.
HIPO = {
    "v238": "aoinel", "v239": "aoasc", "v240": "dao", "v241": "va", "v242": "as",
    "v243": "vd", "v244": "peretevd", "v245": "siv", "v246": "dtdvs", "v247": "dtsvs",
    "v248": "ppvs", "v249": "fs", "v250": "mpsiv", "v251": "feteich", "v252": "masavs",
    "v253": "vm", "v254": "vtd", "v255": "vts", "v256": "fevs", "v257": "suprafas",
    "v258": "volas", "v259": "functiediastolica", "v260": "e", "v261": "a",
    "v262": "eprim", "v263": "aprim", "v264": "sprim", "v265": "sm", "v266": "pmmitral",
    "v268": "phtmitral", "v271": "smitral", "v272": "splanmitral", "v273": "im",
    "v275": "sorim", "v276": "vrim", "v277": "vcim", "v278": "vps", "v279": "vpd",
    "v280": "imra", "v281": "vmaxao", "v282": "pmaxao", "v283": "itvao",
    "v284": "tevs", "v285": "qao", "v287": "sa", "v288": "pmedao", "v289": "scontao",
    "v290": "splanao", "v291": "ia", "v292": "phtao", "v293": "soria", "v294": "vria",
    "v295": "vcia", "v296": "aortadesc", "v297": "et", "v298": "atricusp",
    "v299": "st", "v300": "pmedt", "v301": "phtt", "v302": "it", "v303": "pmaxt",
    "v304": "paps", "v305": "vmaxp", "v306": "pmaxp", "v307": "itvp", "v308": "qp",
    "v309": "tacc", "v310": "sp", "v311": "pmedp", "v312": "ip", "v313": "cinetica",
    "v314": "wmsi", "v317": "pericard", "v318": "pericardant", "v319": "pericardpost",
    "v320": "vci", "v321": "colapsvci", "v322": "medic", "v323": "mapse",
    "v324": "tapse", "v214": "concluzie",
}


def canonical_key(raw_key: str) -> str:
    k = norm_key(raw_key)
    if not k:
        return ""
    if k in HIPO:
        return HIPO[k]
    if re.fullmatch(r"\d+", k):
        return HIPO.get("v" + k, "v" + k)
    if k in ALIASES:
        return ALIASES[k]
    return k


def parse_pairs(text: str) -> dict:
    data = {}
    if not text:
        return data

    # semicolon or newline separated; keep colons inside long conclusion if user uses key=value
    chunks = re.split(r"[;\n]+", text)
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        if "=" in chunk:
            key, value = chunk.split("=", 1)
        elif ":" in chunk:
            key, value = chunk.split(":", 1)
        else:
            continue

        key = canonical_key(key)
        value = value.strip().replace(",", ".")
        if key and value:
            data[key] = value
    return data


def v(data: dict, key: str) -> str:
    return html.escape(str(data.get(key, "")))


def pos(page: int, x: float, y: float, w: float = 55, fs: int = 14, cls: str = "") -> dict:
    pw, ph = PAGE_DIMS[page]
    return {
        "left": x / pw * 100,
        "top": y / ph * 100,
        "width": w / pw * 100,
        "fs": fs,
        "cls": cls,
    }


# Approximate overlay coordinates on the scanned protocol backgrounds.
FIELDS = {
    # Page 1 administrative
    "data_exam": (1, pos(1, 104, 181, 105, 12)),
    "nume": (1, pos(1, 58, 199, 230, 12)),
    "prenume": (1, pos(1, 335, 199, 120, 12)),
    "varsta": (1, pos(1, 492, 199, 45, 12)),
    "salon": (1, pos(1, 552, 199, 45, 12)),
    "inaltime": (1, pos(1, 68, 216, 35, 12)),
    "greutate": (1, pos(1, 156, 216, 35, 12)),
    "scorp": (1, pos(1, 249, 216, 42, 12)),
    "calitate": (1, pos(1, 420, 216, 90, 12)),
    "fc": (1, pos(1, 414, 232, 60, 12)),
    "ta": (1, pos(1, 490, 232, 80, 12)),

    # Page 1 parasternal
    "aoinel": (1, pos(1, 93, 276, 38)),
    "aoasc": (1, pos(1, 299, 276, 42)),
    "sinusvals": (1, pos(1, 526, 276, 42)),
    "dao": (1, pos(1, 115, 292, 42)),
    "va": (1, pos(1, 249, 307, 330, 12, "long")),
    "as": (1, pos(1, 70, 322, 42)),
    "vd": (1, pos(1, 70, 337, 42)),
    "peretevd": (1, pos(1, 254, 337, 35)),
    "siv": (1, pos(1, 55, 351, 42)),
    "mpsiv": (1, pos(1, 452, 351, 32, 12)),
    "dtdvs": (1, pos(1, 74, 366, 42)),
    "dtsvs": (1, pos(1, 74, 381, 42)),
    "ppvs": (1, pos(1, 74, 395, 42)),
    "fs": (1, pos(1, 61, 410, 42)),
    "masavs": (1, pos(1, 250, 410, 58)),
    "vm": (1, pos(1, 250, 425, 330, 12, "long")),

    # Page 1 apical
    "vtd": (1, pos(1, 58, 470, 44)),
    "vtdidx": (1, pos(1, 136, 470, 44)),
    "vts": (1, pos(1, 58, 485, 44)),
    "vtsidx": (1, pos(1, 136, 485, 44)),
    "fevs": (1, pos(1, 102, 500, 44)),
    "suprafas": (1, pos(1, 91, 514, 50)),
    "volas": (1, pos(1, 188, 514, 45)),
    "volasidx": (1, pos(1, 284, 514, 55)),
    "mapse": (1, pos(1, 76, 529, 44)),
    "dvs": (1, pos(1, 535, 470, 44)),
    "dvd": (1, pos(1, 535, 485, 44)),
    "dad": (1, pos(1, 535, 500, 44)),
    "das": (1, pos(1, 535, 514, 44)),
    "fe2c": (1, pos(1, 125, 555, 44)),
    "functiediastolica": (1, pos(1, 208, 571, 300, 12, "long")),

    # Page 1 mitral flow
    "e": (1, pos(1, 94, 600, 42)),
    "a": (1, pos(1, 160, 600, 42)),
    "durataa": (1, pos(1, 250, 600, 42)),
    "ea": (1, pos(1, 318, 600, 42)),
    "tde": (1, pos(1, 390, 600, 42)),
    "triv": (1, pos(1, 55, 615, 42)),
    "vp": (1, pos(1, 212, 615, 42)),
    "sprimlat": (1, pos(1, 161, 630, 42)),
    "elat": (1, pos(1, 275, 630, 42)),
    "alat": (1, pos(1, 354, 630, 42)),
    "sprimsiv": (1, pos(1, 161, 646, 42)),
    "esiv": (1, pos(1, 275, 646, 42)),
    "asiv": (1, pos(1, 354, 646, 42)),
    "ee": (1, pos(1, 515, 646, 42)),

    "sm": (1, pos(1, 254, 661, 105, 12)),
    "pmmitral": (1, pos(1, 75, 676, 42)),
    "phtmitral": (1, pos(1, 158, 676, 42)),
    "sphtmitral": (1, pos(1, 246, 676, 42)),
    "splanmitral": (1, pos(1, 345, 676, 42)),
    "spisamitral": (1, pos(1, 442, 676, 42)),
    "sfcontmitral": (1, pos(1, 533, 676, 42)),
    "im": (1, pos(1, 255, 691, 110, 12)),
    "sorim": (1, pos(1, 52, 707, 42)),
    "vrim": (1, pos(1, 136, 707, 42)),
    "frim": (1, pos(1, 214, 707, 42)),
    "vcim": (1, pos(1, 288, 707, 42)),
    "dpdt": (1, pos(1, 374, 707, 65)),
    "vps": (1, pos(1, 142, 722, 42)),
    "vpd": (1, pos(1, 210, 722, 42)),
    "vpsd": (1, pos(1, 277, 722, 42)),
    "duratara": (1, pos(1, 385, 722, 42)),

    # Page 1 aortic flow
    "vmaxao": (1, pos(1, 123, 751, 45)),
    "pmaxao": (1, pos(1, 231, 751, 45)),
    "itvao": (1, pos(1, 327, 751, 45)),
    "tevs": (1, pos(1, 431, 751, 45)),
    "qao": (1, pos(1, 525, 751, 45)),
    "sa": (1, pos(1, 250, 767, 110, 12)),
    "pmedao": (1, pos(1, 65, 782, 45)),
    "scontao": (1, pos(1, 151, 782, 45)),
    "splanao": (1, pos(1, 252, 782, 45)),
    "ia": (1, pos(1, 250, 798, 110, 12)),
    "phtao": (1, pos(1, 55, 814, 45)),
    "soria": (1, pos(1, 136, 814, 45)),
    "vria": (1, pos(1, 218, 814, 45)),
    "fria": (1, pos(1, 290, 814, 45)),
    "vcia": (1, pos(1, 360, 814, 45)),
    "aortadesc": (1, pos(1, 505, 814, 55)),

    # Page 2 tricuspid / pulmonary
    "et": (2, pos(2, 119, 31, 42)),
    "atricusp": (2, pos(2, 186, 31, 42)),
    "stricusp": (2, pos(2, 260, 31, 42)),
    "eprimtricuspid": (2, pos(2, 372, 31, 42)),
    "aprimtricuspid": (2, pos(2, 470, 31, 42)),
    "eetricuspid": (2, pos(2, 553, 31, 42)),
    "st": (2, pos(2, 250, 47, 110, 12)),
    "pmedt": (2, pos(2, 65, 64, 42)),
    "phtt": (2, pos(2, 150, 64, 42)),
    "sphtt": (2, pos(2, 240, 64, 42)),
    "it": (2, pos(2, 248, 80, 100, 12)),
    "vmaxtr": (2, pos(2, 380, 80, 42)),
    "pmaxt": (2, pos(2, 490, 80, 42)),
    "paps": (2, pos(2, 570, 80, 42)),

    "vmaxp": (2, pos(2, 137, 108, 42)),
    "pmaxp": (2, pos(2, 235, 108, 42)),
    "itvp": (2, pos(2, 332, 108, 42)),
    "tevd": (2, pos(2, 435, 108, 42)),
    "qp": (2, pos(2, 523, 108, 42)),
    "tacc": (2, pos(2, 590, 108, 42)),
    "sp": (2, pos(2, 247, 125, 110, 12)),
    "pmedp": (2, pos(2, 390, 141, 42)),
    "scontp": (2, pos(2, 520, 141, 42)),
    "ip": (2, pos(2, 247, 156, 110, 12)),
    "phtp": (2, pos(2, 380, 156, 42)),
    "pdap": (2, pos(2, 510, 156, 42)),

    # Page 2 wall motion / RV / other
    "cinetica": (2, pos(2, 175, 169, 230, 12, "long")),
    "wmsi": (2, pos(2, 497, 424, 65)),
    "gls": (2, pos(2, 480, 455, 65)),
    "fac": (2, pos(2, 145, 508, 42)),
    "fevd": (2, pos(2, 255, 508, 42)),
    "tapse": (2, pos(2, 345, 508, 42)),
    "fdvd": (2, pos(2, 270, 524, 240, 12, "long")),
    "formatiuniatriale": (2, pos(2, 175, 553, 45)),
    "descformatiuniatriale": (2, pos(2, 245, 553, 330, 12, "long")),
    "formatiuniventriculare": (2, pos(2, 175, 568, 45)),
    "descformatiuniventriculare": (2, pos(2, 245, 568, 330, 12, "long")),
    "pericard": (2, pos(2, 208, 584, 75)),
    "cantitatepericard": (2, pos(2, 340, 584, 75)),
    "pericardant": (2, pos(2, 440, 584, 45)),
    "pericardpost": (2, pos(2, 540, 584, 45)),
    "aspectpericard": (2, pos(2, 180, 600, 400, 12, "long")),
    "vci": (2, pos(2, 250, 630, 45)),
    "colapsvci": (2, pos(2, 500, 630, 70)),
    "observatii": (2, pos(2, 35, 665, 540, 12, "multiline")),
    "concluzie": (2, pos(2, 35, 725, 540, 13, "multiline conclusion")),
    "medic": (2, pos(2, 500, 826, 90, 12)),
}


def field_html(key: str, value: str, spec: dict) -> str:
    if not value:
        return ""
    cls = "val " + spec.get("cls", "")
    style = (
        f"left:{spec['left']:.3f}%; top:{spec['top']:.3f}%; "
        f"width:{spec['width']:.3f}%; font-size:{spec['fs']}px;"
    )
    return f'<div class="{cls}" style="{style}">{html.escape(value)}</div>'


def render_protocol(data: dict) -> str:
    p1_fields = []
    p2_fields = []
    for key, value in data.items():
        if key not in FIELDS:
            continue
        page, spec = FIELDS[key]
        fragment = field_html(key, value, spec)
        if page == 1:
            p1_fields.append(fragment)
        else:
            p2_fields.append(fragment)

    css = """
    <style>
      body {
        margin: 0;
        background: #eeeeee;
        font-family: 'Times New Roman', Times, serif;
      }
      .toolbar {
        position: sticky;
        top: 0;
        z-index: 9999;
        background: #f7f7f7;
        border-bottom: 1px solid #ccc;
        padding: 10px;
        font-family: Arial, sans-serif;
        text-align: center;
      }
      .toolbar button {
        font-size: 15px;
        padding: 8px 14px;
        border: 1px solid #333;
        background: white;
        cursor: pointer;
      }
      .protocol {
        width: 794px;
        margin: 18px auto;
      }
      .page {
        position: relative;
        width: 794px;
        background: white;
        margin: 0 auto 28px auto;
        box-shadow: 0 0 10px rgba(0,0,0,0.25);
        page-break-after: always;
      }
      .page img.bg {
        display: block;
        width: 100%;
        height: auto;
      }
      .val {
        position: absolute;
        color: #000;
        font-family: 'Times New Roman', Times, serif;
        font-weight: bold;
        line-height: 1.05;
        white-space: pre-wrap;
        overflow: hidden;
      }
      .long {
        font-weight: bold;
      }
      .multiline {
        line-height: 1.25;
        height: 45px;
      }
      .conclusion {
        line-height: 1.35;
        height: 75px;
      }
      @media print {
        @page {
          size: A4 portrait;
          margin: 0;
        }
        html, body {
          margin: 0 !important;
          padding: 0 !important;
          background: white !important;
        }
        .toolbar {
          display: none !important;
        }
        .protocol {
          width: 210mm;
          margin: 0;
        }
        .page {
          width: 210mm;
          margin: 0;
          box-shadow: none;
          page-break-after: always;
          break-after: page;
        }
      }
    </style>
    """

    body = f"""
    <div class="toolbar">
      <button onclick="window.print()">🖨️ Imprimă protocolul</button>
      <span style="margin-left:12px;color:#555;">Verifică valorile înainte de printare.</span>
    </div>
    <div class="protocol">
      <div class="page">
        <img class="bg" src="data:image/png;base64,{PAGE1_B64}">
        {''.join(p1_fields)}
      </div>
      <div class="page">
        <img class="bg" src="data:image/png;base64,{PAGE2_B64}">
        {''.join(p2_fields)}
      </div>
    </div>
    """
    return "<!doctype html><html><head><meta charset='utf-8'>" + css + "</head><body>" + body + "</body></html>"


# ----- UI -----
st.title("Protocol ecocardiografie ECHOTIM imprimabil")
st.caption("Lipești aceeași linie de tip `cheie=valoare; cheie=valoare`, iar aplicația completează protocolul scanat și îl pregătește pentru print.")

query_data = ""
try:
    # Streamlit >= 1.30
    query_data = st.query_params.get("data", "")
except Exception:
    query_data = st.experimental_get_query_params().get("data", [""])[0]

query_data = unquote_plus(query_data or "")

example = (
    "data=23.05.2026;nume=Popescu;prenume=Ion;varsta=71;salon=USIC;"
    "aoinel=2.1;aoasc=3.4;dao=1.8;as=4.0;vd=2.8;siv=1.1;dtdvs=5.2;dtsvs=3.4;"
    "ppvs=1.0;fevs=60;functiediastolica=Normala;im=I;ia=Nu;it=I;tapse=22;paps=30;"
    "vci=1.8;concluzie=FEVS pastrata. Fara valvulopatii semnificative."
)

with st.sidebar:
    st.header("Date pentru autofill")
    st.write("Format acceptat:")
    st.code("aoinel=2.1;aoasc=3.4;fevs=60;im=I;ia=Nu;it=I;tapse=22;paps=30", language="text")
    st.write("Acceptă și coduri HIPOCRATE directe:")
    st.code("v238=2.1;v239=3.4;v256=60;v273=I;v291=Nu;v302=I", language="text")
    st.divider()
    st.subheader("Bookmarklet pentru protocol")
    st.write("După publicare, înlocuiește `URL_STREAMLIT` cu adresa aplicației tale.")
    bookmarklet = "javascript:(function(){var u='URL_STREAMLIT';var x=prompt('Lipeste valori pentru protocol','aoinel=2.1;aoasc=3.4;fevs=60;im=I;ia=Nu;it=I');if(x)location.href=u+'?data='+encodeURIComponent(x);})();"
    st.code(bookmarklet, language="javascript")

data_text = st.text_area(
    "Date de completat",
    value=query_data or example,
    height=140,
    help="Poți lipi valori separate prin punct și virgulă sau câte una pe rând.",
)

parsed = parse_pairs(data_text)

col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    st.metric("Câmpuri recunoscute", len(parsed))
with col2:
    unknown = []
    for raw in re.split(r"[;\n]+", data_text):
        raw = raw.strip()
        if not raw or ("=" not in raw and ":" not in raw):
            continue
        key = raw.split("=", 1)[0] if "=" in raw else raw.split(":", 1)[0]
        ck = canonical_key(key)
        if ck and ck not in FIELDS:
            unknown.append(key.strip())
    st.metric("Câmpuri nepoziționate", len(unknown))
with col3:
    if unknown:
        st.warning("Chei citite, dar fără poziție pe protocol: " + ", ".join(unknown[:12]) + ("..." if len(unknown) > 12 else ""))

protocol_html = render_protocol(parsed)

components.html(protocol_html, height=2380, scrolling=True)

st.download_button(
    "Descarcă protocolul ca HTML",
    data=protocol_html,
    file_name="protocol_ecocardiografie.html",
    mime="text/html",
)

st.info("Pentru print fidel: în dialogul de print, alege A4, Portrait, Scale 100%, Margins: None/Minimum și activează Background graphics dacă browserul cere asta.")
