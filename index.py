from flask_restful import Resource
# Endpoint de login


class Index(Resource):

    # Funcao chamada que chama as demais funcoes
    def get(self):
        return {
            "msg": "server online"
        }
