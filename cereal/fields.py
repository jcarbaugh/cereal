from .utils import get_attribute_or_key


__all__ = ['BaseField', 'Field', 'ConstantField',
           'IteratorField', 'SerializerField']


class BaseField:
    """ The base field for all other fields.
        Acts as a pass-through to the underlying object or dict.
    """
    pass


class Field(BaseField):
    def __init__(self, from_attr=None):
        self.from_attr = from_attr


class ConstantField(BaseField):
    """ Returns a constant value each time the field is evaluated.
    """

    def __init__(self, value):
        self._value = value

    def value(self, obj, name):
        return self._value


class SerializerField(BaseField):

    def __init__(self, serializer):
        self._serializer = serializer()

    def value(self, obj, name):
        other = get_attribute_or_key(obj, name)
        if isinstance(other, (list, tuple, set)):
            return [self._serializer.asdict_(o) for o in other]
        elif hasattr(other, 'objects'):
            return [self._serializer.asdict_(o) for o in other.objects.all()]
        return self._serializer.asdict_(other)


class IteratorField(BaseField):
    """ Returns next value from iterator until StopIteration occurs.
        Once the iterator has been exhausted, this field will return None.
    """

    def __init__(self, container):
        self._iter = iter(container)

    def value(self, obj, name):
        """ Return next value from the iterator
            or None if StopIteration has occured.
        """
        if self._iter:
            try:
                v = next(self._iter)
                return v
            except StopIteration:
                self._iter = None
