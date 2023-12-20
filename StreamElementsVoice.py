import requests
import json
from colorama import init, Fore
from time import sleep

def inform_token():
    x = input(Fore.BLUE + "Informe seu token da Stream Elements: ")
    return x

def get_id(pessoa):
    r = requests.get(f'https://api.streamelements.com/kappa/v2/channels/{pessoa}')
    return json.loads(r.text)['_id']

def get_itens(id):
    i = 0
    r = requests.get(f'https://api.streamelements.com/kappa/v2/store/{id}/items?source=website')
    itens = json.loads(r.text)
    for item in itens:
        if item['enabled'] == True:
            print(Fore.YELLOW + f"Item: {i}\n" + Fore.GREEN + f"Name: {item['name']}\nPrice: {item['cost']}\nCD: {item['cooldown']['global']}\n")
            i+=1
        else:
            print(Fore.RED + f"Item: {i}\nName: {item['name']}\nPrice: {item['cost']}\nCD: {item['cooldown']['global']}\n")
            i+=1
    
    select = int(input(Fore.YELLOW +"Selecione o item que deseja: "))
    return itens[select]['_id'], itens[select]['cooldown']['global']
    
def purchase_itens(item_id, id, bearer, cd):
    message = input(Fore.BLUE + 'Digite a mensagem que deseja spammar: ')
    amount = int(input(Fore.BLUE + 'Quantas vezes deseja mandar a mensagem: '))
    json = {"input":[],"message":f"{message}"}
    headers = {
        "Authorization": f"Bearer {bearer}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    for x in range(amount):
        request = requests.post(f'https://api.streamelements.com/kappa/v2/store/{id}/redemptions/{item_id}', headers=headers, json=json)
        if(request.status_code == 200):
            print(Fore.GREEN +"Mensagem enviada com sucesso")
        else:
            print(Fore.RED +"Erro ao enviar a mensagem")
        sleep(int(cd))

if __name__ == '__main__':
    bearer = inform_token()
    loja = str(input("Digite a loja que deseja spammar: "))
    id = get_id(loja)
    item_id, cd = get_itens(id)
    purchase_itens(item_id, id, bearer, cd)
