from qlaccess.qlaccess import *
from gql import gql
import json
import sys
import urllib3

urllib3.disable_warnings()

def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

def deleteAll():

    query = gql(''' query {
        listProducts {
            items {
            id
            }
        }
    }''')
    data = client.execute(query)

    while len(data["listProducts"]["items"]) > 0:
        if "error" in data:
            print("Error al obtener información")
            return

        data = data["listProducts"]["items"]
        query2 = gql('''
               mutation deleteProduct($input: DeleteProductInput!) {
                deleteProduct(input: $input) {
                    id
                }
            }
            ''')
        for item in data:
            params = {
                "input": item
            }
            res = client.execute(query2, variable_values=params)
        data = client.execute(query)
    print("Delete Finished!")

def loadData():
    with open("data50.json", "r") as inputfile:
        data = json.load(inputfile)

    data = [{"name": "Producto {0}".format(i),
             "description": "Descripción del producto {0}".format(i),
             "image": item["image"],
             "category": item["image"].split("/")[4]
             }
            for i, item in enumerate(data)]

    query = gql('''
           mutation createProduct($input: CreateProductInput!) {
            createProduct(input: $input) {
                id
      	        name
      	        description
      	        image
      	        category
            }
        }
        ''')

    for i, item in enumerate(data):
        progress(i, len(data), status="Working...")
        params = {
            "input": item
        }
        res = client.execute(query, variable_values=params)
        if "id" not in res["createProduct"]:
            print("Error al cargar: " + json.dumps(res))
        else:
            print(str(i) + " - " + res["createProduct"]["id"])

    print("Finished!")



if __name__ == '__main__':
    loadData()
