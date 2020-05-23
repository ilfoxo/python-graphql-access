import requests
import os
import json

"""
    Obtiene url de las fotos del sitio de perros
"""

def downloadFile(url: str):
    filename = url.split('/')[len(url.split('/')) - 1]

    resp = requests.get(url)
    if resp.status_code == 200:
        with open(os.path.join('downloaded_files', filename), 'wb') as r:
            r.write(resp.content)
    else:
        print("Error al descargar archivo: " + url)



categorias = ["borzoi", "boxer", "chow", "dingo"]
contenedor = list()

for categoria in categorias:
    url = "https://dog.ceo/api/breed/{0}/images/random".format(categoria)
    i = 0
    while i < 50:
        data = requests.get(url)
        if data.status_code == 200:
            if data.json()['message'] not in contenedor:
                contenedor.append(data.json()['message'])
                i = i+1
            else:
                continue
        print(str(i) + " - " + data.json()['message'])
        downloadFile(data.json()['message'])
        # time.sleep(0)
res = [{"image": contenedor[i]} for i in range(0, len(contenedor))]

with open('data50.json', 'w') as outfile:
    json.dump(res, outfile)



