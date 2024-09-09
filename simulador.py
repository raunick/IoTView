# exemple.py
from PySensorMQTT import SensorManager, MqttParameters

def main():
    # Dados do Broker MQTT
    """
    Inicializa o gerenciamento dos sensores, adicionando-os ao
    SensorManager e iniciando a execu o dos mesmos.

    :raises: Exce o caso n o seja poss vel conectar ao broker MQTT
    """
    broker = "broker.mqtt.cool"
    porta = 1883
    topic = 'sensors'

    # Lista de sensores com seus respectivos IDs
    sensores = ['temperature', 'humidity_air', 'humidity_soil', 'light', 'motion', 'modulo_rele']
    
    # Crie uma instância do SensorManager
    manager = SensorManager()
    
    # Adicione os sensores ao SensorManager
    for sensor in sensores:
        id = f'Iot_{sensor}_01'
        device_id = id.upper()

        parameters = MqttParameters(
            broker=broker,
            port=porta,
            topic=f'{topic}/{sensor}',
            update_interval=5,  # Intervalo de atualização em segundos
            sensor_type=sensor,
            device_id=device_id  # Passando o ID do dispositivo
        )
        manager.add_sensor(parameters)
        print(f'Adicionando sensor: {sensor} com ID: {device_id}')
    
    # Inicie o gerenciamento dos sensores
    print('Sensores adicionados com sucesso!')
    print('Iniciando o gerenciamento dos sensores...')
    try:
        manager.start()
    except Exception as e:
        print(f'Erro ao iniciar o gerenciamento dos sensores: {e}')


if __name__ == "__main__":
    main()