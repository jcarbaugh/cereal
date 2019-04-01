import datetime
import logging
import random

import pytest

import cereal


logger = logging.getLogger('cereal.tests')


@pytest.fixture
def instance():
    return new_instance()


def new_instance(id_=None):
    obj = JustAClass()
    obj.id = id_ or random.randint(1, 1024)
    obj.title = 'A Title'
    obj.content = 'jk not a post'
    obj.created = datetime.datetime.now()
    return obj


class ClassSerializer(cereal.Serializer):
    exclude = ('content',)
    id = cereal.Field()
    title = cereal.Field()
    created = cereal.Field()

    def serialize_title(self, obj):
        return obj.title.upper()


class DerivedClassSerializer(ClassSerializer):
    exclude = ('id',)
    content = cereal.Field()
    updated = cereal.Field()


class ClonedClassSerializer(ClassSerializer):
    pass


class JustAClass():
    pass


def test_exclude(instance):
    data = ClassSerializer().asdict_(instance)
    assert 'content' not in data


def test_serializer_method(instance):
    data = ClassSerializer().asdict_(instance)
    assert 'A TITLE' == data['title']


def test_datetime(instance):
    dt = datetime.datetime.now()
    instance.created = dt
    data = ClassSerializer().asdict_(instance)
    assert dt.isoformat() == data['created']


def test_serialize_list():
    obj1 = new_instance(1)
    obj2 = new_instance(2)
    data = ClassSerializer().serialize([obj1, obj2], raw=True)
    assert data[0]['id'] == obj1.id
    assert data[1]['id'] == obj2.id


def test_serializer_inheritance(instance):
    dt = datetime.datetime.now()
    instance.updated = dt
    data = DerivedClassSerializer().asdict_(instance)
    assert 'A TITLE' == data['title']
    assert 'jk not a post' == data['content']
    assert dt.isoformat() == data['updated']


def test_inheritance_override_exclude(instance):
    data = DerivedClassSerializer().asdict_(instance)
    assert 'id' not in data


def test_inheritance_exclude_from_parent(instance):
    data = ClonedClassSerializer().asdict_(instance)
    assert 'content' not in data

