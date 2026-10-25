"""
Optional project capability: Tools & External API Integration.

Implement this module only if this capability is relevant to your application's
user problem. Remove the file if the capability is not used.

Conceptual Overview:
-------------------
Tools allow the AI application to perform operations beyond text generation,
such as fetching live data from external APIs, performing calculations, or
executing internal application functions.

Key concepts when implementing tools:
1. Tool Definition: Defining function schemas (names, descriptions, parameters)
   that describe what each tool does.
2. Model Tool Calling: Providing tool schemas to the model so it can request tool execution
   when needed.
3. Execution & Response: Parsing tool call requests, executing the corresponding
   Python function or API call, and passing the results back to the model or user.

Note:
-----
Tools should be deterministic, safe, and scoped to the user problem.
"""

from src.schemas.responses import ProductArgs, ProductObservation

PRODUCT_RECORDS = {
    "LAPTOP-1000": {
        "manufacturing": "2026-12-15T17:00:00+02:00",
        "testing": "2027-01-10T17:00:00+02:00",
        "shipping": "2027-01-31T12:00:00+02:00",
    }
}


def _normalize(product_id: str) -> str:
    """Make 'laptop model 1000', 'laptop 1000' and 'LAPTOP_1000' all become LAPTOP-1000."""
    key = product_id.strip().upper().replace("_", " ")
    key = key.replace("MODEL", "").replace("-", " ")
    return "-".join(key.split())


def lookup_product_deadline(product_id: str, stage: str) -> ProductObservation:
    """Read the deadline for a production stage of a fictional product."""
    args = ProductArgs(product_id=product_id, stage=stage)
    key = _normalize(args.product_id)
    deadline = PRODUCT_RECORDS.get(key, {}).get(args.stage)
    return ProductObservation(
        found=deadline is not None,
        product_id=key,
        stage=args.stage,
        deadline=deadline,
    )