from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .users import UserSerializer  # Ensure this serializer is tailored for profile-related fields

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]  # Adjust permissions as necessary

    def retrieve(self, request, pk=None):
        """
        Retrieve the profile of the authenticated user or a specific user by ID.
        """
        if pk == 'me':
            user = request.user
        else:
            user = get_object_or_404(User, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)