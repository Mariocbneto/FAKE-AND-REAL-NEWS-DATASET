import pandas as pd
import pymysql
import os

base_path = os.path.dirname(__file__) 
data_path = os.path.join(base_path, "../data/noticiasJuntas.csv")
data_path = os.path.abspath(data_path)  

df = pd.read_csv(data_path)


conn = pymysql.connect(
    host='localhost',
    user='root',
    password='MarioNeto2005',
    database='fakenews'
)
cursor = conn.cursor()


cursor.execute("DELETE FROM noticias;")
conn.commit()


dados = df[['title', 'text', 'rotulo']].values.tolist()


sql = "INSERT INTO noticias (title, text, rotulo) VALUES (%s, %s, %s)"
cursor.executemany(sql, dados)

conn.commit()
conn.close()
print("Dados inseridos com sucesso!")