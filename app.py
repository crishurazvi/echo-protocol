
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
    page_title="Protocol ecocardiografie interactiv",
    page_icon="🫀",
    layout="wide",
)


def asset_b64(name: str) -> str:
    return base64.b64encode((ASSETS / name).read_bytes()).decode("ascii")


CINETICA_B64 = asset_b64("cinetica.png")


def norm_key(s: str) -> str:
    s = str(s or "").strip().lower()
    s = s.translate(str.maketrans({
        "ă": "a", "â": "a", "î": "i", "ș": "s", "ş": "s", "ț": "t", "ţ": "t",
    }))
    return re.sub(r"[^a-z0-9]+", "", s)


ALIASES = {
    # admin
    "data": "data_exam", "dataexaminarii": "data_exam", "nume": "nume", "prenume": "prenume",
    "varsta": "varsta", "salon": "salon", "inaltime": "inaltime", "greutate": "greutate",
    "scorp": "scorp", "scorporala": "scorp", "calitate": "calitate", "ritm": "ritm",
    "fc": "fc", "frecventa": "fc", "ta": "ta", "tas": "ta", "tensiune": "ta",

    # parasternal
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
    "fs": "fs", "mpsiv": "mpsiv", "miscareparadoxalasiv": "mpsiv",
    "feteich": "feteich", "feteichholtz": "feteich",
    "masavs": "masavs", "vm": "vm", "valvamitrala": "vm", "aspectvalvamitral": "vm",

    # apical
    "vtd": "vtd", "vtdidx": "vtdidx", "vts": "vts", "vtsidx": "vtsidx",
    "fe": "fevs", "fevs": "fevs", "ef": "fevs", "lvef": "fevs",
    "feplanimetric": "fevs", "feplanimetrica": "fevs",
    "suprafas": "suprafas", "laarea": "suprafas", "volas": "volas",
    "lavi": "volasidx", "volasidx": "volasidx", "mapse": "mapse",
    "dvs": "dvs", "dvd": "dvd", "dad": "dad", "das": "das",
    "fe2c": "fe2c", "fe2camere": "fe2c",
    "fd": "functiediastolica", "functiediastolica": "functiediastolica",

    # mitral
    "e": "e", "emitral": "e", "a": "a", "amitral": "a",
    "durataa": "durataa", "ea": "ea", "tde": "tde", "triv": "triv", "vp": "vp",
    "sprimlat": "sprimlat", "slat": "sprimlat", "elat": "elat", "alat": "alat",
    "sprimsiv": "sprimsiv", "ssiv": "sprimsiv", "esiv": "esiv", "asiv": "asiv", "ee": "ee",
    "sm": "sm", "stenozamitrala": "sm", "pmmitral": "pmmitral", "pmedmitral": "pmmitral",
    "phtmitral": "phtmitral", "sphtmitral": "sphtmitral", "smitral": "smitral",
    "splanmitral": "splanmitral", "spisamitral": "spisamitral", "sfcontmitral": "sfcontmitral",
    "im": "im", "mr": "im", "insuficientamitrala": "im", "sorim": "sorim",
    "eroa": "sorim", "vrim": "vrim", "frim": "frim", "vcim": "vcim", "dpdt": "dpdt",
    "vps": "vps", "vpd": "vpd", "vpsd": "vpsd", "duratara": "duratara",

    # aortic
    "vmaxao": "vmaxao", "vaovmax": "vmaxao", "pmaxao": "pmaxao", "itvao": "itvao",
    "tevs": "tevs", "qao": "qao", "qs": "qao",
    "sa": "sa", "stenozaao": "sa", "stenozaaortica": "sa",
    "pmedao": "pmedao", "scontao": "scontao", "splanao": "splanao",
    "ia": "ia", "ar": "ia", "insuficientaaortica": "ia",
    "phtao": "phtao", "soria": "soria", "vria": "vria", "fria": "fria", "vcia": "vcia",
    "aortadesc": "aortadesc",

    # tricuspid
    "et": "et", "etricusp": "et", "atricusp": "atricusp", "stricusp": "stricusp",
    "eprimtricuspid": "eprimtricuspid", "aprimtricuspid": "aprimtricuspid",
    "eetricuspid": "eetricuspid",
    "st": "st", "stenozatricuspidiana": "st", "pmedt": "pmedt", "phtt": "phtt", "sphtt": "sphtt",
    "it": "it", "tr": "it", "insuficientatricuspidiana": "it",
    "vmaxtr": "vmaxtr", "pmaxt": "pmaxt", "paps": "paps", "psap": "paps",

    # pulmonary
    "vmaxp": "vmaxp", "pmaxp": "pmaxp", "itvp": "itvp", "tevd": "tevd",
    "qp": "qp", "tacc": "tacc", "sp": "sp", "stenozapulmonara": "sp",
    "pmedp": "pmedp", "scontp": "scontp", "ip": "ip", "insuficientapulmonara": "ip",
    "phtp": "phtp", "pdap": "pdap",

    # page 2
    "cinetica": "cinetica", "wallmotion": "cinetica", "wmsi": "wmsi", "scorwmsi": "wmsi",
    "gls": "gls", "fac": "fac", "fevd": "fevd", "tapse": "tapse",
    "fdvd": "fdvd", "functiediastolicavd": "fdvd",
    "formatiuniatriale": "formatiuniatriale", "descformatiuniatriale": "descformatiuniatriale",
    "formatiuniventriculare": "formatiuniventriculare", "descformatiuniventriculare": "descformatiuniventriculare",
    "pericard": "pericard", "lichidpericardic": "pericard", "cantitatepericard": "cantitatepericard",
    "pericardant": "pericardant", "pericardpost": "pericardpost", "aspectpericard": "aspectpericard",
    "vci": "vci", "diamvci": "vci", "ivc": "vci", "colapsvci": "colapsvci",
    "observatii": "observatii", "altemasuratori": "observatii",
    "concluzie": "concluzie", "concluzii": "concluzie", "medic": "medic", "examinator": "medic",
}

