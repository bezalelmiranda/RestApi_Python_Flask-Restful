from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from resources.filtros import consulta_sem_cidade, consulta_com_cidade
from resources.filtros import normalize_path_params
from flask_jwt_extended import jwt_required
import mysql.connector
from config_json import *


# path /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
    def get(self):
        open_connection = mysql.connector.connect(user=USER,
                                                  password=PASSWORD,
                                                  host=HOST,
                                                  database=DATABASE,
                                                  port=PORT)
        # connection = open_connection['connection']
        cursor = open_connection.cursor()

        # connection = sqlite3.connect('banco.db')
        # cursor = connection.cursor()

        # recebe os argumentos definidos em path_params
        dados = path_params.parse_args()
        # pega apenas os argumentos que não são none
        dados_validos = {chave: dados[chave]
                         for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)

        if not parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            # resultado = cursor.execute(consulta_sem_cidade, tupla)
            cursor.execute(consulta_sem_cidade, tupla)
            resultado = cursor.fetchall()
        else:
            tupla = tuple([parametros[chave] for chave in parametros])
            # resultado = cursor.execute(consulta_com_cidade, tupla)
            cursor.execute(consulta_com_cidade, tupla)
            resultado = cursor.fetchall()

        hoteis = []
        if resultado:
            for linha in resultado:
                hoteis.append({
                    'hotel_id': linha[0],
                    'nome': linha[1],
                    'estrelas': linha[2],
                    'diaria': linha[3],
                    'cidade': linha[4],
                    'site_id': linha[5],
                })

        return {'hoteis': hoteis}


class Hotel(Resource):
    atributos = reqparse.RequestParser()
    # Tratamento de erros
    atributos.add_argument('nome', type=str, required=True,
                           help="The field 'nome' cannot be left blank.")
    atributos.add_argument('estrelas')
    atributos.add_argument('diaria')
    atributos.add_argument('cidade', type=str, required=True,
                           help="The field 'cidade' cannot be left blank.")
    atributos.add_argument('site_id', type=int, required=True,
                           help="Every hotel needs to be linked with a site.")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404  # statusCode not found

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id "{}" already exists.'
                    .format(hotel_id)}, 400  # bad resquest

        # construtor
        dados = Hotel.atributos.parse_args()
        hotel = HotelModel(hotel_id, **dados)

        if not SiteModel.find_by_id(dados.get('site_id')):
            return {'message': 'The hotel must be\
                 associated to a valid site id.'}, 400

        try:
            hotel.save_hotel()
        except Exception:
            return {'message': 'An internal error\
                 ocurred trying to save hotel.'}, 500
        return hotel.json()

    @jwt_required()
    def put(self, hotel_id):

        dados = Hotel.atributos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()  # sava no banco
            return hotel_encontrado.json(), 200  # OK
        hotel = HotelModel(hotel_id, **dados)
        # Tratamento de erros
        try:
            hotel.save_hotel()
        except Exception:
            return {'message': 'An internal error\
                 ocurred trying to save hotel.'}, 500
            # Internal Server Error
        return hotel.json(), 201  # created = criado

    @jwt_required()
    def delete(self, hotel_id):
        # global hoteis
        # diz ao python que hoteis do for não
        # é o mesmo da variavel recem criada, mas é a lsita de hoteis
        # hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]

        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except Exception:
                return {'message': 'An error\
                    ocurred trying to delete hotel.'}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404
