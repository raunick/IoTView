from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./mqtt_messages.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do banco de dados
class MQTTMessage(Base):
    __tablename__ = "mqtt_messages"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    device_id = Column(String)
    sensor_type = Column(String)
    data = Column(Float)
    unit = Column(String)
    status = Column(String)
    battery_level = Column(Integer)
    timestamp = Column(DateTime)
    raw_payload = Column(JSON)

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Função para adicionar a mensagem ao banco de dados
def add_message_to_db(message):
    db = SessionLocal()
    try:
        db.add(message)
        db.commit()
        db.refresh(message)
    except Exception as e:
        db.rollback()
        print(f"Erro ao adicionar mensagem: {e}")
    finally:
        db.close()
