
# IoTView - Sistema de Monitoramento de Sensores com MQTT

## Descrição

O **IoTView** é um sistema de monitoramento em tempo real que utiliza sensores para coletar dados e enviá-los para um broker MQTT. Ele permite que dispositivos como sensores de temperatura, umidade, movimento e módulos de relé enviem informações para um servidor, onde os dados são processados e armazenados em um banco de dados. Além disso, o sistema oferece uma interface para monitoramento de dispositivos e ações via MQTT. O backend foi desenvolvido em Django, enquanto a comunicação de sensores utiliza o protocolo MQTT.

## Funcionalidades

- **Monitoramento de Sensores**: Coleta de dados em tempo real de sensores como temperatura, umidade do ar, umidade do solo, movimento, luz e módulos de relé.
- **Ações em Tempo Real**: Possibilidade de receber e armazenar comandos de ação (como ligar/desligar dispositivos) via MQTT.
- **Suporte a MQTT**: Conexão e subscrição a tópicos MQTT para comunicação entre dispositivos e servidor.
- **Armazenamento de Dados**: Todos os dados de sensores e ações são armazenados em um banco de dados para histórico e análise.
- **Notificações e Alertas**: Geração de logs para notificações de erros e status de dispositivos.
  
## Arquitetura do Projeto

O projeto é composto por:

- **Backend**: Desenvolvido em Django, o backend é responsável pelo armazenamento de dados, gerenciamento de usuários e integração com o broker MQTT.
- **Broker MQTT**: O projeto utiliza o broker MQTT para comunicação entre dispositivos e servidor. O broker em uso é `mqtt.cool`.
- **Banco de Dados**: Armazenamento de dados de sensores e ações utilizando modelos do Django.
- **Monitoramento em Tempo Real**: Coleta e armazenamento contínuos dos dados enviados pelos sensores.

## Tecnologias Utilizadas

- **Django**: Framework web usado para criar o backend e a administração do sistema.
- **Paho MQTT**: Biblioteca para integração com o protocolo MQTT.
- **SQLite**: Banco de dados utilizado para armazenar as mensagens e ações recebidas.
- **Python**: Linguagem de programação para desenvolvimento do backend e integração com MQTT.

## Modelos

### MQTTMessage

Armazena os dados enviados pelos sensores MQTT.

- `topic`: Tópico MQTT do sensor.
- `device_id`: Identificador do dispositivo.
- `sensor_type`: Tipo de sensor (ex: `temperature`, `humidity`).
- `data`: Dados coletados pelo sensor (ex: temperatura, umidade, etc).
- `unit`: Unidade de medida do dado (`Celsius`, `%`, `lux`, etc).
- `status`: Status do sensor (`ATIVO`, `DESATIVADO`).
- `battery_level`: Nível de bateria do sensor.
- `timestamp`: Data e hora em que a mensagem foi recebida.
- `raw_payload`: Payload bruto recebido do sensor.

### ActionMessage

Armazena as ações enviadas via MQTT.

- `topic`: Tópico MQTT da ação.
- `device_id`: Identificador do dispositivo.
- `action_type`: Tipo de ação (ex: `on`, `off`).
- `status`: Status do dispositivo (`ATIVO`, `DESATIVADO`).
- `timestamp`: Data e hora em que a ação foi recebida.
- `raw_payload`: Payload bruto da ação.

## Como Usar

## 📦 PySensor-MQTT

Esta biblioteca Python foi projetada para facilitar a simulação e publicação de dados de sensores usando o protocolo MQTT. Ideal para projetos de IoT, automação e monitoramento em tempo real, a biblioteca oferece uma interface simples para a criação de diferentes tipos de sensores e a publicação de dados via um broker MQTT. 🚀

**https://pypi.org/project/PySensor-MQTT**

´´´bash
pip install PySensor-Mqtt
´´´

### Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu_usuario/IoTView.git
   cd IoTView
   ```

2. Crie um ambiente virtual e ative-o:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Windows use: venv\Scripts ctivate
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Realize as migrações do banco de dados:

   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor Django:

   ```bash
   python manage.py runserver
   ```

6. O sistema estará disponível em `http://127.0.0.1:8000`.

### Configuração do Broker MQTT

O sistema se conecta ao broker `mqtt.cool` no endereço `broker.mqtt.cool` utilizando a porta `1883`. Certifique-se de que os dispositivos estejam configurados para publicar mensagens nos tópicos corretos (ex: `sensors/#` e `action/#`).

### Tópicos Utilizados

- **sensors/#**: Usado para publicar dados de sensores.
- **action/#**: Usado para enviar comandos de ação para dispositivos.

### Exemplo de Publicação de Mensagem

Para publicar uma mensagem em um tópico MQTT, utilize o seguinte formato:

```json
{
    "device_id": "IOT_TEMPERATURE_01",
    "sensor_type": "temperature",
    "data": 26.5,
    "unit": "Celsius",
    "status": "ATIVO",
    "battery_level": 85,
    "timestamp": "2024-09-09T12:34:56+00:00"
}
```

### Exemplo de Mensagem de Ação

```json
{
    "device_id": "IOT_RELAY_01",
    "action": "on",
    "status": "ATIVO",
    "timestamp": "2024-09-09T12:34:56+00:00"
}
```

## Contribuição

Sinta-se à vontade para contribuir com este projeto. Para isso, siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature ou correção de bug (`git checkout -b minha-feature`).
3. Commit suas mudanças (`git commit -am 'Minha nova feature'`).
4. Faça um push para a branch (`git push origin minha-feature`).
5. Abra um Pull Request.

## Licença

Este projeto está sob a licença MIT. 
