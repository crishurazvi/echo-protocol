
# Protocol ecocardiografie interactiv, Streamlit

Aceasta versiune NU folosește protocolul ca imagine de fundal. Formularul este reconstruit în HTML/CSS, cu câmpuri editabile direct în pagină, iar imaginea de cinetică parietală este inclusă ca asset separat.

## Fișiere

```text
app.py
requirements.txt
.streamlit/config.toml
assets/cinetica_parietala.png
```

## Deploy pe Streamlit Community Cloud

1. Creează un repository GitHub.
2. Încarcă fișierele din acest folder.
3. Pe Streamlit Community Cloud: New app.
4. Main file path: `app.py`.
5. Deploy.

## Format date

```text
aoinel=2.1;aoasc=3.4;dao=1.8;fevs=60;im=I;ia=Nu;it=I;tapse=22;paps=30
```

Acceptă și coduri HIPOCRATE:

```text
v238=2.1;v239=3.4;v240=1.8;v256=60;v273=I;v291=Nu;v302=I;v324=22;v304=30
```

## Bookmarklet

După deploy, înlocuiește `URL_STREAMLIT` cu adresa aplicației tale:

```javascript
javascript:(function(){var u='URL_STREAMLIT';var x=prompt('Lipeste valori pentru protocol','aoinel=2.1;aoasc=3.4;fevs=60;im=I;ia=Nu;it=I');if(x)location.href=u+'?data='+encodeURIComponent(x);})();
```

Exemplu:

```javascript
javascript:(function(){var u='https://protocol-eco.streamlit.app/';var x=prompt('Lipeste valori pentru protocol','aoinel=2.1;aoasc=3.4;fevs=60;im=I;ia=Nu;it=I');if(x)location.href=u+'?data='+encodeURIComponent(x);})();
```

## Print

În dialogul de print:
- A4
- Portrait
- Scale 100%
- Margins: None sau Minimum
