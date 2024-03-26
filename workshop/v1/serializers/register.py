from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.db.utils import IntegrityError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User 
        fields = ["password", "first_name", "last_name", "email"]
        
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def save(self):
        password = self.validated_data.pop("password")
        self.validated_data["username"] = self.validated_data["email"]
        try:
         user = super().save()
        except IntegrityError:
           raise serializers.ValidationError("User with this email already exists")
            
        user.set_password(password)
        
        group, _ = Group.objects.get_or_create(name="student")
        user.groups.add(group)
                    
        user.save()
        