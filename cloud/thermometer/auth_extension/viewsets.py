from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from utils.permissions import IsOwnerOrReadOnly, IsSelfOrAdmin, IsUserOrReadOnly

from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer


class UserViewset(viewsets.ModelViewSet):
    """Viewset for Users

    Fields:
        queryset: list of users ordered by pk
        serializer_class: serializer used to represent users
        permission_classes: restrictions on who can access detail view
    """

    queryset = get_user_model().objects.all().order_by('pk')
    serializer_class = UserSerializer
    permission_classes = (IsSelfOrAdmin,)


class UserProfileViewset(viewsets.ModelViewSet):
    """
    Viewset for User Profiles.
    """

    queryset = UserProfile.objects.all().order_by('created_date')
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsUserOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