# HIPOCRATE -> protocol keys
HIPO = {
    "v214": "concluzie",
    "v238": "aoinel", "v239": "aoasc", "v240": "dao", "v241": "va", "v242": "as",
    "v243": "vd", "v244": "peretevd", "v245": "siv", "v246": "dtdvs", "v247": "dtsvs",
    "v248": "ppvs", "v249": "fs", "v250": "mpsiv", "v251": "feteich", "v252": "masavs",
    "v253": "vm", "v254": "vtd", "v255": "vts", "v256": "fevs", "v257": "suprafas",
    "v258": "volas", "v259": "functiediastolica", "v260": "e", "v261": "a",
    "v262": "eprim", "v263": "aprim", "v264": "sprim", "v265": "sm", "v266": "pmmitral",
    "v268": "phtmitral", "v271": "smitral", "v272": "splanmitral", "v273": "im",
    "v275": "sorim", "v276": "vrim", "v277": "vcim", "v278": "vps", "v279": "vpd",
    "v280": "imra", "v281": "vmaxao", "v282": "pmaxao", "v283": "itvao", "v284": "tevs",
    "v285": "qao", "v287": "sa", "v288": "pmedao", "v289": "scontao", "v290": "splanao",
    "v291": "ia", "v292": "phtao", "v293": "soria", "v294": "vria", "v295": "vcia",
    "v296": "aortadesc", "v297": "et", "v298": "atricusp", "v299": "st", "v300": "pmedt",
    "v301": "phtt", "v302": "it", "v303": "pmaxt", "v304": "paps", "v305": "vmaxp",
    "v306": "pmaxp", "v307": "itvp", "v308": "qp", "v309": "tacc", "v310": "sp",
    "v311": "pmedp", "v312": "ip", "v313": "cinetica", "v314": "wmsi", "v315": "formatiuniatriale",
    "v316": "formatiuniventriculare", "v317": "pericard", "v318": "pericardant",
    "v319": "pericardpost", "v320": "vci", "v321": "colapsvci", "v322": "medic",
    "v323": "mapse", "v324": "tapse",
}


def canonical_key(raw_key: str) -> str:
    k = norm_key(raw_key)
    if not k:
        return ""
    if k in HIPO:
        return HIPO[k]
    if re.fullmatch(r"\d+", k):
        return HIPO.get("v" + k, "v" + k)
    return ALIASES.get(k, k)


def parse_pairs(text: str) -> dict:
    data = {}
    if not text:
        return data

    for chunk in re.split(r"[;\n]+", text):
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


