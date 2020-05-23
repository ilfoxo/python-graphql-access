import json
import sys
import urllib3
from conf import config
from python_graphql_client import GraphqlClient
import requests
import os

urllib3.disable_warnings()

headers = {
    # 'Content-Type': "application/graphql",
    'x-api-key': config.API_KEY,
    'cache-control': 'no-cache'
}

client = GraphqlClient(endpoint="http://localhost:20002/graphql", headers=headers)

def progress(count, total, status=''):

    """
    Como usarlo:

        for i in range(10):
        progress(i+1, 10, status="Descargando")
        time.sleep(1)
    """

    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
    if count == total:
        print()

def deleteAll():

    query = ''' 
        query listProducts {
            listProducts {
                items {
                    id
                }
            }
        }'''

    data = client.execute(query=query)

    while len(data["data"]["listProducts"]["items"]) > 0:
        if "error" in data:
            print("Error al obtener información")
            return

        data = data["data"]["listProducts"]["items"]
        query2 = '''
             mutation deleteProduct($input: DeleteProductInput!) {
                deleteProduct(input: $input) {
                    id
                }
            }
            '''

        for item in data:
            params = {
                "input": item
            }
            res = client.execute(query2, variables=params)
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

    query = """
        mutation createProduct($input: CreateProductInput!) {
            createProduct(input: $input) {
                id
  	            name
  	            description
  	            image
  	            category
            }
        }
      """

    for i, item in enumerate(data):
        progress(i, len(data), status="Working...")
        params = {
            "input": item
        }
        res = client.execute(query=query, variables=params)
        if "id" not in res["data"]["createProduct"]:
            print("Error al cargar: " + json.dumps(res))
        else:
            print(str(i) + " - " + res["data"]["createProduct"]["id"])

    print("Finished!")



if __name__ == '__main__':
    #loadData()
    #deleteAll()



