from dataclasses import dataclass, field
from typing import Optional


@dataclass()
class Post:
    title: str
    year: str
    rating: int
    count: int = field(default=0)
    description: Optional[str] = field(default=None)
    uid: Optional[int] = field(default=None)

    def __post_init__(self):
        if not self.uid:
            self.uid = self._generate_id()

    def as_dict(self):
        return {
            "uid": self.uid,
            "title": self.title,
            "year": self.year,
            "count": self.count,
            "rating": self.rating,
            "description": self.description,
        }

    def _generate_id(self):
        return abs(hash((self.title, self.year, self.description)))

    # from dict can be replaced with **kwargs of dict
    @classmethod
    def fromDict(cls, row):
        return cls(
            uid=row.get("uid"),
            title=row.get("title"),
            year=row.get("year"),
            rating=row.get("rating"),
            count=row.get("count") if row.get("count") is not None else 0,
            description=row.get("description"),
        )