def get(data: dict, key: str) -> str:
    return str(data.get(key, ""))


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def inp(data: dict, key: str, w: str = "42px", cls: str = "", ph: str = "") -> str:
    return f'<input class="line {cls}" name="{esc(key)}" value="{esc(get(data, key))}" placeholder="{esc(ph)}" style="width:{w};">'


def area(data: dict, key: str, rows: int = 2, cls: str = "") -> str:
    return f'<textarea class="line area {cls}" name="{esc(key)}" rows="{rows}">{esc(get(data, key))}</textarea>'


def checked(data: dict, key: str, expected: str) -> str:
    value = norm_key(get(data, key))
    exp = norm_key(expected)
    if not value:
        return ""
    if value == exp or value.startswith(exp) or exp.startswith(value):
        return "checked"
    return ""


def cb(data: dict, key: str, expected: str) -> str:
    return f'<input type="checkbox" {checked(data, key, expected)}>'


def severity(data: dict, key: str, w: str = "115px") -> str:
    return inp(data, key, w)


def render_protocol(data: dict) -> str:
    css = """
    <style>
    :root {
      --fs: 10.6pt;
      --line: #111;
    }
    html, body {
      margin: 0;
      padding: 0;
      background: #e9e9e9;
      font-family: "Times New Roman", Times, serif;
      color: #000;
    }
    .toolbar {
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 10px;
      background: #f7f7f7;
      border-bottom: 1px solid #ccc;
      font-family: Arial, sans-serif;
      text-align: center;
    }
    .toolbar button {
      padding: 8px 14px;
      font-size: 15px;
      cursor: pointer;
      background: white;
      border: 1px solid #333;
      border-radius: 4px;
    }
    .page {
      width: 210mm;
      height: 297mm;
      box-sizing: border-box;
      background: white;
      margin: 16px auto;
      padding: 9mm 10mm 8mm 10mm;
      box-shadow: 0 0 10px rgba(0,0,0,.22);
      page-break-after: always;
      overflow: hidden;
      font-size: var(--fs);
      line-height: 1.12;
    }
    .header {
      display: grid;
      grid-template-columns: 1fr 1fr;
      column-gap: 12mm;
      align-items: start;
      margin-bottom: 5mm;
      font-size: 9.2pt;
      line-height: 1.08;
    }
    .logo-line {
      font-size: 9pt;
      font-weight: bold;
      letter-spacing: .2px;
      margin-bottom: 2mm;
    }
    .eacvi {
      text-align: right;
      font-size: 23pt;
      font-weight: bold;
      letter-spacing: .5px;
      line-height: 1;
    }
    .eacvi-small {
      text-align: right;
      font-size: 8.5pt;
      font-weight: bold;
      margin-top: 5mm;
    }
    h1 {
      text-align: center;
      font-size: 15pt;
      margin: 2mm 0 3mm 0;
      line-height: 1;
    }
    .row {
      margin: 1.1mm 0;
      display: flex;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 1.6mm;
    }
    .section {
      margin-top: 3.2mm;
      font-weight: bold;
    }
    .line {
      border: 0;
      border-bottom: 1px solid var(--line);
      font-family: "Times New Roman", Times, serif;
      font-size: var(--fs);
      padding: 0 1mm;
      height: 4mm;
      line-height: 4mm;
      outline: none;
      background: transparent;
      box-sizing: border-box;
    }
    .line:focus {
      background: #fff8d8;
    }
    .area {
      height: auto;
      resize: vertical;
      line-height: 1.2;
      vertical-align: top;
    }
    input[type="checkbox"] {
      width: 3.2mm;
      height: 3.2mm;
      margin: 0 .8mm 0 .8mm;
      vertical-align: -1px;
      accent-color: black;
    }
    .small {
      font-size: 9.1pt;
    }
    .tiny {
      font-size: 8.5pt;
    }
    .two-col {
      display: grid;
      grid-template-columns: 1fr 31mm;
      column-gap: 4mm;
      align-items: start;
    }
    .right-mini .row {
      margin: 1.25mm 0;
    }
    .cinetica-wrap0 {
      display: grid;
      grid-template-columns: 1fr 45mm;
      column-gap: 6mm;
      align-items: start;
      margin-top: 3mm;
    }
    .cinetica-img {
      width: 80%;
      display: block;
      align: center;
    }
    .blank-wide {
      flex: 1;
      min-width: 80mm;
    }
    .signature {
      text-align: right;
      margin-top: 8mm;
      font-weight: bold;
    }
    .footer-space {
      height: 2mm;
    }
    @media print {
      @page {
        size: A4 portrait;
        margin: 0;
      }
      html, body {
        background: white !important;
        margin: 0 !important;
        padding: 0 !important;
      }
      .toolbar {
        display: none !important;
      }
      .page {
        margin: 0 !important;
        box-shadow: none !important;
        width: 210mm;
        height: 297mm;
        padding: 9mm 10mm 8mm 10mm;
      }
      .line {
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
      }
      input::placeholder {
        color: transparent;
      }
      textarea::placeholder {
        color: transparent;
      }
    }
    </style>
    """

    p1 = f"""
    <section class="page">
      <div class="header">
        <div>
          <div class="logo-line">INSTITUTUL DE BOLI CARDIOVASCULARE</div>
          <div><b>Timișoara, str Gh Adam 13 A</b></div>
          <div>Timișoara, cod 300310</div>
          <div>Tel 0256207355; Fax 0256207362</div>
          <div><b>LABORATOR DE ECOCARDIOGRAFIE ECHOTIM</b></div>
          <div>Coordonator prof dr Adina Ionac</div>
        </div>
        <div>
          <div class="eacvi">EACVI</div>
          <div class="eacvi-small">acreditare europeană 2012, re-acreditare 2022</div>
        </div>
      </div>

      <h1>ECOCARDIOGRAFIE TRANSTORACICĂ</h1>

      <div class="row">
        Data examinării {inp(data, "data_exam", "31mm")}
      </div>
      <div class="row">
        Nume {inp(data, "nume", "40mm")}
        Prenume {inp(data, "prenume", "25mm")}
        Vârstă {inp(data, "varsta", "12mm")} ani,
        salon {inp(data, "salon", "16mm")}
      </div>
      <div class="row">
        Înălțime {inp(data, "inaltime", "10mm")} cm,
        Greutate {inp(data, "greutate", "10mm")} kg,
        S<sub>corporală</sub> {inp(data, "scorp", "8mm")} m²;
        Calitate imagine: bună {cb(data, "calitate", "buna")}
        satisfăcătoare {cb(data, "calitate", "satisfacatoare")}
        slabă {cb(data, "calitate", "slaba")}
      </div>
      <div class="row">
        Ritm sinusal {cb(data, "ritm", "sinusal")}
        Fibrilație atrială {cb(data, "ritm", "fibrilatie")}
        Ritm electrostimulat {cb(data, "ritm", "electrostimulat")}
        {inp(data, "fc", "10mm")} b/min
        {inp(data, "ta", "15mm")} mmHg
      </div>

      <div class="section">Incidența parasternală:
        <span style="font-weight:normal">mod M {cb(data, "mod", "m")} 2D {cb(data, "mod", "2d")}</span>
      </div>
      <div class="row">
        Ao la inel {inp(data, "aoinel")} cm (2.2-3.7 cm),
        Ao ascendentă {inp(data, "aoasc")} cm (2,1-3,4cm),
        Ao la sinusuri Valsalva {inp(data, "sinusvals")} cm
      </div>
      <div class="row">
        Deschidere v ao {inp(data, "dao")} cm (&gt;1,6 cm),
      </div>
      <div class="row">
        Aspectul valvei aortice: normal {cb(data, "va", "normal")}
        patologic: {inp(data, "va", "18mm")}
      </div>
      <div class="row">
        Diam AS {inp(data, "as")} cm (F: 2,7-3,8 cm, B:3-4 cm, &lt; 2,3 cm/m²),
      </div>
      <div class="row">
        Diam VD {inp(data, "vd")} cm (2.5-2.9 cm),
        perete ant VD {inp(data, "peretevd", "14mm")} mm (&lt;5 mm)
      </div>
      <div class="row">
        SIV {inp(data, "siv")} cm (F:0.6-0.9 cm; B: 0.6-1 cm)
        mișcare paradoxală SIV da {cb(data, "mpsiv", "da")} nu {cb(data, "mpsiv", "nu")}
      </div>
      <div class="row">
        DTDVS {inp(data, "dtdvs")} cm (F &lt;5.3cm, B&lt;5.9 cm; F:2.4-3.2 cm/m²; B:2.2-3.1 cm/m²)
      </div>
      <div class="row">
        DTSVS {inp(data, "dtsvs")} cm
      </div>
      <div class="row">
        PPVS {inp(data, "ppvs")} cm (F:0.6-0.9 cm; B: 0.6-1 cm)
      </div>
      <div class="row">
        FS {inp(data, "fs")} % (25-45%)
        Masa VS {inp(data, "masavs", "27mm")} g (F 43-95 g/m²; B: 49 – 115 g/m²)
      </div>
      <div class="row">
        Aspectul valvei mitrale: normal {cb(data, "vm", "normal")}
        patologic: {inp(data, "vm", "29mm")}
      </div>

      <div class="two-col">
        <div>
          <div class="section">Apical 4 camere:</div>
          <div class="row">VTD {inp(data, "vtd")} ml, {inp(data, "vtdidx")} ml/m² (F: 56-104 ml; B:67-155ml; 35-75 ml/m²)</div>
          <div class="row">VTS {inp(data, "vts")} ml, {inp(data, "vtsidx")} ml/m² (F: 19-49 ml; M:22-58ml; 12-30 ml/m²)</div>
          <div class="row">FE planimetric {inp(data, "fevs")} % (&gt;55%)</div>
          <div class="row">Supraf AS {inp(data, "suprafas")} cm² (&lt;20 cm²), Vol AS {inp(data, "volas")} ml, {inp(data, "volasidx", "22mm")} ml/m² (&lt;34 ml/m²)</div>
          <div class="row">MAPSE {inp(data, "mapse")} mm (&gt;10mm)</div>
        </div>
        <div class="right-mini">
          <div class="row">dVS: {inp(data, "dvs", "7mm")} cm</div>
          <div class="row">dVD: {inp(data, "dvd", "7mm")} cm</div>
          <div class="row">dAD: {inp(data, "dad", "7mm")} cm</div>
          <div class="row">dAS: {inp(data, "das", "7mm")} cm</div>
        </div>
      </div>

      <div class="section">Apical 2 camere:</div>
      <div class="row">FE planimetric: {inp(data, "fe2c", "23mm")} % (&gt;55%)</div>
      <div class="row">
        Funcție diastolică VS: normală {cb(data, "functiediastolica", "normala")}
        disfuncție diastolică
        tip I {cb(data, "functiediastolica", "tipi")}
        tip II {cb(data, "functiediastolica", "tipii")}
        tip III {cb(data, "functiediastolica", "tipiii")}
        tip IV {cb(data, "functiediastolica", "tipiv")}
      </div>

      <div class="section">Flux mitral:</div>
      <div class="row">
        E {inp(data, "e")} cm/s, A {inp(data, "a")} cm/s,
        durata A {inp(data, "durataa")} msec, E/A {inp(data, "ea")},
        TDE {inp(data, "tde")} msec (160-240msec),
      </div>
      <div class="row">
        TRIV {inp(data, "triv")} msec (60-90msec),
        Vp {inp(data, "vp")} cm/s (&gt;45cm/s)
      </div>
      <div class="row">
        Doppler tisular: lateral:
        S′ {inp(data, "sprimlat")} cm/s (&gt;7,5cm/s),
        E′ {inp(data, "elat")} cm/s (&gt;10cm/s),
        A′ {inp(data, "alat")} cm/s,
      </div>
      <div class="row">
        SIV:
        S′ {inp(data, "sprimsiv")} cm/s (&gt;7,5cm/s),
        E′ {inp(data, "esiv")} cm/s (&gt;7cm/s),
        A′ {inp(data, "asiv")} cm/s,
        E/E′ {inp(data, "ee")}
      </div>
      <div class="row">
        Stenoză mitrală: nu {cb(data, "sm", "nu")} da {cb(data, "sm", "da")}
        severitate: {severity(data, "sm", "36mm")}
      </div>
      <div class="row">
        Pmed {inp(data, "pmmitral")} mmHg, PHT {inp(data, "phtmitral")} msec,
        S<sub>PHT</sub> {inp(data, "sphtmitral")} cm²,
        S<sub>planimetric</sub> {inp(data, "splanmitral")} cm²,
        S<sub>PISA</sub> {inp(data, "spisamitral")} cm²,
        S<sub>fr cont</sub> {inp(data, "sfcontmitral")} cm²
      </div>
      <div class="row">
        Insuficiență mitrală: nu {cb(data, "im", "nu")} da {cb(data, "im", "da")}
        severitate: {severity(data, "im", "37mm")}
      </div>
      <div class="row">
        SOR {inp(data, "sorim")} mm², VR {inp(data, "vrim")} ml, FR {inp(data, "frim")} %,
        VC {inp(data, "vcim")} mm, dp/dt {inp(data, "dpdt", "25mm")} mmHg/s (&gt;1200mmHg/s)
      </div>
      <div class="row">
        Flux vene pulmonare: S {inp(data, "vps")} cm/s, D {inp(data, "vpd")} cm/s,
        S/D {inp(data, "vpsd")}, durata RA {inp(data, "duratara")} msec
      </div>

      <div class="section">Flux aortic:</div>
      <div class="row">
        Vmax {inp(data, "vmaxao")} cm/s, Pmax {inp(data, "pmaxao")} mmHg,
        ITV {inp(data, "itvao")} cm (&gt;18cm), TEVS {inp(data, "tevs")} cm,
        Qs {inp(data, "qao")} l/m
      </div>
      <div class="row">
        Stenoza aortică: nu {cb(data, "sa", "nu")} da {cb(data, "sa", "da")}
        severitate: {severity(data, "sa", "34mm")}
      </div>
      <div class="row">
        Pmed {inp(data, "pmedao")} mmHg, S<sub>fr cont</sub> {inp(data, "scontao")} cm²,
        S<sub>plan</sub> {inp(data, "splanao")} cm²,
      </div>
      <div class="row">
        Insuficiență aortică: nu {cb(data, "ia", "nu")} da {cb(data, "ia", "da")}
        severitate: {severity(data, "ia", "34mm")}
      </div>
      <div class="row">
        PHT {inp(data, "phtao")} ms, SOR {inp(data, "soria")} mm², VR {inp(data, "vria")} ml,
        FR {inp(data, "fria")} %, vc {inp(data, "vcia")} mm,
        Vtd aorta desc {inp(data, "aortadesc")} cm/s,
      </div>
    </section>
    """

    p2 = f"""
    <section class="page">
      <div class="section">Flux tricuspidian:</div>
      <div class="row">
        E {inp(data, "et")} cm/s, A {inp(data, "atricusp")} cm/s,
        S′ {inp(data, "stricusp")} cm/s (&gt;9,5cm/s),
        E′ {inp(data, "eprimtricuspid")} cm/s,
        A′ {inp(data, "aprimtricuspid")} cm/s,
        E/E′ {inp(data, "eetricuspid")}
      </div>
      <div class="row">
        Stenoza tricuspidiană: nu {cb(data, "st", "nu")} da {cb(data, "st", "da")}
        severitate: {severity(data, "st", "17mm")}
      </div>
      <div class="row">
        Pmed {inp(data, "pmedt")} mmHg, PHT {inp(data, "phtt")} ms,
        S<sub>PHT</sub> {inp(data, "sphtt")} cm²,
      </div>
      <div class="row">
        Insuficiență tricuspidiană: nu {cb(data, "it", "nu")} da {cb(data, "it", "da")}
        severitate {severity(data, "it", "16mm")}
        Vmax {inp(data, "vmaxtr")} cm/s,
        Pmax {inp(data, "pmaxt")} mmHg,
        PSAP {inp(data, "paps")} mmHg
      </div>

      <div class="section">Flux pulmonar:</div>
      <div class="row">
        Vmax {inp(data, "vmaxp")} cm/s, Pmax {inp(data, "pmaxp")} mmHg,
        ITV {inp(data, "itvp")} cm, TEVD {inp(data, "tevd")} cm,
        Qp {inp(data, "qp")} l/m,
        Timp accel {inp(data, "tacc")} ms
      </div>
      <div class="row">
        Stenoza pulmonară: nu {cb(data, "sp", "nu")} da {cb(data, "sp", "da")}
        severitate: {severity(data, "sp", "17mm")}
        Pmed {inp(data, "pmedp")} mmHg,
        Scont {inp(data, "scontp")} cm²,
      </div>
      <div class="row">
        Insuficiența pulmonară: nu {cb(data, "ip", "nu")} da {cb(data, "ip", "da")}
        severitate: {severity(data, "ip", "17mm")}
        PHT {inp(data, "phtp")} ms,
        PDAP {inp(data, "pdap")} mmHg
      </div>

      <div class="row" style="margin-top:4mm;">
        Cinetica parietală:
        normală {cb(data, "cinetica", "normala")}
        anomalii de cinetică parietală {cb(data, "cinetica", "anomalii")}
      </div>

      <div class="cinetica-wrap">
        <div>
          <img class="cinetica-img" src="data:image/png;base64,{CINETICA_B64}">
        </div>
        
      </div>

      <div class="row" style="margin-top:5mm;">
        Funcția sistolică VD: FAC {inp(data, "fac")} % (&gt;35%),
        FE {inp(data, "fevd")} %,
        TAPSE {inp(data, "tapse")} mm (&gt;17mm)
      </div>
      <div class="row">
        Funcție diastolică VD:
        normală {cb(data, "fdvd", "normala")}
        disfuncție diastolică
        tip I {cb(data, "fdvd", "tipi")}
        tip II {cb(data, "fdvd", "tipii")}
        tip III {cb(data, "fdvd", "tipiii")}
        tip IV {cb(data, "fdvd", "tipiv")}
      </div>

      <div class="row" style="margin-top:6mm;">
        Formațiuni intratriale: nu {cb(data, "formatiuniatriale", "nu")} da {cb(data, "formatiuniatriale", "da")}
        descriere {inp(data, "descformatiuniatriale", "12mm")}
      </div>
      <div class="row">
        Formațiuni intraventriculare: nu {cb(data, "formatiuniventriculare", "nu")} da {cb(data, "formatiuniventriculare", "da")}
        descriere {inp(data, "descformatiuniventriculare", "10mm")}
      </div>
      <div class="row">
        Lichid pericardic: absent {cb(data, "pericard", "absent")}
        prezent {cb(data, "pericard", "prezent")}
        cantitate {inp(data, "cantitatepericard", "13mm")}
        anterior {inp(data, "pericardant", "18mm")} cm,
        posterior {inp(data, "pericardpost", "18mm")} cm
      </div>
      <div class="row">
        Aspect pericard: normal {cb(data, "aspectpericard", "normal")}
        patologic: {inp(data, "aspectpericard", "28mm")}
      </div>

      <div class="section">Flux vena cava inferioară:</div>
      <div class="row">
        S/ {inp(data, "vcis", "20mm")}
        diametru VCI: {inp(data, "vci", "22mm")} cm,
        variabilitate cu respirația:
        nu {cb(data, "colapsvci", "nu")}
        da {cb(data, "colapsvci", "da")}
      </div>

      <div style="margin-top:2mm;">
        Observații, alte măsurători<br>
        {area(data, "observatii", 3)}
      </div>

      <div style="margin-top:2mm;">
        <b>Concluzie</b><br>
        {area(data, "concluzie", 4, "conclusion", "133mm")}
      </div>

      <div class="signature">Medic examinator<br>{inp(data, "medic", "45mm")}</div>
    </section>
    """

    js = """
    <script>
      function printProtocol() {
        window.print();
      }
    </script>
    """

    toolbar = """
    <div class="toolbar">
      <button onclick="printProtocol()">🖨️ Imprimă protocolul</button>
      <span style="margin-left:12px;color:#555;">Poți edita direct câmpurile înainte de print.</span>
    </div>
    """

    return "<!doctype html><html><head><meta charset='utf-8'>" + css + "</head><body>" + js + toolbar + p1 + p2 + "</body></html>"


