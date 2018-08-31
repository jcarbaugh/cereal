import cereal
# import pytest
# import sys
# from tests.testapp.models import Post, Comment


def test_field():

    class FieldSerializer(cereal.Serializer):
        foo = cereal.Field()

    data = FieldSerializer().asdict_(None)
    assert data['foo'] is None


def test_field_from_attr():

    class FieldSerializer(cereal.Serializer):
        bar = cereal.Field(from_attr='foo')

    data = FieldSerializer().asdict_({
        'foo': 'cereal',
    })
    assert data['bar'] == 'cereal'


# @pytest.mark.skipif(sys.version_info < (3, 6),
#                     reason="requires python3.6")
# def test_annotated_field():

#     class FieldSerializer(cereal.Serializer):
#         foo: int

#     fs = FieldSerializer()
#     fs.defined_fields['foo'].__class__ is cereal.Field


def test_constant_field():

    value = 'bar'

    class ConstantSerializer(cereal.Serializer):
        foo = cereal.ConstantField(value)

    data = ConstantSerializer().asdict_(None)
    assert data['foo'] == value


def test_iterator_generator_field():

    def gen():
        value = 0
        while 1:
            yield value
            value += 1

    class IteratorSerializer(cereal.Serializer):
        foo = cereal.IteratorField(gen())

    ser = IteratorSerializer()

    data = ser.asdict_(None)
    assert data['foo'] == 0

    data = ser.asdict_(None)
    assert data['foo'] == 1


def test_iterator_list_field():

    class IteratorSerializer(cereal.Serializer):
        foo = cereal.IteratorField([0])

    ser = IteratorSerializer()

    data = ser.asdict_(None)
    assert data['foo'] == 0

    data = ser.asdict_(None)
    assert data['foo'] is None


def test_serializer_field():

    class ClassyClass():
        def __init__(self, *args, **kwargs):
            self.__dict__.update(kwargs)

    class InnerSerializer(cereal.Serializer):
        foo = cereal.Field()

    class OuterSerializer(cereal.Serializer):
        foo = cereal.SerializerField(InnerSerializer)

    obj = ClassyClass(foo=ClassyClass(foo='bar'))
    data = OuterSerializer().asdict_(obj)
    assert isinstance(data['foo'], dict)
    assert data['foo']['foo'] == 'bar'


def test_serializer_field_list():

    class ClassyClass():
        def __init__(self, *args, **kwargs):
            self.__dict__.update(kwargs)

    class InnerSerializer(cereal.Serializer):
        foo = cereal.Field()

    class OuterSerializer(cereal.Serializer):
        foo = cereal.SerializerField(InnerSerializer)

    obj = ClassyClass(foo=[ClassyClass(foo='bar'), ClassyClass(foo='baz')])
    data = OuterSerializer().asdict_(obj)
    assert isinstance(data['foo'], list)
    assert data['foo'][0]['foo'] == 'bar'
    assert data['foo'][1]['foo'] == 'baz'


# def test_serializer_field_m2m(db):
#
#     class CommentSerializer(cereal.Serializer):
#         model = Comment
#
#     class PostSerializer(cereal.Serializer):
#         model = Post
#         comments = cereal.SerializerField(CommentSerializer)
#
#     obj = Post.objects.create(title='TITLE', content='CONTENT')
#     Comment.objects.create(username='j', post=obj)
#     Comment.objects.create(username='c', post=obj)
#     obj.refresh_from_db()
#
#     print(obj.comments)
#
#     data = PostSerializer().serialize(obj)
#
#     assert data['title'] == 'TITLE'
#     assert data['comments'] == 'comments'
