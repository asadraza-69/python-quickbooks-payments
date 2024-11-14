class Entity:
    """
    Represents an entity with an ID and a creation timestamp.
    """

    def __init__(self, id=None, created=None):
        self.id = id
        self.created = created
