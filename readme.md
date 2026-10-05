# Tailgate Quote

### Voice-first field service quoting for technicians and contractors

> **Talk through the job. Get the quote. Verify every number.**

Tailgate Quote is a voice-first AI quoting assistant designed for technicians and contractors working at job sites.

Instead of typing measurements, materials, and job requirements into a quoting system, a technician can simply describe the work naturally by voice. The agent listens, asks clarifying questions when information is missing, retrieves pricing from a catalog, calculates line-item costs, and prepares a quote for human review.

The quote is **never sent automatically**. The technician must review and explicitly confirm it before the system marks it as sent.

A core feature of Tailgate Quote is **Proof of Hearing**: important quote values are connected back to the exact words that produced them, allowing the technician to verify what the agent heard and how the final numbers were produced.

---

# Problem

Technicians and contractors often create quotes while standing at a job site.

The information they need to capture may include:

* Material type
* Material size
* Quantity
* Measurements
* Labor
* Additional components
* Customer information
* Current prices

Traditional quoting workflows require typing this information manually or remembering it until later.

That creates friction and increases the possibility of:

* Missing job details
* Incorrect quantities
* Pricing mistakes
* Incomplete quotes
* Administrative work after leaving the job site

Tailgate Quote explores a simpler workflow:

> **Speak the job description naturally and let the system turn it into a verified quote.**

---

# Solution

Tailgate Quote combines real-time voice interaction with structured backend tools.

A technician can say something like:

> "Replace the three-quarter-inch copper run from the meter to the house. It's about eighteen feet, plus a new shutoff valve."

The agent can then:

1. Understand the request.
2. Extract structured job information.
3. Ask for missing details.
4. Retrieve matching catalog prices.
5. Calculate line-item totals.
6. Create a draft quote.
7. Show the evidence behind each important value.
8. Ask the technician to review the quote.
9. Send the quote only after explicit confirmation.

---

# Key Feature: Proof of Hearing

Voice systems can fail in subtle ways.

A technician may say:

> "about eighteen feet"

while the system interprets it as:

> `18 ft`

The user should be able to verify that interpretation.

Tailgate Quote therefore maintains an evidence relationship between:

```text
Spoken statement
       ↓
Extracted value
       ↓
Quote line item
       ↓
Calculation
       ↓
Final amount
```

For example:

```text
3/4-inch Copper Pipe
18 ft × $8.50
Subtotal: $153.00

Evidence:
"three-quarter-inch copper run..."
"about eighteen feet"

Price source:
Catalog SKU: CP-075

Calculation:
18 × 8.50 = 153.00
```

This makes the quote auditable instead of treating the AI's output as a black box.

---

# Example Workflow

```text
Technician
    │
    │ Voice
    ▼
AssemblyAI Voice Agent
    │
    │ Understand request
    ▼
Clarification
    │
    │ Missing information?
    ▼
Tool Calling
    │
    ├── get_price_list
    │
    ├── calculate_line_item
    │
    └── create_draft_quote
    │
    ▼
Draft Quote
    │
    ├── Line items
    ├── Prices
    ├── Calculations
    └── Evidence
    │
    ▼
Human Review
    │
    │ Explicit confirmation
    ▼
confirm_and_send
    │
    ▼
Quote Sent
```

---

# Architecture

```text
                         ┌─────────────────────┐
                         │      TECHNICIAN     │
                         │        🎙️           │
                         └──────────┬──────────┘
                                    │
                                    │ Voice
                                    ▼
                         ┌─────────────────────┐
                         │    React / PWA      │
                         │                     │
                         │ Live Transcript     │
                         │ Conversation        │
                         │ Quote Preview       │
                         │ Evidence Panel      │
                         └──────────┬──────────┘
                                    │
                                    │ WebSocket
                                    ▼
                         ┌─────────────────────┐
                         │     AssemblyAI      │
                         │   Voice Agent API   │
                         │                     │
                         │ Speech Recognition  │
                         │ Turn Detection      │
                         │ LLM                 │
                         │ Tool Calling        │
                         │ Voice Response      │
                         └──────────┬──────────┘
                                    │
                                    │ Tool Calls
                                    ▼
                         ┌─────────────────────┐
                         │      FastAPI        │
                         │      Backend        │
                         │                     │
                         │ Tool Router         │
                         │ Quote Service       │
                         │ Pricing Service     │
                         │ Calculation Service │
                         │ Evidence Service    │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         ▼                     ▼
                  ┌──────────────┐      ┌──────────────┐
                  │    SQLite    │      │ Price Catalog│
                  │              │      │              │
                  │ Quotes       │      │ SKU          │
                  │ Items        │      │ Unit Price   │
                  │ Evidence     │      │ Category     │
                  └──────────────┘      └──────────────┘
```

