import datetime
from datetime import timedelta
from django.db import transaction
from rest_framework import serializers

from v1.models import Event, Lecture


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = [
            "start",
            "end",
            "info",
            "lecture_id"
        ]

    def create(self, validated_data):
        validated_data['lecture_id'] = self.context['lecture_pk']
        #with transaction.atomic():
        self.instance = super().create(validated_data)
        return self.instance

    # TODO: validate information by the agreed rules
    # def validate(self):
    #
    #     data = self.validated_data
    #     start = data.get("start")
    #     end = data.get("end")
    #     info = data.get("info")
    #
    #     if start is not None and end is not None:
    #         if start > end:
    #             raise serializers.ValidationError(
    #                 ("Start time and end time count mismatch")
    #             )
    #     lecture_id = self.context['lecture_pk']  # self.context['view'].kwargs['lecture_pk']
    #     lecture = Lecture.objects.filter(pk=lecture_id).first()
    #     if not (lecture := Lecture.objects.filter(pk=lecture_id).first()):
    #         raise serializers.Val
    #
    #
    #     return data
