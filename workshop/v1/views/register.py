from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from v1.serializers.register import RegisterSerializer
from v1.serializers.login import MyTokenObtainPairSerializer

class RegisterViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        data = {
            "username": request.data['email'],
            "password": request.data['password']
            
        }
        serializer = MyTokenObtainPairSerializer(data=data)
        serializer.is_valid()
        return Response(serializer.validated_data)
    
    