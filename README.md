
# Protocol ecocardiografie ECHOTIM, Streamlit

Aplicație Streamlit pentru completarea și imprimarea protocolului de ecocardiografie pe baza unei linii de date de tip:

```text
aoinel=2.1;aoasc=3.4;dao=1.8;fevs=60;im=I;ia=Nu;it=I;tapse=22;paps=30
```

Acceptă și coduri HIPOCRATE directe:

```text
v238=2.1;v239=3.4;v256=60;v273=I;v291=Nu;v302=I
```

## Structură

```text
app.py
requirements.txt
.streamlit/config.toml
assets/protocol_page1.png
assets/protocol_page2.png
assets/cinetica_parietala.png
```

## Publicare pe Streamlit Community Cloud

1. Creează un repository GitHub.
2. Încarcă toate fișierele din acest folder.
3. Intră pe Streamlit Community Cloud.
4. New app → selectezi repo-ul.
5. Main file path: `app.py`.
6. Deploy.

## Bookmarklet pentru protocol

După ce aplicația este publicată, înlocuiește `URL_STREAMLIT` cu URL-ul real al aplicației tale:

```javascript
javascript:(function(){var u='URL_STREAMLIT';var x=prompt('Lipeste valori pentru protocol','aoinel=2.1;aoasc=3.4;fevs=60;im=I;ia=Nu;it=I');if(x)location.href=u+'?data='+encodeURIComponent(x);})();
```

Exemplu:

```javascript
javascript:(function(){var u='https://protocol-eco.streamlit.app/';var x=prompt('Lipeste valori pentru protocol','aoinel=2.1;aoasc=3.4;fevs=60;im=I;ia=Nu;it=I');if(x)location.href=u+'?data='+encodeURIComponent(x);})();
```

## Prompt AI/OCR recomandat

```text
Extrage valorile din poza ecografiei si da-mi o singura linie pentru autofill protocol ecocardiografie, cu perechi cheie=valoare separate prin punct si virgula. Nu interpreta medical, nu inventa valori, nu calcula valori lipsa. Foloseste preferabil cheile: aoinel, aoasc, dao, as, vd, siv, dtdvs, dtsvs, ppvs, fevs, functiediastolica, im, ia, it, tapse, mapse, paps, vci. Pentru orice camp nesigur, nu il include. Raspunde doar cu linia finala.
```

## Observație

Pozițiile valorilor sunt calibrate pe imaginile scanate din `assets/`. Dacă schimbi protocolul sau imaginea de fundal, ajustează coordonatele din dicționarul `FIELDS` din `app.py`.
