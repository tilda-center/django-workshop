from rest_framework import serializers

from v1.models import VerifyToken


class VerifyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyToken
        fields = ['email', 'token']
