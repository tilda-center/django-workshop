import datetime
from datetime import timedelta
from django.db import transaction
from rest_framework import serializers

from v1.models import Lecture, Event


class EventSerializer(serializers.Serializer):
    DATEYPE_INTERVAL_CHOICE = ("day", "week", "month")
    type = serializers.ChoiceField(
        choices=DATEYPE_INTERVAL_CHOICE,
        required=False,
        default="day",
    )

    # week case
    weekdays = serializers.ListField(
        child=serializers.IntegerField(), required=False)

    # month case
    dates = serializers.ListField(
        child=serializers.DateTimeField(), required=False)

    # times on the day
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    # max value one year.
    first_date = serializers.DateField(required=False)
    last_date = serializers.DateField(required=False)

    def validate(self, data):
        # we neeed comprehenisve validation
        return data

    def initialize_event(self, *args, **kwargs):
        if self.context.get("queryset"):
            if not self.context.get("queryset").filter(
                lecture=kwargs["lecture"],
                start=kwargs["start"],
                end=kwargs["end"]
            ).exists():
                return Event(**{
                    "lecture": kwargs["lecture"],
                    "start": kwargs["start"],
                    "end": kwargs["end"]
                })
            else:
                pass
        else:
            return Event(**{
                "lecture": kwargs["lecture"],
                "start": kwargs["start"],
                "end": kwargs["end"]
            })

    def make_events(self):
        data = self.validated_data

        dates = data.get("dates", [])
        weekdays = data.get("weekdays", [])
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        first_date = data.get("first_date")
        last_date = data.get("last_date")
        choice = data.get("type")

        if first_date is None:
            first_date = datetime.now()

        if first_date is not None and last_date is not None:
            if first_date > last_date:
                raise serializers.ValidationError(
                    ("Start dates and end dates count mismatch")
                )

        intervals = []
        start_time = datetime.combine(first_date, start_time)
        end_time = datetime.combine(first_date, end_time)
        duration = end_time - start_time

        if choice == "day":
            pivot_date = datetime.combine(first_date, start_time.time())
            while pivot_date.date() < last_date:
                intervals.append(self.initialize_event(
                    **{
                        "lecture": self.context["lecture"],
                        "start": pivot_date,
                        "end": (pivot_date + duration),
                    })
                )
                pivot_date = pivot_date + timedelta(days=1)

        elif choice == "week":
            for weekday in weekdays:
                pivot_date = datetime.combine(first_date, start_time.time())

                # Calculate days until next day of the week
                days_ahead = (weekday - pivot_date.weekday() + 7) % 7
                next_day_of_the_week = pivot_date + \
                    timedelta(days=days_ahead)

                # Move to the next day of the week
                while next_day_of_the_week.date() < last_date:
                    intervals.append(
                        self.initialize_event(**{
                            "lecture": self.context["lecture"],
                            "start": next_day_of_the_week,
                            "end": (
                                next_day_of_the_week + duration
                            ),
                        })
                    )
                    next_day_of_the_week = (
                        next_day_of_the_week + timedelta(days=7)
                    )

        elif choice == "month":
            for date in dates:
                pivot_date = datetime.combine(date, start_time.time())
                while pivot_date.date() <= last_date:
                    intervals.append(
                        self.initialize_event(**{
                            "lecture": self.context["lecture"],
                            "start": pivot_date,
                            "end": (
                                pivot_date + duration
                            ),
                        })
                    )
                    pivot_date += timedelta(days=35)
        else:
            raise NotImplementedError

        Event.objects.bulk_create(intervals)

        return intervals


class LectureSerializer(serializers.ModelSerializer):
    events = EventSerializer(write_only=True, required=False)
    time_preset = serializers.ChoiceField(
        choices=(
            ("every_day", "every_day"),
            ("every_working_day", "every_working_day"),
            ("every_weekend", "every_weekend"),
            ("every_week_on_day", "every_week_on_day"),
            ("custom", "custom"),
        ),
        required=False,
    )
    professor = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = [
            "title",
            "info",
            "professor",
            "time_preset",
            "events",
        ]

    def get_professor(self, obj):
        return obj.professor.first_name + " " + obj.professor.last_name

    def create(self, validated_data):
        validated_data["professor"] = self.context["request"].user
        self.events = validated_data.pop('events', [])
        self.time_preset = validated_data.pop('time_preset', [])

        with transaction.atomic():
            self.instance = super().create(validated_data)
            self.override_events(self.instance)

        return self.instance

    def update(self, validated_data):
        validated_data["professor"] = self.context["request"].user
        # TODO: obrisi sve ostale eventove u buducnosti

        self.events = validated_data.pop('events', [])
        self.time_preset = validated_data.pop('time_preset', [])

        with transaction.atomic():
            self.instance = super().update(validated_data)
            self.override_events(self.instance)

        return self.instance

    def override_events(self, lecture):
        if self.time_preset:
            self.events.update(self.generate_preset_events(self.time_preset))

        events_serializer = EventSerializer(
            data=self.events, context={"lecture": lecture}
        )
        events_serializer.is_valid()
        events_serializer.make_events()

    def generate_preset_events(self, preset):
        if preset == "every_day":
            return {
                "type": "day",
            }
        elif preset == "every_working_day":
            return {
                "type": "week",
                "weekdays": [0, 1, 2, 3, 4]
            }
        elif preset == "every_weekend":
            return {
                "type": "week",
                "weekdays": [5, 6]
            }
        elif preset == "every_week_on_day":
            return {
                "type": "week",
                "weekdays": [
                    self.validated_data["events"]["first_date"].weekday()
                ]
            }
        else:
            return {}
