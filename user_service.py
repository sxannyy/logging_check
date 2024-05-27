from fastapi import FastAPI
from hashlib import sha256
from datetime import datetime
from loguru_logger import logger


main_service_app = FastAPI()

logger.info("Сервер был успешно запущен")

all_tokens = []

@main_service_app.get('/get_token')
async def get_token():
    token = sha256(str(datetime.now()).encode('utf-8')).hexdigest()
    #token = 123 # при проверке одинаковых токенов
    logger.info("Метод get_token находится в действии ")
    check_all_tokens(token)
    all_tokens.append(token)
    return{token}

def check_all_tokens(token):
    if token in all_tokens:
        logger.error("Этот токен уже существует в базе!")
