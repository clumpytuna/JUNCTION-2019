from uuid import uuid4


def gen_uuid() -> str:
    """
    Generate a UUID
    """
    return str(uuid4()).replace('-', '')