# Query param, for bookmarklet workflow
try:
    query_data = st.query_params.get("data", "")
except Exception:
    query_data = st.experimental_get_query_params().get("data", [""])[0]
query_data = unquote_plus(query_data or "")

example = (
    "data=23.05.2026;nume=Popescu;prenume=Ion;varsta=71;salon=;"
    "aoinel=2.1;aoasc=3.4;dao=1.8;as=4.0;vd=2.8;siv=1.1;dtdvs=5.2;"
    "dtsvs=3.4;ppvs=1.0;fevs=60;functiediastolica=Normala;im=I;ia=Nu;it=I;"
    "tapse=22;paps=30;vci=1.8;cinetica=normala;pericard=absent;"
    "concluzie="
)

st.title("Protocol ecocardiografie interactiv")
st.caption("Formular HTML imprimabil, fără fundal PDF. Datele se pot trimite prin bookmarklet sau lipi manual.")

with st.sidebar:
    st.header("Date autofill")
    st.write("Format:")
    st.code("aoinel=2.1;aoasc=3.4;fevs=60;im=I;ia=Nu;it=I", language="text")
    st.write("Acceptă și coduri HIPOCRATE:")
    st.code("v238=2.1;v239=3.4;v256=60;v273=I;v291=Nu;v302=I", language="text")
    st.divider()
    st.subheader("Bookmarklet")
    st.write("După deploy, înlocuiește `URL_STREAMLIT` cu adresa aplicației.")
    bookmarklet = (
        "javascript:(function(){var u='URL_STREAMLIT';"
        "var x=prompt('Lipeste valori pentru protocol','aoinel=2.1;aoasc=3.4;fevs=60;im=I;ia=Nu;it=I');"
        "if(x)location.href=u+'?data='+encodeURIComponent(x);})();"
    )
    st.code(bookmarklet, language="javascript")

