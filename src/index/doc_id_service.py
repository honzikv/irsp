# Current document id that will be returned by the service
_current_doc_id = 0


def get_next_doc_id():
    """
    Returns the next document id.
    :return: int
    """
    global _current_doc_id
    doc_id = _current_doc_id
    _current_doc_id += 1  # increment by one
    return doc_id


