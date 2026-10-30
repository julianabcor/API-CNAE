import requests

def mostrar_menu():
    print("")
    print("========== API Atividades Econômicas ==========")
    print("1. Listar todas as Seções")
    print("2. Listar todas as Divisões")
    print("3. Sair")
    print("----------")
    return input("Digite o número da sua opção: ")

while True:
    opcao = mostrar_menu()

    if opcao == "1":
        url = "https://servicodados.ibge.gov.br/api/v2/cnae/secoes"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            for secao in resposta.json():
                print(f"[{secao['id']}] - {secao['descricao']}")
        else:
            print("Erro ao buscar seções.")

    elif opcao == "2":
        url = "https://servicodados.ibge.gov.br/api/v2/cnae/divisoes"
        resposta = requests.get(url)
        if resposta.status_code == 200:
            for divisao in resposta.json():
                print(f"Divisão {divisao['id']}: {divisao['descricao']}")
        else:
            print("Erro ao buscar divisões.")

    elif opcao == "3":
        print("Saindo do programa... Até logo!")
        break

    else:
        print("Opção inválida! Tente novamente.")