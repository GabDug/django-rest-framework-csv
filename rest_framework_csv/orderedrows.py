from typing import List, Optional


class OrderedRows(list):
    """Maintains original header/field ordering."""

    def __init__(self, header: Optional[List[str]] = None) -> None:
        self.header = [c.strip() for c in header] if (header is not None) else None
