from rest_framework import viewsets

from utils.permissions import IsUserOrReadOnly

from .models import Testimonial
from .serializers import TestimonialSerializer


class TestimonialViewset(viewsets.ModelViewSet):
    """Viewset for Testimonials

    Fields:
        serializer_class: Serializer used to convert testimonials to JSON
        permission_classes: Restrict testimonials to being edited by their creators
        queryset: Queryset of Testimonial objects

    Methods:
        perform_create: Overwrite default create method to associate Testimonial with authenticated
            user

    """
    serializer_class = TestimonialSerializer
    permission_classes = (IsUserOrReadOnly,)
    queryset = Testimonial.objects.all()

    def perform_create(self, serializer):
        """
        Create new testimonial associated with the authenticated user
        """
        serializer.save(user=self.request.user)
