from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE")

client = None
db = None


async def connect_to_db():
    """Conecta ao MongoDB com validação por ping."""
    global client, db
    if not MONGO_URI or not MONGO_INITDB_DATABASE:
        raise ValueError("As variáveis de ambiente MONGO_URI e MONGO_INITDB_DATABASE devem estar configuradas.")

    if client:
        print("Já conectado ao MongoDB.")
        return

    try:
        print("Tentando conectar ao MongoDB...")
        client = AsyncIOMotorClient(MONGO_URI)
        # Testa a conexão com um ping
        await client.admin.command("ping")
        db = client[MONGO_INITDB_DATABASE]
        print("Conexão com o MongoDB validada e estabelecida.")
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        raise


async def close_db_connection():
    """Fecha a conexão com o MongoDB."""
    global client
    if client:
        client.close()
        print("Conexão com o MongoDB encerrada")
        client = None
    else:
        print("Nenhuma conexão com o MongoDB para encerrar.")

def parse_obj_id(item):
    """Converte ObjectId para string no documento."""
    if isinstance(item, list):
        return [{**doc, "_id": str(doc["_id"])} for doc in item]
    elif isinstance(item, dict):
        item["_id"] = str(item["_id"])
        return item
    return item
   
# Lifespan gerador assíncrono
async def lifespan(app):
    # Executa na inicialização
    await connect_to_db()
    yield  # Permite que a aplicação execute
    # Executa no encerramento
    await close_db_connection()
