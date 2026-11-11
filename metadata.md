# Repository Metadata: zouq-ul-ilm

_Extracted from the GitHub API on 2026-11-11. Public metadata only._

---

## 1. Core Identity

| Field | Value |
| --- | --- |
| Name | `zouq-ul-ilm` |
| Full Name | `muhammadsami987123/zouq-ul-ilm` |
| URL | https://github.com/muhammadsami987123/zouq-ul-ilm |
| Clone (HTTPS) | `https://github.com/muhammadsami987123/zouq-ul-ilm.git` |
| Visibility | Private |
| Archived | No |
| Homepage | Not set |
| Default Branch | `main` (only branch) |

## 2. Description

> AI study assistant for students: turn course outlines and PDFs into structured study notes, in-depth or quick summaries, document rewrites, and presentation-ready PPTX decks from built-in templates. Stack: Next.js 15, React 19, Tailwind CSS 4 frontend; Python (Flask + FastAPI) with Google Gemini, multi-key rotation, OCR, and PDF/PPTX export.

Character count: 343 / 350 (GitHub limit).

## 3. Language Profile

| Language | Bytes | Share |
| --- | --- | --- |
| Python | 179,216 | 75.1% |
| TypeScript | 57,796 | 24.2% |
| CSS | 941 | 0.4% |
| JavaScript | 605 | 0.3% |

| Field | Value |
| --- | --- |
| Primary Language (GitHub) | **Python** |
| Total languages detected | 4 |

## 4. Repository Status

| Field | Value |
| --- | --- |
| Created (UTC) | 2026-11-11 10:57:11 |
| Last Updated (UTC) | 2026-11-11 10:58:48 |
| Last Push (UTC) | 2026-11-11 10:57:19 |
| Commits | 1 |
| Tracked Files | 67 |
| Working Tree Size (excl. `.git`) | 5.07 MB |
| Stars | 0 |
| Watchers / Subscribers | 0 |
| Forks | 0 |
| Open Issues | 0 |

## 5. Licensing

| Field | Value |
| --- | --- |
| License | GNU General Public License v3.0 |
| SPDX ID | `GPL-3.0` |
| License file | `LICENSE` (official GPL-3.0 text, 35,149 bytes) |
| Detection | Confirmed by GitHub |

## 6. Topics (20 / 20 max)

`ai`, `document-rewriter`, `edtech`, `education`, `fastapi`, `flask`, `generative-ai`, `google-gemini`, `llm`, `nextjs`, `notes-generator`, `powerpoint`, `pptx`, `presentation-generator`, `python`, `react`, `study-assistant`, `summarizer`, `tailwindcss`, `typescript`

## 7. Repository Features

| Feature | State |
| --- | --- |
| Issues | Enabled |
| Projects | Enabled |
| Wiki | Disabled |
| Discussions | Disabled |
| Pages | Not configured |
| Actions / Workflows | None committed |

## 8. Tech Stack

### Frontend (`frontend/`)

| Package | Version | Role |
| --- | --- | --- |
| `next` | 15.5.4 | App Router framework |
| `react` / `react-dom` | 19.1.0 | UI runtime |
| `tailwindcss` | ^4 | Styling (PostCSS plugin) |
| `typescript` | ^5 | Type safety |
| `axios` | ^1.12.2 | HTTP client |
| `framer-motion` | ^12.23.22 | Animations |
| `react-icons` | ^5.5.0 | Icon set |
| `eslint` / `eslint-config-next` | ^9 / 15.5.4 | Linting |

### Backend (`backend/`)

| Package | Role |
| --- | --- |
| `Flask`, `Flask-CORS` | Main HTTP API (`app.py`) |
| `google-generativeai` | Gemini model calls (keys `GEMINI_API_KEY_1..10`, rotated) |
| `PyPDF2`, `PyMuPDF` | PDF text extraction |
| `python-pptx` | PPTX generation from templates |
| `python-docx` | DOCX handling |
| `fpdf` | PDF export |
| `pytesseract`, `Pillow` | OCR and image handling |
| `python-dotenv` | Environment configuration |

