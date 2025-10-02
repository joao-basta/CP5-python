logado = False
historico_disponivel = False

def listaProd(): 
    total = 0.0
    quantidade = 0 
    try:
        with open("listaProdutos.txt", "r", encoding="utf-8") as arquivoPler: 
            for linha in arquivoPler:
                partes = linha.strip().split(':')
                if len(partes) == 2:
                    nome, preco = partes
                    try:
                        preco = float(preco)
                        total += preco
                        quantidade += 1
                        print(f" produto: {nome} | Preco: R$ {preco:.2f}")
                    except ValueError:
                        print(f"Erro ao ler o preço do produto: {nome.strip()}")


                print(f"\nTotal de produtos: {quantidade}")
                print(f"Valor total da compra: R$ {total:.2f}")
    except FileNotFoundError:
        print("A lista de produtos ainda não foi criada.")
        return False
    
def logar():
    global logado
    login = input("Insira a sua senha: ")
    try:
        with open("conta.txt", "r", encoding="utf-8") as arquivoCler:
            for linha in arquivoCler:
                if "Senha: " in linha:
                    senha = linha[7:]
                    if senha.strip() == login:
                        print("deu certo o login")
                        logado = True
                    else:
                        print("Não deu certo")
                        return False
    except FileNotFoundError:
        print("Arquivo não encontrado. crie uma conta primeiro.")
        return False




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