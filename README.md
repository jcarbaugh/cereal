# Cereal

[![CircleCI](https://circleci.com/gh/istrategylabs/cereal.svg?style=svg)](https://circleci.com/gh/istrategylabs/cereal)

Serialize objects, dicts, and [Django models](https://djangoproject.com)  to JSON with ease.

I occasionally need to make very small APIs, maybe just an endpoint or two to provide a bit of data to a client. It always seems like overkill to use Django REST framework when a simple View will do. Unfortunately, the DRF serializer is really good and hand coding an object-to-JSON map can be fragile and gross. Cereal was created to be that trusty serializer when that's all you need.



## Installation

Cereal is available on [PyPI](https://pypi.org/project/pycereal):

```shell
pip install pycereal
```

or

```shell
pipenv install pycereal
```



## Serializers

### Fields

If you've ever used Django's [ModelForms](https://docs.djangoproject.com/en/2.0/topics/forms/modelforms/), Cereal should seem fairly familiar to you. A Serializer defines a set of attributes (Fields) that will be… serialized… into JSON.

```python
import cereal

class ArticleSerializer(cereal.Serializer):
    title = cereal.Field()

data = {
    'id': 1,
    'title': 'An Important Headline',
}

ArticleSerializer().serialize(data)
```

This will result in the JSON object:

```json
{
    "title": "An Important Headline"
}
```

### Customizing fields

Sometimes there's a need to transform a value before it is converted to JSON. Cereal provides an opportunity to hook into serialization by adding methods named with the `serialize_<field>` format. The method will receive the data structure that is being serialized as the sole argument.

```python
import cereal

class ArticleSerializer(cereal.Serializer):
    title = cereal.Field()

    def serialize_title(self, obj):
        return obj['title'].upper()

data = {
    'id': 1,
    'title': 'An Important Headline',
}

ArticleSerializer().serialize(data)
```

Which will generate:

```shell
{
    "title": "AN IMPORTANT HEADLINE"
}
```

The field methods can also be used to create completely new values.

```python
import cereal

class AuthorSerializer(cereal.Serializer):
    full_name = cereal.Field()

    def serialize_full_name(self, obj):
        return f"{obj['first_name']} {obj['last_name']}"

data = {
    'first_name': 'Corey',
    'last_name': 'Spaceman',
}

AuthorSerializer().serialize(data)
```

The generated JSON:

```json
{
    "full_name": "Corey Spaceman"
}
```

The JSON only includes the custom *full_name* Field, which is computed using the *serialize_full_name* method, and not the *first_name* or *last_name* attributes. Of course, you can include all of the attributes too by defining them as Fields as well.

### Serializing objects

The examples so far have involved serializing a dict to JSON, but the *json* module already does this, so what's the point? Cereal handles objects the exact same way as it does dicts.

```python
import cereal

class Article:
    def __init__(self, _id, title):
        self.id = _id
        self.title = title

class ArticleSerializer(cereal.Serializer):
    title = cereal.Field()

obj = Article(1, 'An Important Headline')
ArticleSerializer().serialize(obj)
```

The resulting JSON shouldn't be much of a surprise.

```json
{
    "title": "An Important Headline"
}
```

### Nested attributes

The world is an imperfect place and not all of your data will be in a simple, flat structure. SerializerField can be used to attach another serializer to handle a nested data structure.

```python
import cereal

class UserSerializer(cereal.Serializer):
    name = cereal.Field()

class ArticleSerializer(cereal.Serializer):
    title = cereal.Field()
    author = cereal.SerializerField(UserSerializer)

data = {
    'id': 1,
    'title': 'An Important Headline',
    'author': {
        'id': 2,
        'name': 'Corey',
    }
}

ArticleSerializer().serialize(data)
```

```json
{
    "title": "An Important Headline",
    "author": {
        "name": "Corey"
    }
}
```

### Dates and datetimes

If you've spent much time with the *json* module, you're probably quite familiar with date serialization errors. JSON does not have native support for dates, so they have to be transformed into string values, but *json* doesn't do this automatically. Cereal has built-in support for dates and datetimes, generating ISO 8601-formatted strings that will be used as the value.

```python
import datetime
import cereal

class EventSerializer(cereal.Serializer):
    timestamp = cereal.Field()

data = {
    'timestamp': datetime.datetime(2018, 3, 8, 11, 57, 23, 129307)
}

EventSerializer().serialize(data)
```

```json
{
    "timestamp": "2018-03-08T11:57:23.129307"
}
```

### Custom type handlers

As with dates, other data types outside of what is natively supported by JSON need to be converted to one of the native types during serialization. Cereal allows you to define handlers for additional data types to convert to a valid JSON format. The handler is a callable that receives the value and returns a value corresponding to a native JSON type.

```python
import uuid
import cereal

def uuid_handler(u):
    return u.hex

class UUIDSerializer(cereal.Serializer):
    id = cereal.Field()

ser = UUIDSerializer()
ser.add_handler(uuid.UUID, uuid_handler)
ser.serialize({'id': uuid.uuid4()})
```

You guessed it, the JSON:

```json
{
    "id": "45ebb187dbc240cabb07b775f63efd6f"
}
```

### Single value vs. list of values

When serializing an attribute, the content can either be a single value or an array of values. The corresponding JSON will likewise be either a single value or an array of values. All of the values of the array will be transformed the same way an individual value would be, either through the default Field behavior, using the custom serialization method, the default SerializerField behavior, or a custom type handler. To be safe, just make sure all items in the array are of the same type and that type would serialize correctly as a single value.



## Special Fields

### Constants

The ConstantField allows you to insert a new, constant value into the JSON.

```python
import cereal

class HumanSerializer(cereal.Serializer):
    name = cereal.Field()
    wants_tacos = cereal.ConstantField(True)

data = {
    'name': 'Corey Spaceman',
}

HumanSerializer().serialize(data)
```

```json
{
    "name": "Corey Spaceman",
    "wants_tacos": true
}
```

### Iterators

The IteratorField allows you to define a generator, use a list, or pass any type of iterable that will be used to generate values. Each serialized object will pull a new value from the iterator. If the iterator is exhausted, *None* will be used.

```python
from itertools import count
import cereal

class ThingSerializer(cereal.Serializer):
    id = cereal.Field()
    offset = cereal.IteratorField(count())

ser = ThingSerializer()
ser.serialize({'id': 1})
ser.serialize({'id': 2})
```

```json
{
    "id": 1,
    "offset": 0
}
{
    "id": 2,
    "offset": 1
}
```



## Django Model Serialization

While Cereal is usable in any Python project, I really made it to be used with Django projects. So, given my previous mention of being inspired by Django ModelForms, Cereal allows you to define a model that automatically defines the fields that will be serialized.

```python
import cereal
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=128)

class PostSerializer(cereal.Serializer):
    exclude = ('id',)

    class Meta:
        model = Post

post = Post.objects.create(title='Breaking News')
PostSerializer().serialize(post)
```

```json
{
    "title": "Breaking News"
}
```

In this example, we're inheriting the fields of the Post model, but excluding the *id*.

Beyond incorporating the fields from the model, the Serializer functions the same as any other non-model Serializer. You can define additional Fields and custom field serializer methods that modify both model fields and any others.

## Deserialization

You may be wondering "What about deserialization?" Well, I had no need for it, so I didn't build it. Contributions are welcome, though!
