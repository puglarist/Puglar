# Puglar

This repository now contains a **starter DeepSeek multi-agent API** with Prisma models and Express endpoints so you can start building immediately.

## What is included

- Prisma schema for agents, runs, messages, tool calls, and provider credentials (`prisma/schema.prisma`).
- Express API starter with endpoints to create agents, create runs, start a run, and fetch run state.
- DeepSeek Chat Completions integration using `DEEPSEEK_API_KEY`.

## Quick start

1. Install dependencies:
   ```bash
   npm install
   ```
2. Copy env template:
   ```bash
   cp .env.example .env
   ```
3. Update `.env` values.
4. Generate Prisma client:
   ```bash
   npm run prisma:generate
   ```
5. Run the API:
   ```bash
   npm run dev
   ```

## API endpoints

- `GET /health`
- `POST /api/agents`
- `GET /api/agents`
- `POST /api/runs`
- `POST /api/runs/:runId/start`
- `GET /api/runs/:runId`

## Security note

Never commit real API keys to git. Keep `DEEPSEEK_API_KEY` in environment variables or a secrets manager.
