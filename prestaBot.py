import slack

import prestashopAPI
from passwords import url, key, slack_token

client = slack.WebClient(slack_token)


def ejecutar(changes):
    client.chat_postMessage(
        channel="#avisos_prestashop",
        text=changes
    )


t = prestashopAPI.PrestashopAPI(url, key, ejecutar, ejecutar)

t.start()


@slack.RTMClient.run_on(event='message')
def send_products(**payload):
    products = t.get_products()
    cont2 = 1
    productos = "Esta es la lista de productos:\n"
    for product in products:
        productos += str(cont2) + ".- " + product['nombre'] + "\n"
        cont2 += 1
    data = payload['data']
    web_client = payload['web_client']
    if '<@UJM3JQH6C> productos' in data['text']:
        channel_id = data['channel']

        web_client.chat_postMessage(
            channel=channel_id,
            text=productos
        )


@slack.RTMClient.run_on(event='message')
def send_customers(**payload):
    clientes = "Esta es la lista de clientes:\n"
    cont = 1
    customers = t.get_customers()
    for customer in customers:
        clientes += str(cont) + ".- " + customer['apellidos'] + ", " + customer['nombre'] + "\n\t" + customer['email'] + \
                    ", " + customer['fecha_nacimiento'] + "\n"
        cont += 1
    data = payload['data']
    web_client = payload['web_client']
    if '<@UJM3JQH6C> clientes' in data['text']:
        channel_id = data['channel']

        web_client.chat_postMessage(
            channel=channel_id,
            text=clientes
        )


rtm_client = slack.RTMClient(token=slack_token)
rtm_client.start()