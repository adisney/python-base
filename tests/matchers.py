def HasFields(cls, fields):
    class HasFields(cls):
        def __eq__(self, other):
            return all(other[key] == fields[key] for key in fields.keys())
    return HasFields()
