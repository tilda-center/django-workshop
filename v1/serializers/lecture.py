from rest_framework import serializers
from v1.models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    professor = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = [
            "title",
            "info",
            "professor",
        ]

    def get_professor(self, obj):
        return obj.professor.first_name + " " + obj.professor.last_name

    def create(self, validated_data):
        validated_data["professor"] = self.context["request"].user
        return super().create(validated_data)

