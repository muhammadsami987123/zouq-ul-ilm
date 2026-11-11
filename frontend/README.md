# GemNotes Frontend (Next.js + Tailwind)

A modern, responsive Next.js (App Router) frontend styled with Tailwind CSS. Migrated from the legacy CRA app to improve maintainability and performance while preserving all features and flows (Notes, Summary, Slides, Rewrite).

## Tech Stack
- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS (via `@tailwindcss/postcss` in `postcss.config.mjs`)
- Axios for API
- Framer Motion, react-icons

## Project Structure
```
frontend-next/
  src/
    app/            # App Router pages
      page.tsx      # Home
      notes/        # Notes tool
      summary/      # Summary tool
      slides/       # Slides tool
      rewrite/      # Rewrite tool
    components/     # Header, Navigation, Footer
    lib/            # api.ts (axios helpers), config.ts (API URL)
  public/
  .env.local        # NEXT_PUBLIC_API_URL
```

## Environment
Create `.env.local` in `frontend-next/` (already created if you ran the scripts):
```
NEXT_PUBLIC_API_URL=http://localhost:5000
```
Point this at your FastAPI backend.

## Backend (FastAPI) Endpoints Expected
- POST `/upload`
- POST `/generate`
- POST `/summary`
- POST `/slides`
- POST `/rewrite`
- GET `/progress/{task_id}`
- GET `/download/{task_id}`
- GET `/templates`

CORS example (allow Next dev origin):
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Install & Run
```
# from repository root
cd frontend-next
npm install
npm run dev
# http://localhost:3000
```

## Features / UI Parity
- Notes: upload → topics from backend → manual topic entry → generate → progress → download
- Summary: upload → length selection → generate → progress → download
- Slides: upload → template selection → topics → generate → progress → download
- Rewrite: upload → rewrite → progress → download

## Known Notes
- If Next.js prints a warning about multiple lockfiles, remove the extra one at the repository root or set `outputFileTracingRoot` in `next.config.ts`.
- The legacy CRA app remains in `frontend/` for reference; it can be removed once you no longer need it.

## Migration Notes
- All traditional CSS was commented out in the legacy project. New UI uses Tailwind utilities only.
- API calls preserved; endpoints unchanged.
