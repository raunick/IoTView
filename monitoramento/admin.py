from django.contrib import admin
from .models import ActionMessage, MQTTMessage

@admin.register(MQTTMessage)
class MQTTMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'device_id', 'sensor_type', 'data', 'unit', 'status', 'battery_level', 'timestamp')
    search_fields = ('topic', 'device_id')

@admin.register(ActionMessage)
class ActionMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic', 'device_id', 'action_type', 'status', 'timestamp')
    search_fields = ('topic', 'device_id', 'action_type')