from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets

from v1.models import Lecture
from v1.serializers.lecture import LectureSerializer
from v1.permissions import IsProfessor


@extend_schema_view(
    list=extend_schema(tags=['lectures']),
    retrieve=extend_schema(tags=['lectures']),
    create=extend_schema(tags=['lectures']),
    update=extend_schema(tags=['lectures']),
    partial_update=extend_schema(tags=['lectures']),
    destroy=extend_schema(tags=['lectures']),
)
class ProfessorLectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    permission_classes = [IsProfessor]
