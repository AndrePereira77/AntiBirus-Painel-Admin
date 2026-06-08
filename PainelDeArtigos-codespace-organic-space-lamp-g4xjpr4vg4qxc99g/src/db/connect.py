import sys
import mysql.connector
from mysql.connector import Error

conn = None

try:
    conn = mysql.connector.connect(
        host='localhost',
        database='loja_informatica',
        user='root',
        password=''
    )
    print("Ligado ao inventário da Loja de Informática.")
except Error as erro:
    print(f"Erro ao ligar ao MySQL: {erro}")
    sys.exit()