from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.hotel import Hoteis, Hotel
from resources.usuario import User, UserLogin, UserRegister, UserLogout
from flask_jwt_extended import JWTManager


app = Flask(__name__)
# caminho e nome do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def cria_banco():
    banco.create_all()
    # Antes da primeira requisição, cria o
    # banco e todas as tabelas(create_all())


# determina para a função verificar se o token esta ou não na blacklist
@jwt.token_in_blocklist_loader
def verifica_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    # se estiver na blacklist vai estar invalidado
    # converte um dicionario para json
    # Unauthorized
    return jsonify({'message': 'You have been logged out.'}), 401


# adiciona o rescurso para api"
api.add_resource(Hoteis, '/hoteis')
# acessa todos os hoteis do site

api.add_resource(Hotel, '/hoteis/<string:hotel_id>')  # syntax padrão
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/singup')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')

if __name__ == '__main__':
    from sql_alchemy import banco
    # só sera executado(criar o banco)
    # dentro do arquivo main e não de qualquer outro arquivo
    banco.init_app(app)
    app.run(debug=True)

# http://127.0.0.1:5000/hoteis