class Item:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def get_name(self) -> str:
        return self.name