### PPT Module (`backend/PPT_gen/`)

| Package | Role |
| --- | --- |
| `fastapi`, `uvicorn` | Alternative ASGI service for slide generation |
| `pydantic` | Request/settings validation |
| `pandas`, `numpy` | Data processing |
| `requests` | Upstream API calls |
| `structlog` | Structured logging |
| `pytest`, `black`, `flake8`, `mypy` | Dev tooling |

## 9. HTTP API Surface (Flask, `backend/app.py`)

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/` | Service root / health |
| POST | `/upload` | Upload source document (PDF etc.) |
| GET | `/templates` | List available PPTX templates |
| POST | `/generate` | Generate PPTX deck from content + template |
| POST | `/summary` | Generate summary (selectable style/depth) |
| POST | `/rewrite` | Rewrite document content |
| GET | `/progress/<task_id>` | Poll generation progress |
| GET | `/download/<task_id>` | Download generated artifact |

## 10. Frontend Routes (Next.js App Router)

| Route | File |
| --- | --- |
| `/` | `frontend/src/app/page.tsx` |
| `/notes` | `frontend/src/app/notes/page.tsx` |
| `/slides` | `frontend/src/app/slides/page.tsx` |
| `/summary` | `frontend/src/app/summary/page.tsx` |
| `/rewrite` | `frontend/src/app/rewrite/page.tsx` |

Shared UI: `components/Navigation.tsx`, `components/Footer.tsx`; API/config helpers: `src/lib/api.ts`, `src/lib/config.ts`.

## 11. Repository Layout

```
Zouq-ul-ilm/
|-- LICENSE                 GPL-3.0
|-- README.md
|-- metadata.md             this file
|-- backend/
|   |-- app.py              Flask API
|   |-- requirements.txt
|   |-- Notes_gen/          notes outline + PDF generation
|   |-- Summarize_gen/      summarization pipeline
|   |-- PPT_gen/            PPTX generation module (FastAPI-based)
|   |   |-- config/ services/ utils/ docs/
|   |   `-- templates/      6 PPTX templates + template_metadata.json
|   `-- uploads/            runtime uploads (git-ignored)
`-- frontend/
    |-- package.json
    `-- src/app, src/components, src/lib
```

### File Count by Type (tracked)

| Extension | Files |
| --- | --- |
| `.py` | 21 |
| `.tsx` | 8 |
| `.pptx` | 6 |
| `.svg` | 5 |
| `.ts` | 4 |
| `.json` | 4 |
| `.pdf` | 4 |
| `.md` | 3 |
| `.mjs` | 2 |
| `.txt` | 2 |
| `.gitignore` | 2 |
| `.css`, `.ico`, `.example`, no extension | 1 each (+3 no-ext) |

## 12. Version Control

| Field | Value |
| --- | --- |
| Commit | `44f44b524a3dcb174f41eda42f2939be0db5f594` |
| Short SHA | `44f44b5` |
| Message | `chore: initial commit` |
| Author | Muhammad Sami |
| Date | 2026-11-11 03:57:06 PM (+05:00 PKT) |
| Remote | `origin` -> GitHub (HTTPS) |
| Tracking | `main` -> `origin/main` (in sync) |

## 13. Bundled Assets

| Asset | Count | Notes |
| --- | --- | --- |
| PPTX templates | 6 | `blue`, `gradation_green`, `green`, `Polyhedron`, `silver_stone`, `yellow_subhan` |
| Course-outline PDFs | 3 | `backend/Notes_gen/course_outline/` |
| Sample input PDF | 1 | `backend/Summarize_gen/content/Manual.pdf` (1.73 MB, largest file) |

Bundled PDFs are third-party course material; the GPL-3.0 license covers the source code, not those documents.

## 14. Security Notes

- No credentials, tokens, API keys, or secrets are recorded in this file.
- Only `.env.example` is tracked; actual `.env` files are git-ignored.
- `backend/uploads/` runtime files are excluded from version control via `*.pdf` ignore rules.
- A scan of the tracked repository for common credential patterns returned no matches.
