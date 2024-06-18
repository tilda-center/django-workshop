from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, response

from v1.models import VerifyToken
from v1.serializers.verify_token import VerifyTokenSerializer


class VerifyTokenViewSet(
            viewsets.GenericViewSet,
            mixins.RetrieveModelMixin
        ):
    queryset = VerifyToken.objects.all()
    serializer_class = VerifyTokenSerializer

    def get_object(self):
        return get_object_or_404(
            VerifyToken,
            used=False,
            token=self.kwargs.get("pk"),
        )

    def update(self, request, pk):
        token = self.get_object()
        token.used = True
        token.save()
        return response.Response("Email Verified.")
