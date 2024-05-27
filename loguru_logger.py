import socket
from loguru import logger

# IP_INFO=socket.getnameinfo()
HOST=socket.gethostname()

logger.add(
    "./logs_of_app.log",
    format="{level} \\ {time:YYYY-MM-DD at HH:mm:ss} \\ {file} -> line {line} \\ {message} \\ HOST: " + HOST,
)