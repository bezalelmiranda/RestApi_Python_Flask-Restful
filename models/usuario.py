from sql_alchemy import banco


class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))

    def __init__(self, login, senha):
        self.login = login
        self.senha = senha

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
        }

    @classmethod
    def find_user(cls, user_id):
        # Método de classe, que é enviado via path
        # leva um decorador @classmethod, a variavel hotel recebe:
        # cls=HotelModel(abreviação) acessa o método(query) da classe
        # que extende o banco.Model de SQLAlchemy que consulta o banco
        user = cls.query.filter_by(user_id=user_id).first()
        # SELECT * FROM hoteis WHERE hotel_id=hotel_id LIMIT 1
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()
    # adiciona o proprio obj ao banco de dados

    # def update_hotel(self, nome, estrelas, diaria, cidade):
    #     self.nome = nome
    #     self.estrelas = estrelas
    #     self.diaria = diaria
    #     self.cidade = cidade

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
