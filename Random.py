import uuid


def generate_random_uuid(used_ids=None):
    """
    Creates a random UUID and checks if it is already used.

    Args:
        used_ids (list, optional): List of strings, containing all the used ID's. Defaults to None.

    Returns:
        _type_: _description_
    """

    if used_ids:
        if not isinstance(used_ids, list):
            raise TypeError("used_ids must be a list or None")
        valid_id = False
        while not valid_id:
            random_id = str(uuid.uuid4())
            if used_ids is None or random_id not in used_ids:
                valid_id = True
        return random_id
    return str(uuid.uuid4())
