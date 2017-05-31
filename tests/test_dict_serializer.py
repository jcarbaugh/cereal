import datetime
import logging

import pytest

import cereal


logger = logging.getLogger('cereal.tests')


@pytest.fixture
def datadict():
    return {
        'id': 3,
        'title': 'A Title',
        'content': 'jk not a post',
        'created': datetime.datetime.now(),
    }


class DictSerializer(cereal.Serializer):
    exclude = ('id',)
    title = cereal.Field()
    content = cereal.Field()
    created = cereal.Field()

    def serialize_title(self, obj):
        return obj['title'].upper()


def test_exclude(datadict):
    data = DictSerializer().serialize(datadict)
    assert 'id' not in data


def test_serializer_method(datadict):
    data = DictSerializer().serialize(datadict)
    assert 'A TITLE' == data['title']


def test_datetime(datadict):
    data = DictSerializer().serialize(datadict)
    assert datadict['created'].isoformat() == data['created']