[![Architecture diagram of kashifali-it/tailgate-quote](https://gitdiagram.com/kashifali-it/tailgate-quote/diagram.png)](https://gitdiagram.com/kashifali-it/tailgate-quote?utm_source=readme&utm_medium=picture)
---

# Technology Stack

## Voice AI

* **AssemblyAI Voice Agent API**
* Real-time speech recognition
* Voice interaction
* Turn detection
* Tool calling
* Voice responses

## Backend

* **Python**
* **FastAPI**
* Pydantic
* SQLite
* REST APIs
* WebSocket integration where required

## Frontend

* **React**
* **TypeScript**
* **Vite**
* Tailwind CSS
* shadcn/ui

## AI / Agent Layer

* AssemblyAI Voice Agent
* LLM-based conversation orchestration
* JSON-Schema tool calling
* Structured tool results

## Data

* SQLite
* Seeded pricing catalog
* Quote records
* Quote line items
* Transcript/evidence records

## Development

* Git
* GitHub
* Docker
* pytest

---

# Agent Tools

The voice agent will interact with the backend through structured tools.

## `get_price_list`

Retrieves matching products and current catalog prices.

Example:

```json
{
  "items": [
    {
      "category": "copper_pipe",
      "specification": "3/4 inch"
    },
    {
      "category": "shutoff_valve",
      "specification": "3/4 inch"
    }
  ]
}
```

---

## `calculate_line_item`

Performs deterministic calculations for quote items.

Example:

```json
{
  "sku": "CP-075",
  "quantity": 18,
  "unit_price": 8.50
}
```

Result:

```json
{
  "subtotal": 153.00
}
```

The backend performs the calculation rather than relying on the LLM for arithmetic.

---

## `create_draft_quote`

Creates a quote in `DRAFT` state after sufficient information has been collected.

The draft contains:

* Customer/job information
* Line items
* Quantities
* Unit prices
* Subtotals
* Evidence references
* Total

---

## `confirm_and_send`

Finalizes and sends a quote after explicit human confirmation.

The agent cannot silently send a quote.

The intended state transition is:

```text
DRAFT
  │
  │ Human confirmation
  ▼
SENT
```

---

# Quote State

The quote lifecycle is intentionally controlled by the backend.

```text
┌─────────────┐
│    DRAFT    │
└──────┬──────┘
       │
       │ Human review
       ▼
┌─────────────┐
│   APPROVED  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     SENT    │
└─────────────┘
```

The AI can prepare the quote, but the human controls the final action.

---

# Example Conversation

### Technician

> "I need a quote for replacing the three-quarter copper line from the meter to the house. It's about eighteen feet and we'll need a new shutoff valve."

### Agent

> "I understand. I have eighteen feet of three-quarter-inch copper pipe and one three-quarter-inch shutoff valve. Do you want standard Type L copper?"

### Technician

> "Yes."

### Agent

> "Got it. I'll price those items and prepare the draft."

The agent calls:

```text
get_price_list()
```

then:

```text
calculate_line_item()
```

and:

```text
create_draft_quote()
```

The technician sees:

```text
QUOTE #TQ-1024

3/4" Type L Copper Pipe
18 ft × $8.50       $153.00

3/4" Shutoff Valve
1 × $24.00            $24.00

Labor
1 × $120.00          $120.00
────────────────────────────
TOTAL                 $297.00
```

The technician can inspect the evidence behind the quantities and pricing before confirming.

---

# Project Structure

```text
tailgate-quote/
│
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── health.py
│   │   │   │   ├── quotes.py
│   │   │   │   ├── catalog.py
│   │   │   │   └── voice.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── models/
│   │   │   ├── quote.py
│   │   │   ├── quote_item.py
│   │   │   ├── catalog_item.py
│   │   │   └── evidence.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── quote.py
│   │   │   ├── catalog.py
│   │   │   ├── tools.py
│   │   │   └── evidence.py
│   │   │
│   │   ├── services/
│   │   │   ├── quote_service.py
│   │   │   ├── pricing_service.py
│   │   │   ├── calculation_service.py
│   │   │   └── evidence_service.py
│   │   │
│   │   ├── tools/
│   │   │   ├── get_price_list.py
│   │   │   ├── calculate_line_item.py
│   │   │   ├── create_draft_quote.py
│   │   │   └── confirm_and_send.py
│   │   │
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── seed.py
│   │   │
│   │   └── integrations/
│   │       └── assemblyai.py
│   │
│   ├── tests/
│   │   ├── test_quotes.py
│   │   ├── test_pricing.py
│   │   ├── test_calculations.py
│   │   └── test_tools.py
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── VoicePanel.tsx
│   │   │   ├── Transcript.tsx
│   │   │   ├── QuotePanel.tsx
│   │   │   ├── QuoteLineItem.tsx
│   │   │   ├── EvidencePanel.tsx
│   │   │   ├── ConfirmationDialog.tsx
│   │   │   └── ConnectionStatus.tsx
│   │   │
│   │   ├── hooks/
│   │   │   ├── useVoiceAgent.ts
│   │   │   └── useQuote.ts
│   │   │
│   │   ├── services/
│   │   │   └── api.ts
│   │   │
│   │   ├── types/
│   │   │   ├── quote.ts
│   │   │   ├── transcript.ts
│   │   │   └── evidence.ts
│   │   │
│   │   ├── pages/
│   │   │   └── Dashboard.tsx
│   │   │
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── data/
│   └── seed_catalog.json
│
├── docs/
│   ├── architecture.md
│   ├── demo-script.md
│   └── screenshots/
│
└── docker-compose.yml
```

---

# Development Stages

The project will be developed incrementally.

### Stage 0 — Project Setup

* Repository setup
* Backend skeleton
* Frontend skeleton
* Environment configuration
* Health endpoint

### Stage 1 — AssemblyAI Voice Agent

* AssemblyAI integration
* Microphone input
* Voice conversation
* Basic transcript
* Voice response

### Stage 2 — Tool Calling

* JSON-Schema tool definitions
* FastAPI tool endpoints
* Tool call/result flow

### Stage 3 — Pricing Catalog

* Catalog schema
* Seed data
* `get_price_list`

### Stage 4 — Quote Calculations

* Line-item calculations
* Deterministic totals
* Validation

### Stage 5 — Draft Quotes

* Quote database
* Quote state
* `create_draft_quote`

### Stage 6 — Proof of Hearing

* Transcript events
* Evidence references
* Source-to-field mapping
* Evidence UI

### Stage 7 — Human Confirmation

* Review workflow
* Confirmation UI
* `confirm_and_send`
* Quote state transitions

### Stage 8 — Production Demo UI

* Responsive interface
* Live transcript
* Quote panel
* Evidence panel
* Error states

### Stage 9 — Deployment

* Backend deployment
* Frontend deployment
* Environment configuration
* End-to-end testing

### Stage 10 — Hackathon Submission

* README finalization
* Architecture diagram
* Demo video
* Presentation slides
* Cover image
* Submission description

---

# Design Principles

### 1. Voice first

The primary interaction should feel natural for someone working at a job site.

### 2. Backend owns business truth

The LLM interprets the conversation, but pricing, calculations, validation, and quote state are controlled by deterministic backend logic.

### 3. Human in the loop

The system prepares and explains the quote. The technician controls the final send action.

### 4. Evidence over assumptions

Important quote values should be traceable back to the conversation or catalog.

### 5. Simple infrastructure

The MVP should prioritize a reliable end-to-end workflow over unnecessary infrastructure.

### 6. Incremental development

Every major capability is implemented, tested, committed, and documented as a separate stage.

---

# Hackathon

This project is being developed for the **AssemblyAI Voice Agent Hackathon 2026**, organized by lablab.ai and AssemblyAI.

The project focuses on:

* Real-time voice interaction
* AssemblyAI Voice Agent API
* JSON-Schema tool calling
* Human-in-the-loop workflows
* Structured backend automation
* Business-oriented AI agents
* Auditable AI-generated quotes

---

# License

MIT License
