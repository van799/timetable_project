from rest_framework import serializers
from .models import Event, SecurityType


class EventSerializer(serializers.ModelSerializer):
    """Класс сериализации для FullCalendar."""
    title = serializers.StringRelatedField(read_only=True)
    start = serializers.SerializerMethodField("get_start")
    type_security = serializers.StringRelatedField(read_only=True)

    def get_start(self, obj):
        return obj.start_date

    class Meta:
        model = Event
        fields = ('title', 'start', 'type_security')
