from django.contrib.auth import get_user_model
from rest_framework import serializers

from .fields import TimeZoneField
from .models import UserProfile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to convert Users to JSON.

    Fields:
        profile: User's profile data

    Metaclass Fields:
        model: model to be serialized
        fields: fields to include in serialization
        read_only_fields: specifies which fields can't be written to via API
        extra_kwargs:
            password: set password so it is write-only. No one should be
                allowed to see any user's password hash

    Methods:
        create: Upon creation, new User should have a blank profile associated
            with it.

    References:
        * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """
    profile = serializers.HyperlinkedRelatedField(
        many=False, view_name='userprofile-detail', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('url', 'id', 'username',
                  'profile', 'email', 'password')
        read_only_fields = ('is_staff', 'is_superuser',
                            'is_active', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """
        Create new User object, as well as an associated Profile Object
        with blank fields.
        """

        user = get_user_model().objects.create_user(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=validated_data.get('password'))
        return user

    def update(self, instance, validated_data):
        """
        Update passwords via `User.set_password` method. Update
        other fields normally.
        """

        if validated_data.get('username'):
            instance.username = validated_data.get('username')

        if validated_data.get('email'):
            instance.email = validated_data.get('email')

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))

        instance.save()
        return instance


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """Seralizer for User Profiles.

    Fields:
        user: related User object
        model: model to be serialized
        fields: fields to include in serialization

    References:
            * http://www.django-rest-framework.org/tutorial/1-serialization/#using-Hyperlinkedmodelserializers

    """

    user = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)
    time_zone = TimeZoneField()

    class Meta:
        model = UserProfile
        fields = ('url', 'user', 'created_date', 'time_zone', 'picture')
        extra_kwargs = {
            'slug': {'read_only': True},
        }