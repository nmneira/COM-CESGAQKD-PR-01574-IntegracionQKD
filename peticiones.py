# Se guardan en local los datos de las variables a utilizar.

import requests
import json
import urllib3

# Suprimir solo warnings de HTTPS no verificados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# > Conexión nodos UVigo < #

# Nodes
KMSM_IP = 'castor.det.uvigo.es:444'
KMSS_IP = 'castor.det.uvigo.es:442'

# Certificados
# Alice
C1_PUB_KEY=r'/mnt/c/Users/nmneira/OneDrive - gradiant.org/Backup/Desktop/qkd/gu-a-cerberis-xgr-qkd/certs/alice/ETSIA.pem'
C1_PRIV_KEY=r'/mnt/c/Users/nmneira/OneDrive - gradiant.org/Backup/Desktop/qkd/gu-a-cerberis-xgr-qkd/certs/alice/ETSIA-key.pem'
C1_ROOT_CA=r'/mnt/c/Users/nmneira/OneDrive - gradiant.org/Backup/Desktop/qkd/gu-a-cerberis-xgr-qkd/certs/ca/ChrisCA.pem'

## Bob
C2_PUB_KEY=r'/mnt/c/Users/nmneira/OneDrive - gradiant.org/Backup/Desktop/qkd/gu-a-cerberis-xgr-qkd/certs/bob/ETSIB.pem'
C2_PRIV_KEY=r'/mnt/c/Users/nmneira/OneDrive - gradiant.org/Backup/Desktop/qkd/gu-a-cerberis-xgr-qkd/certs/bob/ETSIB-key.pem'
C2_ROOT_CA=r'/mnt/c/Users/nmneira/OneDrive - gradiant.org/Backup/Desktop/qkd/gu-a-cerberis-xgr-qkd/certs/ca/ChrisCA.pem'
# SAEs
C1_ENC = 'CONSA'
C2_ENC = 'CONSB'

# Función para manejar las solicitudes
def make_request(url, cert, key, cacert, method='GET', headers=None, data=None):
    try:
        response = requests.request(
            method=method,
            url=url,
            cert=(cert, key),
            verify=cacert,
            headers=headers,
            data=data
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")
        return None
    

# Petición del status
print("\nEstado del KMS maestro (Alice):")
url = f"https://{KMSM_IP}/api/v1/keys/{C2_ENC}/status"

respuesta = make_request(url, C1_PUB_KEY, C1_PRIV_KEY, False)
if respuesta:
    print(json.dumps(respuesta, indent=4))


# Petición de una clave al nodo maestro (Alice)
print("\nLeer clave del nodo maestro (Alice):")
url = f"https://{KMSM_IP}/api/v1/keys/{C2_ENC}/enc_keys"
respuesta = make_request(url, C1_PUB_KEY, C1_PRIV_KEY, False)
if respuesta:
    key = respuesta['keys'][0]['key']
    key_id = respuesta['keys'][0]['key_ID']
    print(f"\tClave: {key}")
    print(f"\tID: {key_id}")
    

# Petición de una clave por su ID al nodo esclavo (Bob)
print("\nLeer una clave por su ID en el nodo esclavo (Bob):")
url = f"https://{KMSS_IP}/api/v1/keys/{C1_ENC}/dec_keys"

data = json.dumps({"key_IDs": [{"key_ID": key_id}]})
respuesta = make_request(
    url,
    C2_PUB_KEY,
    C2_PRIV_KEY,
    False,
    method='POST',
    headers={'Content-Type': 'application/json'},
    data=data
)
if respuesta:
    key = respuesta['keys'][0]['key']
    key_id = respuesta['keys'][0]['key_ID']
    print(f"\tClave: {key}")
    print(f"\tID: {key_id}")

    with open('claves_qkd.txt', 'a') as archivo:
        archivo.write(f"Clave: {key}\n")
        archivo.write(f"ID: {key_id}\n")
print("\n")