data_text = st.text_area(
    "Date de completat",
    value=query_data or example,
    height=130,
)

parsed = parse_pairs(data_text)

raw_keys = []
unknown = []
for raw in re.split(r"[;\n]+", data_text):
    raw = raw.strip()
    if not raw or ("=" not in raw and ":" not in raw):
        continue
    key = raw.split("=", 1)[0] if "=" in raw else raw.split(":", 1)[0]
    ck = canonical_key(key)
    raw_keys.append(ck)
    # We accept many keys, but not every unknown has visible field in this draft.
    visible = ck in {
        "data_exam","nume","prenume","varsta","salon","inaltime","greutate","scorp","calitate","ritm","fc","ta",
        "aoinel","aoasc","sinusvals","dao","va","as","vd","peretevd","siv","mpsiv","dtdvs","dtsvs","ppvs","fs","masavs","vm",
        "vtd","vtdidx","vts","vtsidx","fevs","suprafas","volas","volasidx","mapse","dvs","dvd","dad","das","fe2c","functiediastolica",
        "e","a","durataa","ea","tde","triv","vp","sprimlat","elat","alat","sprimsiv","esiv","asiv","ee",
        "sm","pmmitral","phtmitral","sphtmitral","splanmitral","spisamitral","sfcontmitral","im","sorim","vrim","frim","vcim","dpdt",
        "vps","vpd","vpsd","duratara","vmaxao","pmaxao","itvao","tevs","qao","sa","pmedao","scontao","splanao","ia","phtao","soria","vria","fria","vcia","aortadesc",
        "et","atricusp","stricusp","eprimtricuspid","aprimtricuspid","eetricuspid","st","pmedt","phtt","sphtt","it","vmaxtr","pmaxt","paps",
        "vmaxp","pmaxp","itvp","tevd","qp","tacc","sp","pmedp","scontp","ip","phtp","pdap","cinetica","wmsi","gls",
        "fac","fevd","tapse","fdvd","formatiuniatriale","descformatiuniatriale","formatiuniventriculare","descformatiuniventriculare",
        "pericard","cantitatepericard","pericardant","pericardpost","aspectpericard","vcis","vci","colapsvci","observatii","concluzie","medic"
    }
    if ck and not visible:
        unknown.append(key.strip())

c1, c2, c3 = st.columns([1, 1, 3])
c1.metric("Câmpuri citite", len(parsed))
c2.metric("Nepuse în formular", len(unknown))
if unknown:
    c3.warning("Chei citite, dar încă fără poziționare explicită: " + ", ".join(unknown[:14]))

html_doc = render_protocol(parsed)
components.html(html_doc, height=2350, scrolling=True)

st.download_button(
    "Descarcă formularul HTML",
    data=html_doc,
    file_name="protocol_ecocardiografie_interactiv.html",
    mime="text/html",
)

st.info("La print: A4, Portrait, Scale 100%, Margins: None/Minimum. Dacă ceva nu se aliniază, ajustarea se face în CSS-ul din `app.py`, nu pe o imagine de fundal.")
