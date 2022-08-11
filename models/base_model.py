#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy import create_engine

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, default=(datetime.utcnow()), nullable=False)
    updated_at = Column(DateTime, default=(datetime.utcnow()), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if (not kwargs.get("id", 0)):
                self.id = str(uuid.uuid4())

            for key, value in kwargs.items():
                if key in ['created_at', 'updated_at']:
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if 'created_at' not in kwargs:
                self.created_at = self.update_at = datetime.now()
 
    def __str__(self):
        """Returns a string representation of the instance"""
        return (f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}")

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        my_dict = dict(self.__dict__)

        if '_sa_instance_state' in my_dict.keys():
            del my_dict["_sa_instance_state"]

        my_dict["__class__"] = str(type(self).__name__)

        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()

        return my_dict

    def delete(self):
        from models import storage
        """delete the current instance from the storage"""
        storage.delete(self)
