# AI Use Case Suite — Logicalis

Demo web app with four AI use cases for document-heavy work, powered by the Claude API:

| Tab | What it does |
|---|---|
| **Document Intelligence** | Extracts metadata, named entities (people, organisations, places), IPTC Media Topics, an adaptive secondary taxonomy and PII/GDPR flags, with a confidence score per block. |
| **Contracts & Compliance** | Clause analysis, compliance risks, regulatory alerts and a Due Diligence score. A second document can be added to compare two versions clause by clause (A/B). |
| **Fraud & Risk** | Takes a case file, incident report or transaction log (including CSV) and returns a fraud score, anomalies, a risk register and a risk map. |
| **Due Diligence** | Tabular Review (Spanish only): extracts the same fields from up to 20 documents, checks every quote against the source text, raises cross-document alerts and exports CSV. |

The UI and the prompts are available in **Spanish, English and German**.

**Due Diligence** templates and prompts live in `prompts/tabular.js`, UI strings in `locales/afianza.js` and logic in `js/tabular-review.js`. Model IDs and limits can be overridden by defining `window.TABULAR_CONFIG` before that script. The results of the other three tabs are restyled by `js/*-afianza.js` and `prompts/suite-afianza.js`. **Guardar análisis** stores a full session as JSON (including the documents, so treat it as confidential) and **Cargar análisis guardado** restores a JSON session or an exported CSV (table only) without model or internet access; `js/i18next-fallback.js` covers i18next when its CDN is unreachable. Sample files: `Demo docs/clientes/afianza/`.

This page started as the Afianza client variant (`index_afianza.html`) and replaced the original three-tab `index.html`, which is still in the Git history.

## Quick start

It is a static site: no build step, no backend, no dependencies to install.

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Open <http://127.0.0.1:8765/>. (`.claude/launch.json` defines the same server as `static` for the Claude desktop preview.) `index.html` also works when opened directly via `file://`.

1. Paste your Anthropic API key (`sk-ant-…`) in the header field.
2. Pick a tab and drop a file (PDF, DOCX/DOC, TXT; PPT/PPTX in Document Intelligence; CSV in Fraud & Risk). You can use the files in [`Demo docs/`](#demo-docs).
3. Run the analysis.

### Language

Resolved in this order: `?lang=es|en|de` in the URL → preference saved in the browser (`localStorage`, key `aiucs.lang`) → browser language → Spanish. The header menu switches it at any time and results already on screen are re-rendered with translated labels.

## How it works

- Everything runs in the browser. Text is extracted locally (PDF.js for PDF, Mammoth for DOCX) and sent straight to `https://api.anthropic.com/v1/messages` with the user's key, using the `anthropic-dangerous-direct-browser-access` header. The model is `claude-haiku-4-5-20251001`.
- The key lives only in the input field (not persisted). There is no server, so the key is visible to whoever is using that browser: this is a **demo**, not a production architecture. For production, put a proxy in front that holds the key and forwards the session token.
- The model must answer with JSON. If the answer is not valid JSON (usually because it was cut off by the output limit) the UI shows an explicit message.

### Internationalisation

- [i18next](https://www.i18next.com/) 23.11.5 (loaded from jsDelivr). Resources are plain `.js` files, not JSON, so the page also works over `file://`.
- **UI strings**: `locales/<lang>.js`, exposed as `window.I18N.<lang>`. HTML elements use `data-i18n*` attributes; code uses `t('key')`.
- **Prompts**: `prompts/<lang>.js`, written natively in each language (not machine-translated at runtime). Free text in the output comes back in the UI language.
- **Enums**: the model returns language-neutral codes (e.g. risk levels); only their labels are translated in the UI (`tEnum(group, code)`).

## Project structure

```
.
├── index.html                      # The whole app: markup, CSS and the logic of the four tabs
├── js/
│   └── i18n.js                     # i18next bootstrap, language detection, header language menu
├── locales/                        # UI strings per language
│   ├── es.js  en.js  de.js
├── prompts/                        # Claude prompts per language
│   ├── es.js  en.js  de.js
├── AI Use Case Suite — Logicalis_files/
│   ├── pdf.min.js                  # PDF.js (PDF text extraction)
│   ├── mammoth.browser.min.js      # Mammoth (DOCX text extraction)
│   └── css2                        # Google Fonts stylesheet saved with the page
├── Demo docs/                      # Sample files, one folder per language
│   ├── es/  en/  de/
├── .claude/launch.json             # Local static-server config for the Claude desktop preview
├── LICENSE                         # MIT
└── README.md
```

## Demo docs

Six sample files per language so each use case can be tried without preparing data. Content, figures and page counts are the same in every folder.

| Use case | es | en | de |
|---|---|---|---|
| Contract comparison (agreement vs. template) | `CONTRATO DE DISTRIBUCIÓN.pdf` + `__PLANTILLA Distribuidor.pdf` | `DISTRIBUTOR AGREEMENT.pdf` + `__TEMPLATE Distributor.pdf` | `VERTRIEBSVERTRAG.pdf` + `__VORLAGE Vertriebspartner.pdf` |
| Document Intelligence: scanned UK dividend journal (3 pp.) | `Diario Reino Unido - FP 02.01.2019.pdf` | `Daily UK - PD 02.01.2019.pdf` | `Tagesjournal UK - PD 02.01.2019.pdf` |
| Document Intelligence: daily confirmation report (29 pp.) | `conf-diaria-694bf15f06-20190103150130.pdf` | `dly-conf-694bf15f06-20190103150130.pdf` | same name as en |
| Document Intelligence: Goldman Sachs confirmations (14 pp.) | `Confirmaciones de dividendos_ Goldman 29_FP 5feb.pdf` | `Dividends Confirmations_ Goldman 29_PD 5Feb.pdf` | `Dividendenbestätigungen_ Goldman 29_PD 5Feb.pdf` |
| Fraud & Risk: expense log (32 rows) | `fraude-riesgo-ejemplo.csv` | `fraud-risk-example.csv` | `betrug-risiko-beispiel.csv` |

Notes:

- `es/` is fully in Spanish, using Spanish date and number formats (`31/12/2018`, `1.944,782`) and Spanish file names (`FP` = fecha de pago, payment date). The UK journal and the Goldman Sachs confirmations keep their scanned look but carry an invisible text layer, so their text can be extracted. The untranslated originals are in the Git history, directly under `Demo docs/`.
- In `en/`, the agreement and the UK journal are verbatim copies of the originals because they were already in English; `Daily UK - PD 02.01.2019.pdf` is therefore the only scan without a text layer. The rest are clean text re-creations (not scans) with the same data.
- `de/` is fully re-created in German, using German date and number formats (`31.12.2018`, `1.944,782`).
- The contracts contain deliberate inconsistencies for the comparison to find (e.g. the template calls the distributor "non-exclusive" but then grants exclusivity; the agreement adds a non-compete, MFN, source-code escrow and a liability cap that the template lacks).
- The dividend files include oddities worth detecting (balance at record date different from opening balance, a reinvestment confirmation, mixed layouts).
- The CSV has planted fraud signals: payments split just under 500 €, the same consultancy paid repeatedly, an expense during a registered holiday, a jewellery purchase booked as office supplies, a self-approved expense and a same-day approval of a 4,850 € purchase. Only the headers and text values change between languages; amounts and ISO dates do not.

## Security

- Never commit API keys. Keep any local key file out of Git (add it to `.gitignore`); the app only needs the key pasted in the browser.
- Demo documents contain fictional or anonymised data. Do not upload real personal or confidential documents to a demo instance without authorisation.

## License

MIT — see [LICENSE](LICENSE).
