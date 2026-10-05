# Architecture

## Overview

Tailgate Quote is a voice-first AI quoting assistant for technicians and contractors.

## System Components

### Backend (FastAPI)
- **API Routes**: Health, Catalog, Quotes, Voice/Tools
- **Services**: Pricing, Calculation, Quote, Evidence
- **Tools**: `get_price_list`, `calculate_line_item`, `create_draft_quote`, `confirm_and_send`
- **Database**: SQLite via SQLAlchemy (async)
- **Seed Data**: `data/seed_catalog.json`

### Frontend (React + TypeScript + Vite)
- **Pages**: Dashboard
- **Components**: VoicePanel, Transcript, QuotePanel, EvidencePanel, ConfirmationDialog, ConnectionStatus
- **Hooks**: useQuote, useVoiceAgent
- **Services**: API client (`services/api.ts`)

### Voice AI Layer
- **AssemblyAI Voice Agent API**: Speech recognition, turn detection, LLM orchestration, tool calling
- **JSON-Schema Tool Definitions**: Structured tool calling between agent and backend

## Data Flow

```
Technician (Voice)
    → React/PWA (microphone capture)
    → AssemblyAI Voice Agent (speech-to-text, LLM, tool calling)
    → FastAPI Backend (deterministic tools)
    → SQLite (persistence)
    → React (quote preview, evidence, confirmation)
```

## Key Design Principles

1. **Voice first** - Natural language interaction for job sites
2. **Backend owns business truth** - Pricing, calculations, validation, and quote state are deterministic
3. **Human in the loop** - The technician controls the final send action
4. **Evidence over assumptions** - Every important value is traceable to its source
5. **Simple infrastructure** - MVP prioritizes reliable end-to-end workflow

## Proof of Hearing

The evidence chain connects:
```
Spoken statement → Extracted value → Quote line item → Calculation → Final amount
```

Each step is recorded with source text and location, making the quote auditable.