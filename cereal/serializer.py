import datetime
import json
import logging
from collections import OrderedDict

from .fields import Field
from .utils import get_attribute_or_key

__all__ = ['Serializer']


logger = logging.getLogger('cereal')


class SerializerMetaclass(type):

    def __new__(celf, name, bases, attrs):

        exclude_fields = attrs.pop('exclude', None) or []
        defined_fields = []
        model_fields = []

        if '__annotations__' in attrs:
            for k, v in attrs['__annotations__'].items():
                if k not in attrs:
                    defined_fields.append((k, Field()))

        for k, v in list(attrs.items()):
            if isinstance(v, Field):
                defined_fields.append((k, v))
                attrs.pop(k)

        meta_cls = attrs.pop('Meta', None)
        if meta_cls:
            model_class = getattr(meta_cls, 'model', None)
            if model_class:
                for field in model_class._meta.fields:
                    name = field.name
                    if name not in exclude_fields and \
                            name not in defined_fields:
                        model_fields.append(name)

        attrs['exclude_fields'] = exclude_fields
        attrs['defined_fields'] = OrderedDict(defined_fields)
        attrs['model_fields'] = model_fields

        cls = super(
            SerializerMetaclass, celf).__new__(celf, name, bases, attrs)
        return cls

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return OrderedDict()


class BaseSerializer:

    def __init__(self, *args, **kwargs):

        super(BaseSerializer, self).__init__(*args, **kwargs)

        def datetime_handler(value):
            return value.isoformat()

        self.handlers = {
            datetime.date: datetime_handler,
            datetime.datetime: datetime_handler,
            datetime.time: datetime_handler,
        }

    def _serialize_value(self, value):
        handler = self.handlers.get(type(value))
        if handler:
            return handler(value)
        elif value is None or isinstance(value, (bool, float, int, str)):
            return value
        elif isinstance(value, dict):
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, (list, tuple, set)):
            return list(self._serialize_value(v) for v in value)
        else:
            return '{}'.format(value)

    def _serializer_method(self, name):
        return 'serialize_{}'.format(name)

    def add_handler(self, _type, handler):
        if not callable(handler):
            raise ValueError('handler must be callable')
        self.handlers[_type] = handler

    def asdict_(self, obj):

        data = {}

        for name, field in self.defined_fields.items():
            """ Resolution order:
                1. serializer serialize_NAME() method
                2. field value() method
                3. object attribute / dict value
            """

            method_name = self._serializer_method(name)
            value = None

            if hasattr(self, method_name):
                value = getattr(self, method_name)(obj)
            elif hasattr(field, 'value'):
                value = getattr(field, 'value')(obj, name)
            else:
                value = get_attribute_or_key(obj, name)

            data[name] = self._serialize_value(value)

        for name in self.model_fields:
            """ Resolution order:
                1. serializer serialize_NAME() method
                2. object attribute
            """

            method_name = self._serializer_method(name)
            value = None

            if hasattr(self, method_name):
                value = getattr(self, method_name)(obj)
            elif hasattr(obj, name):
                value = get_attribute_or_key(obj, name)

            data[name] = self._serialize_value(value)

        return data

    def serialize(self, obj):
        data = self.asdict_(obj)
        return json.dumps(data)


class Serializer(BaseSerializer, metaclass=SerializerMetaclass):
    pass
