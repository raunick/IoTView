from django.db import models
from datetime import datetime

class MQTTMessage(models.Model):
    topic = models.CharField(max_length=255, db_index=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    sensor_type = models.CharField(max_length=255, blank=True, null=True)
    data = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    battery_level = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(default=datetime.now)
    raw_payload = models.JSONField()

    def __str__(self):
        return f"{self.device_id} - {self.topic}"

# Função para adicionar uma mensagem MQTT ao banco de dados
def add_message_to_db(message):
    try:
        message.save()
    except Exception as e:
        print(f"Erro ao adicionar mensagem: {e}")


class ActionMessage(models.Model):
    topic = models.CharField(max_length=255, db_index=True)
    device_id = models.CharField(max_length=255, blank=True, null=True)
    action_type = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=datetime.now)
    raw_payload = models.JSONField()

    def __str__(self):
        return f"Action from {self.device_id} on {self.topic}"

# Função para adicionar uma mensagem de ação ao banco de dados
def add_action_message_to_db(message):
    try:
        message.save()
    except Exception as e:
        print(f"Erro ao adicionar ação: {e}")
