import json

with open('credentials.json') as arquivo_json:
    config = json.load(arquivo_json)

USER = config.get("user")
PASSWORD = config.get("password")
DATABASE = config.get("db")
JWT_SECRET_KEY = config.get("JWT_SECRET_KEY")
PORT = config.get("port")
HOST = config.get("ip")
