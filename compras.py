def listaProd():   
    with open("listaProdutos.txt", "r", encoding="utf-8") as arquivoPler: 
        for linha in arquivoPler:
            print(linha, end="")

def logar():
    login = input("Insira a sua senha: ")
    with open("conta.txt", "r", encoding="utf-8") as arquivoCler:
        for linha in arquivoCler:
            if "Senha: " in linha:
                senha = linha[7:]

        if senha.strip() == login:
            print("deu certo o login")
        else:
            print("Não deu certo")





print("-------------------------------------------")
print("   Seja bem-vindo ao açougue do Allen ")
print("-------------------------------------------\n")

print("-------------------------------------------")
print("Opções \n" \
    "1 - Ver lista de produtos \n" \
    "2 - Logar no sistema \n" \
    "3 - Editar / Cadastrar produtos \n" \
    "0 - Sair do sistema ")
print("-------------------------------------------")

opcao = int(input("Insira uma opção: "))

match opcao:
    case 1:
        listaProd()
    case 2:
        logar()
    
        









