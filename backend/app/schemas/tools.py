from typing import Any, Dict, List, Optional
from pydantic import BaseModel


# JSON-Schema tool definitions for AssemblyAI Voice Agent integration

GET_PRICE_LIST_SCHEMA: Dict[str, Any] = {
    "name": "get_price_list",
    "description": (
        "Retrieve matching products and current catalog prices for the items "
        "needed for the job. Pass the categories and specifications you need."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "description": "List of items to look up in the pricing catalog.",
                "items": {
                    "type": "object",
                    "properties": {
                        "category": {
                            "type": "string",
                            "description": "Product category, e.g. copper_pipe, shutoff_valve, pex_pipe, labor.",
                        },
                        "specification": {
                            "type": "string",
                            "description": "Product specification, e.g. 3/4 inch, 1 inch, Type L.",
                        },
                    },
                    "required": ["category", "specification"],
                },
            },
        },
        "required": ["items"],
    },
}


CALCULATE_LINE_ITEM_SCHEMA: Dict[str, Any] = {
    "name": "calculate_line_item",
    "description": (
        "Perform a deterministic calculation for a single quote line item. "
        "Provide the SKU, quantity, and unit price. The backend performs the "
        "arithmetic so it is auditable and consistent."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "sku": {"type": "string", "description": "Catalog SKU for the item."},
            "quantity": {"type": "number", "description": "Quantity of the item."},
            "unit_price": {"type": "number", "description": "Unit price from the catalog."},
        },
        "required": ["sku", "quantity", "unit_price"],
    },
}


CREATE_DRAFT_QUOTE_SCHEMA: Dict[str, Any] = {
    "name": "create_draft_quote",
    "description": (
        "Create a draft quote with the collected line items, quantities, prices, "
        "and evidence. The quote is saved in DRAFT state and must be reviewed "
        "before it can be sent."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "customer_name": {"type": "string"},
            "customer_company": {"type": "string"},
            "job_address": {"type": "string"},
            "job_description": {"type": "string"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "sku": {"type": "string"},
                        "quantity": {"type": "number"},
                        "unit_price": {"type": "number"},
                        "description_override": {"type": "string"},
                    },
                    "required": ["sku", "quantity", "unit_price"],
                },
            },
            "labor_hours": {"type": "number"},
            "labor_rate": {"type": "number"},
            "notes": {"type": "string"},
        },
        "required": ["line_items"],
    },
}


CONFIRM_AND_SEND_SCHEMA: Dict[str, Any] = {
    "name": "confirm_and_send",
    "description": (
        "Finalize and send a quote after the technician has explicitly reviewed "
        "and confirmed it. The quote must be in DRAFT state. This action cannot "
        "be performed silently - the human must confirm."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "quote_id": {"type": "integer", "description": "ID of the quote to send."},
            "confirmed_by": {"type": "string", "description": "Name of the technician confirming."},
        },
        "required": ["quote_id"],
    },
}


ALL_TOOLS: List[Dict[str, Any]] = [
    GET_PRICE_LIST_SCHEMA,
    CALCULATE_LINE_ITEM_SCHEMA,
    CREATE_DRAFT_QUOTE_SCHEMA,
    CONFIRM_AND_SEND_SCHEMA,
]


class GetPriceListRequest(BaseModel):
    items: List[dict]


class CalculateLineItemRequest(BaseModel):
    sku: str
    quantity: float
    unit_price: float


class CreateDraftQuoteRequest(BaseModel):
    customer_name: Optional[str] = None
    customer_company: Optional[str] = None
    job_address: Optional[str] = None
    job_description: Optional[str] = None
    line_items: List[dict]
    labor_hours: float = 0.0
    labor_rate: float = 0.0
    notes: Optional[str] = None


class ConfirmAndSendRequest(BaseModel):
    quote_id: int
    confirmed_by: Optional[str] = None


class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict


class ToolResultResponse(BaseModel):
    tool: str
    success: bool
    result: dict