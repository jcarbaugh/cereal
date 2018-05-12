import datetime
import logging

import pytest

import cereal
from .testapp.models import Post


logger = logging.getLogger('cereal.tests')


@pytest.fixture
def post():
    return Post(title='A Title', content='jk not a post')


class PostSerializer(cereal.Serializer):
    exclude = ('id',)
    a_dict = cereal.Field()
    a_list = cereal.Field()

    class Meta:
        model = Post

    def serialize_title(self, obj):
        return obj.title.upper()


def test_exclude(post):
    data = PostSerializer().asdict_(post)
    assert 'id' not in data


def test_serializer_method(post):
    data = PostSerializer().asdict_(post)
    assert 'A TITLE' == data['title']


def test_datetime(post):
    dt = datetime.datetime.now()
    post.created = dt
    data = PostSerializer().asdict_(post)
    assert dt.isoformat() == data['created']
