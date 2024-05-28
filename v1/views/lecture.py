from rest_framework import viewsets

from v1.models import Lecture
from v1.serializers.lecture import LectureSerializer
from v1.permissions import IsProfessor

class ProfessorLectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    queryset = Lecture.objects.all()
    permission_classes = [IsProfessor]
