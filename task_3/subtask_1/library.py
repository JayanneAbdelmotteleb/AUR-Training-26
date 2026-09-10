from abc import ABC, abstractmethod
from enum import Enum
class ItemStatus(Enum):
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked Out"
    LOST = "Lost"
class LibraryItem(ABC):
    FIELDS = ()
    def __init__(self, title, status=ItemStatus.AVAILABLE):
        self._title = title
        self._status = status
    @property
    def title(self):
        return self._title
    @property
    def status(self):
        return self._status
    @property
    @abstractmethod
    def loan_period_days(self):
        pass
    def checkout(self):
        if self._status != ItemStatus.AVAILABLE:
            raise ValueError(f"{self._title} is not available")
        self._status = ItemStatus.CHECKED_OUT
    def return_item(self):
        if self._status != ItemStatus.CHECKED_OUT:
            raise ValueError(f"{self._title} is not checked out")
        self._status = ItemStatus.AVAILABLE
    def mark_lost(self):
        self._status = ItemStatus.LOST
    def __lt__(self, other):
        return self._title.lower() < other._title.lower()
    def __repr__(self):
        return f"{type(self).__name__}(title={self._title}, status={self._status.name})"
    def __str__(self):
        return f"{self._title} ({type(self).__name__}) — {self._status.value}"
    @staticmethod
    def validate_isbn(isbn):
        isbn = isbn.replace("-", "").replace(" ", "")
        if len(isbn) != 13 or not isbn.isdigit():
            return False
        total = 0
        for i in range(13):
            weight = 1 if i % 2 == 0 else 3
            total += int(isbn[i]) * weight
        return total % 10 == 0
    @classmethod
    def from_dict(cls, data):
        item_class = ITEM_TYPES.get(data["type"].lower())
        if item_class is None:
            raise ValueError(f"Unknown item type: {data['type']}")
        return item_class._build(data)

class Book(LibraryItem):
    loan_period_days = 21
    FIELDS = ("author", "isbn")
    def __init__(self, title, author, isbn, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.author = author
        self.isbn = isbn
    @classmethod
    def _build(cls, data):
        return cls(
            title=data["title"],
            author=data.get("author", ""),
            isbn=data.get("isbn", ""),
            status=ItemStatus[data.get("status", "AVAILABLE")],
        )

class DVD(LibraryItem):
    loan_period_days = 5
    FIELDS = ("director",)
    def __init__(self, title, director, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.director = director
    @classmethod
    def _build(cls, data):
        return cls(
            title=data["title"],
            director=data.get("director", ""),
            status=ItemStatus[data.get("status", "AVAILABLE")],
        )

class Magazine(LibraryItem):
    loan_period_days = 14
    FIELDS = ("issue",)
    def __init__(self, title, issue, status=ItemStatus.AVAILABLE):
        super().__init__(title, status)
        self.issue = issue
    @classmethod
    def _build(cls, data):
        return cls(
            title=data["title"],
            issue=data.get("issue", ""),
            status=ItemStatus[data.get("status", "AVAILABLE")],
        )
ITEM_TYPES = {
    "book": Book,
    "dvd": DVD,
    "magazine": Magazine,
}
class Library:
    def __init__(self, database):
        self.items = []
        self.database = database
    def add_item(self, item):
        self.items.append(item)
    def find_by_title(self, title):
        for item in self.items:
            if item.title.lower() == title.lower():
                return item
        return None
    def checkout(self, title):
        item = self.find_by_title(title)
        if item is None:
            raise ValueError(f"No item found with title '{title}'")
        item.checkout()
    def return_item(self, title):
        item = self.find_by_title(title)
        if item is None:
            raise ValueError(f"No item found with title '{title}'")
        item.return_item()
    def list_available(self):
        available = [i for i in self.items if i.status == ItemStatus.AVAILABLE]
        return sorted(available)
    def load_from_database(self):
        self.items = self.database.load()
    def save_to_database(self):
        self.database.save(self.items)

class Database:
    def __init__(self, filepath):
        self.filepath = filepath
    def load(self):
        items = []
        with open(self.filepath) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = {}
                for pair in line.split("|"):
                    key, value = pair.split("=")
                    data[key] = value
                items.append(LibraryItem.from_dict(data))
        return items
    def save(self, items):
        with open(self.filepath, "w") as f:
            for item in items:
                type_name = type(item).__name__
                parts = [f"type={type_name}", f"title={item.title}"]
                for field in item.FIELDS:
                    parts.append(f"{field}={getattr(item, field)}")
                parts.append(f"status={item.status.name}")
                f.write("|".join(parts) + "\n")

def main():
    db = Database("database.txt")
    library = Library(db)
    library.load_from_database()
    print("All items:")
    for item in library.items:
        print(repr(item))
    library.checkout("Dune")
    print("\nAfter checkout:", library.find_by_title("Dune"))
    library.return_item("Dune")
    print("After return:", library.find_by_title("Dune"))
    print("\nAvailable items sorted:")
    for item in library.list_available():
        print(item)
    print("\nISBN checks:")
    print("9780441013593 ->", LibraryItem.validate_isbn("9780441013593"))
    print("1234567890123 ->", LibraryItem.validate_isbn("1234567890123"))
    library.save_to_database()
if __name__ == "__main__":
    main()