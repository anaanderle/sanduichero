class Item:
    last_id = 1

    def __init__(self, name: str, value: float, description: str):
        self._name = name
        self._value = value
        self._description = description
        self._id = Item.last_id
        Item.last_id += 1

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def value(self, name: str):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        self._value = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description