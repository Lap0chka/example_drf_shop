from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from account.serializers import UserRegisterSerializer, ProfileSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super().destroy(request, *args, **kwargs)
        return Response({"detail": "FORBIDDEN."}, status=status.HTTP_403_FORBIDDEN)

    def list(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return super().list(request, *args, **kwargs)
        return Response({"detail": "FORBIDDEN."}, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if self.request.user.is_staff or user == self.request.user:
            serializer = self.get_serializer(user, data=request.data,
                                             partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "FORBIDDEN."}, status=status.HTTP_403_FORBIDDEN)




