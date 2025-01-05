from typing import Any, Dict, Optional, Type, Union
import logging

logger = logging.getLogger('gnomonic_projection.registry')

class RegistryBase(type):
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)

class BaseRegisteredClass(metaclass=RegistryBase):
    pass