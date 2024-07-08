from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from v1.models import Event
from v1.serializers.event import EventSerializer
from v1.permissions import IsProfessor



@extend_schema_view(
    list=extend_schema(tags=['events']),
    retrieve=extend_schema(tags=['events']),
    create=extend_schema(tags=['events']),
    update=extend_schema(tags=['events']),
    partial_update=extend_schema(tags=['events']),
    destroy=extend_schema(tags=['events']),
)
class ProfessorEventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsProfessor]

    def get_queryset(self):
        lecture_id = self.kwargs['lecture_pk']
        test = super().get_queryset().filter(
            lecture_id=lecture_id,
            lecture__professor=self.request.user,
        )
        return super().get_queryset().filter(
            lecture_id=lecture_id,
            lecture__professor=self.request.user,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["lecture_pk"] = self.kwargs['lecture_pk']
        return context

    def get_object(self):
        obj = get_object_or_404(Event,
                                id=self.kwargs['pk'],
                                lecture_id=self.kwargs['lecture_pk'],
                                lecture__professor=self.request.user,
                                )
        self.check_object_permissions(self.request, obj)

        return obj
