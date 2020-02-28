from rest_framework import serializers

from .models import Testimonial


class TestimonialSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Testimonials to JSON

    Metaclass Fields:
        model: Model to be serialized
        fields: Fields to include in serialization

    Fields:
        user: User associated with this temperature reading

    """
    user = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)

    class Meta:
        model = Testimonial
        fields = ('user', 'submission_date', 'text')
        read_only_fields = ('submission_date',)
