import traceback
from flask import make_response, render_template
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.usuario import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import jwt_required, get_jwt

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True,
                       help="The field 'login' cannot be left blank.")
atributos.add_argument('senha', type=str, required=True,
                       help="The field 'senha' cannot be left blank.")
atributos.add_argument('email', type=str)
atributos.add_argument('ativado', type=bool)

# /usuarios/{user_id}


class User(Resource):
    # argumentos = reqparse.RequestParser()
    # # Tratamento de erros
    # argumentos.add_argument('nome', type=str, required=True,
    #                         help="The field 'nome' cannot be left blank.")
    # argumentos.add_argument('estrelas')
    # argumentos.add_argument('diaria')
    # argumentos.add_argument('cidade', type=str, required=True,
    #                         help="The field 'cidade' cannot be left blank.")

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404  # statusCode not found

    # def post(self, hotel_id):
    #     if HotelModel.find_hotel(hotel_id):
    #         return {'message': 'Hotel id "{}" already exists.'
    #                 .format(hotel_id)}, 400  # bad resquest

    #     # construtor
    #     dados = Hotel.argumentos.parse_args()
    #     hotel = HotelModel(hotel_id, **dados)
    #     try:
    #         hotel.save_hotel()
    #     except Exception:
    #         return {'message': 'An internal error\
    #              ocurred trying to save hotel.'}, 500
    #     return hotel.json()

    # def put(self, hotel_id):

    #     dados = Hotel.argumentos.parse_args()
    #     hotel_encontrado = HotelModel.find_hotel(hotel_id)
    #     if hotel_encontrado:
    #         hotel_encontrado.update_hotel(**dados)
    #         hotel_encontrado.save_hotel()  # sava no banco
    #         return hotel_encontrado.json(), 200  # OK
    #     hotel = HotelModel(hotel_id, **dados)
    #     # Tratamento de erros
    #     try:
    #         hotel.save_hotel()
    #     except Exception:
    #         return {'message': 'An internal error\
    #              ocurred trying to save hotel.'}, 500
    #         # Internal Server Error
    #     return hotel.json(), 201  # created = criado

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except Exception:
                return {'message': 'An error\
                    ocurred trying to delete user.'}, 500
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

# /singup


class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()
        # Verifica se o campo email foi cadastrado ou é nulo
        if not dados.get('email') or dados.get('email') is None:
            return {"message": "The field 'email' cannot be left blank."}, 400

        # garante que o email não seja duplicado
        if UserModel.find_by_email(dados['email']):
            return {"message": "The email '{}' already exists."
                    .format('login')}, 400

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists."
                    .format(dados['login'])}

        user = UserModel(**dados)
        user.ativado = False

        try:
            user.save_user()
            user.send_confirmation_email()
        except Exception:
            user.delete_user()
            traceback.print_exc()
            return {'message': 'An internal server error has ocurred.'}, 500
        return {'message': 'User created successfully!'}, 201  # created


class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        # função que compara de forma segura duas strings
        if user and safe_str_cmp(user.senha, dados['senha']):
            if user.ativado:
                token_de_acesso = create_access_token(identity=user.user_id)
        # se existe o user e se a senha for igual
        # cria-se um token de acesso, que identifica o usuario pelo id
                return {'access_token': token_de_acesso}, 200
            return {'message': 'User not confirmed.'}, 400
        # Unauthorized
        return {'message': 'The username or password is incorrect.'}, 401


class UserLogout(Resource):

    @jwt_required()
    def post(self):
        # A variavel recebe o id do token, jti pega o id (JWT Token Identifier)
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully!'}, 200


class UserConfirm(Resource):
    # /confirmacao/{user_id}
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_user(user_id)

        if not user:
            return {"message": "User id '{}' not found.".format(user_id)}, 404

        user.ativado = True
        user.save_user()
        # return {"message": "User id '{}'\
        #      confirmed successfully.".format(user_id)}, 200
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user_confirm.html',
                                             email=user.email,
                                             usuario=user.login), 200, headers)
