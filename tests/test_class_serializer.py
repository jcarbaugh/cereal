import datetime
import logging

import pytest

import cereal


logger = logging.getLogger('cereal.tests')


@pytest.fixture
def instance():
    obj = JustAClass()
    obj.id = 3
    obj.title = 'A Title'
    obj.content = 'jk not a post'
    obj.created = datetime.datetime.now()
    return obj


class ClassSerializer(cereal.Serializer):
    exclude = ('id',)
    title = cereal.Field()
    content = cereal.Field()
    created = cereal.Field()

    def serialize_title(self, obj):
        return obj.title.upper()


class JustAClass():
    pass


def test_exclude(instance):
    data = ClassSerializer().to_dict(instance)
    assert 'id' not in data


def test_serializer_method(instance):
    data = ClassSerializer().to_dict(instance)
    assert 'A TITLE' == data['title']


def test_datetime(instance):
    dt = datetime.datetime.now()
    instance.created = dt
    data = ClassSerializer().to_dict(instance)
    assert dt.isoformat() == data['created']
