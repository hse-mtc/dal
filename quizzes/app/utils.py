from datetime import datetime, UTC

def utcnow() -> datetime:
    return datetime.now(UTC)
