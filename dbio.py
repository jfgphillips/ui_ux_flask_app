import json
from models import Post
from typing import Optional, List, Dict
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class PostManager(ABC):

    @abstractmethod
    def load_db(self):
        pass

    @abstractmethod
    def save_db(self, entries: List[Dict]):
        pass

    @abstractmethod
    def insert_post(self, post: Post, position: Optional[int] = 0):
        pass

    @abstractmethod
    def update_post(self, uid: int, updated_post: Post):
        pass

    @abstractmethod
    def delete_post(self, uid: int):
        pass

    @abstractmethod
    def get_posts(self) -> List[Dict]:
        pass

    @abstractmethod
    def inspect_post(self, uid) -> Optional[Dict]:
        pass


class JSONManager(PostManager):
    JSON_FILE = "data.json"

    def __init__(self):
        self._entries: List[Dict] = self.load_db()

    def load_db(self):
        with open(self.JSON_FILE, "r") as data:
            logger.info("loading db")
            return json.load(data)

    def save_db(self, entries: List[Dict]):
        with open(self.JSON_FILE, "w") as data:
            json.dump(entries, data)

    def insert_post(self, post: Post, position: Optional[int] = 0):
        self._entries.insert(position, post.as_dict())
        self.save_db(self._entries)

    def update_post(self, uid: int, updated_post: Post):
        for _idx, entry in enumerate(self._entries):
            if int(uid) == entry.get("uid"):
                logger.info("successfully found an entry, updating db")
                self._entries[_idx] = updated_post.as_dict()
        self.save_db(self._entries)

    def delete_post(self, uid: int):
        for _idx, entry in enumerate(self._entries):
            if int(uid) == entry.get("uid"):
                logger.info(f"deleting entry: {entry}")
                del self._entries[_idx]
        self.save_db(self._entries)

    def get_posts(self) -> List[Dict]:
        return self._entries

    def inspect_post(self, uid) -> Optional[Dict]:
        for _idx, entry in enumerate(self._entries):
            if int(uid) == entry.get("uid"):
                logger.info("found post to inspect")
                entry["count"] += 1
                self.save_db(self._entries)
                return entry
        return None


class SQLightManager(PostManager):

    def save_db(self, entries: List[Dict]):
        pass

    def insert_post(self, post: Post, position: Optional[int] = 0):
        pass

    def update_post(self, uid: int, updated_post: Post):
        pass

    def delete_post(self, uid: int):
        pass

    def get_posts(self) -> List[Dict]:
        pass

    def inspect_post(self, uid) -> Optional[Dict]:
        pass

    def load_db(self):
        pass