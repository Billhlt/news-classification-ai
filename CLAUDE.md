# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A news auto-categorization and archiving tool. The user pastes AI-related news, an AI service assigns each news item one of 17 predefined categories, the items are sorted by category, and appended to per-category Markdown files stored in the user's Obsidian vault.

The repo has two halves: a Vue 3 frontend at the root, and a Python FastAPI backend in `backend/`. **The AI service itself (SpringAI, port 8081) is external and NOT in this repository** — it must be running separately for the app to work. See `项目实现逻辑框架.md` for the authoritative design doc (Chinese).

## Required Services & Ports

| Service | Port | How to run |
| --- | --- | --- |
| Vite dev server (frontend) | 5173 | `npm run dev` |
| SpringAI (AI chat, external) | 8081 | Not in this repo; serves `GET /ai/chat?prompt=&chatId=` |
| FastAPI (backend) | 8083 | `cd backend && python main.py` |

## Commands

Frontend (from repo root):
- `npm install` — install dependencies
- `npm run dev` — Vite dev server with hot reload
- `npm run build` — runs `type-check` (vue-tsc) then `vite build`
- `npm run lint` — ESLint with `--fix --cache`
- `npm run format` — Prettier over `src/`
- `npm run type-check` — vue-tsc type checking only

Backend:
- `cd backend && pip install -r requirements.txt`
- `python main.py` — starts FastAPI on port 8083 (uvicorn, no reload)
- `uvicorn main:app --host 0.0.0.0 --port 8083 --reload`

## Architecture / Data Flow

Two routes (`src/router/index.ts`): `/` (SearchPage) and `/textbox` (TextBoxPage).

1. **SearchPage.vue** — textarea input. Normalizes text (collapse `\n+` to single newline, `trimEnd()`), then navigates to `/textbox?content=<processed text>`. Each line becomes one news item.
2. **TextBoxPage.vue** `handleStart` — splits content into `newsList` (string[]), initializes `analysisList` (string[]).
3. `processNewsWithAI` — builds one Promise per news item calling `chatWithAI(prompts.CategoryAnalysis + news, 'news_analysis_' + i)`, fires them all with `Promise.all()`. The AI returns only a category number (1–17). Results are written back into `analysisList` by index.
4. `transformToNewsBars` — renders each news item as a bar div (category number + content) into the left pane via `v-html`.
5. `sort` — builds `TDList01` as `[[originalIndex(1-based), categoryId], ...]`, sorts a copy by category into `TDList02`, then builds `finallist` as `[[categoryId, "- " + content], ...]` (Markdown list format). Note: sorting is wrapped in `setTimeout` to avoid blocking the UI.
6. `append` — calls `saveNews(finallist)` (frontend `src/api/api.js`) → FastAPI `POST /api/save-news` → validates and appends each item to the Markdown file for its category.

Key state shapes in `TextBoxPage.vue`:
- `newsList: string[]` — raw news, index-aligned with `analysisList`
- `analysisList: string[]` — AI category numbers (parallel to `newsList`)
- `TDList01: number[][]` — `[originalIndex, categoryId]`
- `finallist: [number, string][]` — `[categoryId, "- content"]`

## Frontend Notes

- `src/api/api.js` uses two separate axios instances with 100s timeouts. Response interceptors unwrap `response.data`, so `chatWithAI` resolves directly to the AI's reply string and `saveNews` resolves to the backend JSON body.
- `src/utils/prompts.js` holds the `CategoryAnalysis` prompt (the 17-category list and the instruction to reply with only a number) plus unused prompt templates.
- `api.js` and `prompts.js` are plain JS with **hand-written `.d.ts` declaration files** (`api.d.ts`, `prompts.d.ts`). `vue-tsc` type checking depends on these declarations staying in sync with the JS.
- UI text and code comments are in Chinese; keep that convention when adding UI strings.

## Backend Notes (`backend/main.py`)

- `POST /api/save-news` accepts `{"news_list": [[categoryId, content], ...]}`. Per item it validates the item is a list of length ≥ 2, category is an int (code checks `1..19`, but `NAME_MAP` only has 1–17), and content is a non-empty string. Items are appended (`"a"` mode, UTF-8) to `{category_name}.md`.
- `NAME_MAP` — the single source of truth mapping category id → file name (17 categories, e.g. `3` → `3.大语言模型，agent智能体-非商业`). Frontend and backend category lists must stay in sync.
- `DATA_DIR` — **hardcoded to an absolute Obsidian vault path** (`/media/bill/新加卷/.../ai技术的突破进展`), not `backend/data/`. Files are actually written there, and `DATA_DIR.mkdir(exist_ok=True)` runs at import time.
- `GET /api/health` — health check.
- CORS is wide open (`allow_origins=["*"]`).

## Outdated Docs / Gotchas

- `backend/README.md` is stale: its uvicorn example uses port 8081 (that's SpringAI's port; backend runs on 8083) and documents an old 19-category `NAME_MAP` (the code has 17). Prefer `项目实现逻辑框架.md` and the actual code.
- Full pipeline needs SpringAI on 8081 reachable from the browser (CORS) and the FastAPI backend on 8083. Without the AI service, `handleStart` will log errors into the right-hand status box.
- `api.js` note above: AI failures are caught in `processNewsWithAI` and surfaced only in the `rightContent` status textarea.
