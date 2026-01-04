import requests
from tabulate import tabulate
import mysql.connector

URL = "https://restcountries.com/v3.1/region/America"

response = requests.get(URL)

if response.status_code == 200:
    print("Conección a API exitosa")
    data = response.json()
    rows = []
    for dic_user in data:
        name = dic_user['name']['official']
        capital = dic_user['capital']
        region = dic_user['region']
        population = dic_user['population']
        rows.append([name,capital,region,population])
        
    headers = ['Name','Capital','Region','Population']
    print(tabulate(rows,headers,tablefmt='grid'))

    #Cargamos data en la BD
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="db_g6"
    )
    if connection.is_connected():
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS paises(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            capital VARCHAR(255) NOT NULL,
            region VARCHAR(255),
            population VARCHAR(100)
            );
            """
        )
    
        #Insertamos los usuarios a la 
        for paises in rows:
            cursor.execute(
                """
                insert into paises(name,capital,region,population)
                values(%s,%s,%s,%s)
                """,
                paises
            )
        connection.commit()
        connection.close()
        print(f' Registros importados a la base de datos')
    else:
            print('Error al conectarse a la base de datos')
    
else:
    print(f"Error:{response.status_code}")