from uuid import UUID


def is_uuid(identifier) -> bool:
    try:
        UUID(identifier)
        return True
    except Exception:
        return False
