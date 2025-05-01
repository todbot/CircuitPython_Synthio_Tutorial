import synthio

class Note:
    """Holder of a synthio.Note and any other needed per-note objects"""
    def __init__(self, note:synthio.Note):
        self.note = note

