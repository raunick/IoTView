from datetime import datetime
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import threading
from .models import MQTTMessage, add_message_to_db, ActionMessage, add_action_message_to_db
import paho.mqtt.client as mqtt

# Variáveis globais para armazenar mensagens MQTT
mqtt_messages = []

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, message):
    global mqtt_messages
    payload = message.payload.decode("utf-8")
    
    try:
        payload_json = json.loads(payload)
    except json.JSONDecodeError:
        print(f"Falha ao decodificar a mensagem no tópico {message.topic}: {payload}")
        return
    
    # Tratando o timestamp: verificar se é uma string
    timestamp_str = payload_json.get('timestamp')
    timestamp = None
    if isinstance(timestamp_str, str):
        try:
            timestamp = datetime.fromisoformat(timestamp_str)
        except ValueError:
            print(f"Timestamp inválido: {timestamp_str}")
            timestamp = None
    
    # Tratar campos com valores "-"
    data = payload_json.get('data')
    if data == '-':
        data = None

    battery_level = payload_json.get('battery_level')
    if battery_level == '-':
        battery_level = None

    # Se for uma mensagem de "action", armazenar na tabela ActionMessage
    if message.topic.startswith("action/"):
        action_message = ActionMessage(
            topic=message.topic,
            device_id=payload_json.get('device_id'),
            action_type=payload_json.get('action_type'),
            status=payload_json.get('status'),
            timestamp=timestamp,
            raw_payload=payload_json
        )
        add_action_message_to_db(action_message)
        print(f"Ação recebida e armazenada no banco de dados: {payload_json}")
    else:
        # Criar e armazenar uma nova instância da mensagem na tabela MQTTMessage
        new_message = MQTTMessage(
            topic=message.topic,
            device_id=payload_json.get('device_id'),
            sensor_type=payload_json.get('sensor_type'),
            data=data,
            unit=payload_json.get('unit'),
            status=payload_json.get('status'),
            battery_level=battery_level,
            timestamp=timestamp,
            raw_payload=payload_json
        )
        add_message_to_db(new_message)
        print(f"Mensagem recebida e armazenada no banco de dados: {payload_json}")
    
    mqtt_messages.append(new_message)

# Configuração do cliente MQTT
client = mqtt.Client()

# Configurações do broker
broker = 'broker.mqtt.cool'
port = 1883

# Função para conectar ao MQTT e iniciar a escuta
def start_mqtt():
    client.on_message = on_message
    client.connect(broker, port, 60)
    client.subscribe("sensors/#")
    client.subscribe("action/#")
    client.loop_forever()

# Função para rodar o cliente MQTT em um thread separado
def run_mqtt():
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

run_mqtt()  # Executa o MQTT em thread separada

# View para retornar as mensagens
def get_messages(request):
    messages = MQTTMessage.objects.all()
    return JsonResponse({"mqtt_messages": list(messages.values())})

# View para retornar as mensagens de ação
def get_action_messages(request):
    messages = ActionMessage.objects.all()
    return JsonResponse({"action_messages": list(messages.values())})

@csrf_exempt
def publish_message(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            topic = body['topic']
            payload = body['payload']
            client.publish(topic, json.dumps(payload))
            print(f"Mensagem publicada no tópico {topic}: {payload}")
            return JsonResponse({"status": "Message published", "topic": topic, "payload": payload})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
