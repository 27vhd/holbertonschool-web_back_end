#!/usr/bin/env python3
"""
Base model module providing common attributes and methods for all models.
"""
import json
import uuid
from datetime import datetime
from os import path

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA = {}


class Base:
    """
    Base class for all models, providing id, timestamps, and
    serialization/deserialization functionality.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes a Base instance with optional keyword arguments.
        """
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        if kwargs.get('created_at') is None:
            self.created_at = datetime.utcnow()
        else:
            self.created_at = datetime.strptime(kwargs.get('created_at'),
                                                TIMESTAMP_FORMAT)
        if kwargs.get('updated_at') is None:
            self.updated_at = datetime.utcnow()
        else:
            self.updated_at = datetime.strptime(kwargs.get('updated_at'),
                                                TIMESTAMP_FORMAT)

    def __eq__(self, other: object) -> bool:
        """
        Returns True if both instances have the same id.
        """
        if not isinstance(other, type(self)):
            return False
        if not isinstance(self, Base):
            return False
        return (self.id == other.id)

    def to_json(self, for_serialization: bool = False) -> dict:
        """
        Returns a JSON-compatible dictionary representation of the instance.
        """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key[0] == '_':
                continue
            if type(value) is datetime:
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def load_from_file(cls):
        """
        Loads all instances of the class from a JSON file on disk.
        """
        s_class = cls.__name__
        file_path = ".db_{}.json".format(s_class)
        DATA[s_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as f:
            objs_json = json.load(f)
            objs = [cls(**o) for o in objs_json.values()]
            DATA[s_class] = {o.id: o for o in objs}

    @classmethod
    def save_to_file(cls):
        """
        Saves all instances of the class to a JSON file on disk.
        """
        s_class = cls.__name__
        file_path = ".db_{}.json".format(s_class)
        objs_json = {}
        for obj_id, obj in DATA[s_class].items():
            objs_json[obj_id] = obj.to_json(for_serialization=True)

        with open(file_path, 'w') as f:
            json.dump(objs_json, f)

    def save(self):
        """
        Saves the current instance to the class storage and disk.
        """
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self):
        """
        Removes the current instance from the class storage and disk.
        """
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id) is not None:
            del DATA[s_class][self.id]
        self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """
        Returns the number of instances currently stored for this class.
        """
        s_class = cls.__name__
        return len(DATA.get(s_class, {}))

    @classmethod
    def all(cls) -> list:
        """
        Returns a list of all instances currently stored for this class.
        """
        return list(DATA.get(cls.__name__, {}).values())

    @classmethod
    def get(cls, id: str) -> object:
        """
        Returns an instance by its id, or None if not found.
        """
        s_class = cls.__name__
        return DATA.get(s_class, {}).get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> list:
        """
        Returns a list of instances matching all given attribute values.
        """
        s_class = cls.__name__

        def _search(obj):
            for k, v in attributes.items():
                if getattr(obj, k) != v:
                    return False
            return True

        return list(filter(_search, DATA.get(s_class, {}).values()))
