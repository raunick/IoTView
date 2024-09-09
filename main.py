import json
import threading
from datetime import datetime
from fastapi import FastAPI
from contextlib import asynccontextmanager
import paho.mqtt.client as mqtt
from database import MQTTMessage, add_message_to_db, SessionLocal

app = FastAPI()

# Variáveis globais para armazenar mensagens MQTT
mqtt_messages = []

# Função chamada quando uma mensagem é recebida
def on_message(client, userdata, message):
    global mqtt_messages
    # Decodificando a mensagem
    payload = message.payload.decode("utf-8")
    
    try:
        # Tentar converter o payload para JSON
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
    
    # Tratar campos com valores "-": convertendo para None ou valores padrão
    data = payload_json.get('data')
    if data == '-':
        data = None  # Ou coloque um valor padrão, por exemplo, 0

    battery_level = payload_json.get('battery_level')
    if battery_level == '-':
        battery_level = None  # Ou um valor padrão

    # Atualizar status no banco de dados se for uma mensagem de "action"
    if message.topic.startswith("action/"):
        db = SessionLocal()
        device_id = payload_json.get('device_id')
        # Buscar o dispositivo e atualizar o status
        device = db.query(MQTTMessage).filter_by(device_id=device_id).first()
        if device:
            device.status = payload_json.get('status', device.status)  # Atualizar o status
            db.commit()
        db.close()

    # Criando uma nova instância da mensagem para o banco de dados
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
    
    # Adicionar ao banco de dados
    add_message_to_db(new_message)
    
    # Log para verificar a recepção das mensagens
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

    # Inscrever-se em tópicos
    client.subscribe("sensors/#")
    client.subscribe("action/#")

    client.loop_forever()

# Usando o Lifespan para eventos de ciclo de vida
@asynccontextmanager
async def lifespan(app: FastAPI):
    # No startup, iniciar o MQTT
    run_mqtt()
    yield
    # No shutdown, desconectar o cliente MQTT
    client.disconnect()

# Criar a aplicação FastAPI usando lifespan
app = FastAPI(lifespan=lifespan)

# Rota para retornar as mensagens do banco de dados
@app.get("/messages")
async def get_messages():
    db = SessionLocal()
    try:
        messages = db.query(MQTTMessage).all()
        return {"mqtt_messages": messages}
    finally:
        db.close()

# Rota para publicar uma mensagem em um tópico MQTT
@app.post("/publish")
async def publish_message(topic: str, payload: dict):
    client.publish(topic, json.dumps(payload))
    print(f"Mensagem publicada no tópico {topic}: {payload}")
    return {"status": "Message published", "topic": topic, "payload": payload}

# Função para rodar o cliente MQTT em um thread separado
def run_mqtt():
    mqtt_thread = threading.Thread(target=start_mqtt)
    mqtt_thread.daemon = True
    mqtt_thread.start()

# Executar a aplicação com uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
