from itertools import count
import cereal

class ThingSerializer(cereal.Serializer):
    id = cereal.Field()
    offset = cereal.IteratorField(count())

print(ThingSerializer().serialize({'id': 1}))
print(ThingSerializer().serialize({'id': 2}))