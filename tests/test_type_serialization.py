import datetime
import json

import cereal


class ValueClass():
    def __init__(self, _value):
        self.value = _value


class ValueSerializer(cereal.Serializer):
    value = cereal.Field()


# none

def test_none_serialization():
    obj = ValueClass(None)
    data = ValueSerializer().serialize(obj)
    assert data['value'] is None


# basic types

def test_bool_serialization():
    obj = ValueClass(False)
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], bool)
    assert data['value'] is False


def test_float_serialization():
    obj = ValueClass(0.0)
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], float)
    assert data['value'] == 0.0


def test_int_serialization():
    obj = ValueClass(0)
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], int)
    assert data['value'] == 0


def test_str_serialization():
    obj = ValueClass('')
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], str)
    assert data['value'] == ''


# date and datetime

def test_date_serialization():
    obj = ValueClass(datetime.date.today())
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], str)
    assert data['value'] == obj.value.isoformat()


def test_datetime_serialization():
    obj = ValueClass(datetime.datetime.now())
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], str)
    assert data['value'] == obj.value.isoformat()


# mapping and iterable types

def test_dict_serialization():
    obj = ValueClass({})
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], dict)


def test_list_serialization():
    obj = ValueClass([])
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], list)


def test_set_serialization():
    obj = ValueClass(set())
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], list)


def test_set_json_serialization():
    obj = ValueClass(set())
    data = ValueSerializer().serialize_json(obj)
    data = json.loads(data)
    assert isinstance(data['value'], list)


def test_tuple_serialization():
    obj = ValueClass(tuple())
    data = ValueSerializer().serialize(obj)
    assert isinstance(data['value'], list)


def test_tuple_json_serialization():
    obj = ValueClass(tuple())
    data = ValueSerializer().serialize_json(obj)
    data = json.loads(data)
    assert isinstance(data['value'], list)


# custom and unknown types

def test_custom_serialization():

    class CustomType():
        def value(self):
            return 'custom'

    obj = ValueClass(CustomType())

    ser = ValueSerializer()
    ser.add_handler(CustomType, lambda v: v.value())
    data = ser.serialize(obj)

    assert data['value'] == 'custom'


def test_unhandled_serialization():

    class UnhandledType():
        def __str__(self):
            return 'unhandled'

    obj = ValueClass(UnhandledType())
    data = ValueSerializer().serialize(obj)
    assert data['value'] == 'unhandled'
