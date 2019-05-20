import datetime
import logging

import pytest

import cereal
from .testapp.models import Post


logger = logging.getLogger('cereal.tests')


@pytest.fixture
def post():
    return Post(id=1, title='A Title', content='jk not a post')


class PostSerializer(cereal.Serializer):
    a_dict = cereal.Field()
    a_list = cereal.Field()

    class Meta:
        model = Post

    def serialize_title(self, obj):
        return obj.title.upper()


class PostSerializerWithID(PostSerializer):
    id = cereal.Field()


class RestrictedPostSerializer(PostSerializer):
    id = cereal.Field()
    exclude = ('content',)

    class Meta:
        model = Post


class ClonedPostSerializer(PostSerializer):
    pass


def test_exclude_id(post):
    data = PostSerializer().asdict_(post)
    assert 'id' not in data


def test_include_id(post):
    data = PostSerializerWithID().asdict_(post)
    assert 'id' in data


def test_serializer_method(post):
    data = PostSerializer().asdict_(post)
    assert 'A TITLE' == data['title']


def test_datetime(post):
    dt = datetime.datetime.now()
    post.created = dt
    data = PostSerializer().asdict_(post)
    assert dt.isoformat() == data['created']


def test_model_serializer_inheritance(post):
    data = RestrictedPostSerializer().asdict_(post)
    assert 'A TITLE' == data['title']


def test_inheritance_override_exclude(post):
    data = RestrictedPostSerializer().asdict_(post)
    assert 'content' not in data
    assert 1 == data['id']


def test_inheritance_exclude_from_parent(post):
    data = ClonedPostSerializer().asdict_(post)
    assert 'id' not in data


def test_inheritance_Meta_from_parent(post):
    data = ClonedPostSerializer().asdict_(post)
    assert 'A TITLE' == data['title']
