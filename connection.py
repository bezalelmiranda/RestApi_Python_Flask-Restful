import json
import mysql.connector

with open('credentials.json') as arquivo_json:
    config = json.load(arquivo_json)


class Connection():
    def open_connection(self):
        self.connection = mysql.connector.connect(
            USER=config.get("user"),
            PASSWORD=config.get("password"),
            DATABASE=config.get("db"),
            JWT_SECRET_KEY=config.get("JWT_SECRET_KEY"),
            PORT=config.get("port"),
            HOST=config.get("ip"),
            # AUTH_PLUGIN='mysql_native_password'
        )

        self.cursor = self.connection.cursor()

        return {
            "connection": self.connection,
            "cursor": self.cursor
        }

    def close_connection(self, connection):
        connection.close()
