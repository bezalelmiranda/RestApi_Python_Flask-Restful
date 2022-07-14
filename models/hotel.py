from sql_alchemy import banco


class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String(80), primary_key=True)
    nome = banco.Column(banco.String(80))
    # precision = quantas casas depois da virgula
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    site_id = banco.Column(banco.Integer, banco.ForeignKey('sites.site_id'))
    # site = banco.relationship('SiteModel')

    # configurações de tabela pro banco de dados
    # definição dos argumentos como colunas
    # mapeamento da classe como uma tabela para o DB

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id': self.site_id,
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        # Método de classe, que é enviado via path
        # leva um decorador @classmethod, a variavel hotel recebe:
        # cls=HotelModel(abreviação) acessa o método(query) da classe
        # que extende o banco.Model de SQLAlchemy que consulta o banco
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        # SELECT * FROM hoteis WHERE hotel_id=hotel_id LIMIT 1
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()
    # adiciona o proprio obj ao banco de dados

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
