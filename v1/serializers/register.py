from django.db.utils import IntegrityError
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from rest_framework import serializers

from v1.models import VerifyToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["password", "first_name", "last_name", "email"]
        extra_kwargs = {"email": {"required": True}}

    def validate_password(self, value):
        validate_password(value)
        return value

    def save(self):
        password = self.validated_data.pop("password")
        self.validated_data["username"] = self.validated_data["email"]
        try:
            user = super().save()
        except IntegrityError:
            raise serializers.ValidationError("User email already exists.")
        user.set_password(password)
        group, _ = Group.objects.get_or_create(name="student")
        verify_token = VerifyToken.objects.create(
                email=self.validated_data["email"]
        )
        self.send_welcome_email(
            self.validated_data["email"],
            verify_token.token,
        ) 
        user.groups.add(group)
        user.save()

    def send_welcome_email(self, email, verify_token):
        subject = 'Welcome to My Site'
        message = f'{verify_token}'
        from_email = 'admin@mysite.com' 
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
