# import sqlite3

# conexao = sqlite3.connect('banco.db')
# cursor = conexao.cursor()

# cria_tabela = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY,\
#      nome text, estrelas real, diaria real, cidade text)"

# cria_hotel = "INSERT INTO hoteis VALUES ('hotel10', 'Hotel 10', 4.0, 345.30,\
#      'Chapecó')"

# cursor.execute(cria_tabela)
# cursor.execute(cria_hotel)

# conexao.commit()
# conexao.close()
