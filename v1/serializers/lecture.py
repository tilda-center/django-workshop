from rest_framework import serializers
from v1.models import Lecture


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        read_only_fields = ["professor"]
        fields = [
            "title",
            "info",
        ]

    def create(self, validated_data):
        validated_data["professor"] = self.context["request"].user
        return super.create(validated_data)

