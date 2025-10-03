# --- VARIÁVEIS DE ESTADO GLOBAIS ---
logado = False
historico_disponivel = False

# --- FUNÇÕES ---

def logar():
    """Gerencia o processo de login do usuário."""
    global logado
    login = input("Insira a sua senha: ")
    try:
        with open("conta.txt", "r", encoding="utf-8") as arquivoCler:
            for linha in arquivoCler:
                if "Senha:" in linha:
                    senha_salva = linha.split(":")[1].strip()
                    if senha_salva == login:
                        print("Login efetuado com sucesso!")
                        logado = True
                        return True
                    else:
                        print("Senha incorreta.")
                        return False
            print("Senha não encontrada no arquivo. Verifique se o arquivo está correto.")
            return False
    except FileNotFoundError:
        print("Arquivo da conta não encontrado. Crie uma conta primeiro.")
        return False

def ver_loja():
    """Exibe a lista completa de produtos disponíveis para compra, numerada."""
    try:
        with open("loja.txt", "r", encoding="utf-8") as arquivo:
            print("\n--- Produtos Disponíveis na Loja ---")
            produtos = arquivo.readlines()
            for i, linha in enumerate(produtos, 1):
                partes = linha.strip().split(':')
                if len(partes) == 2:
                    nome, preco_str = partes
                    try:
                        preco = float(preco_str)
                        print(f"{i} - Produto: {nome.strip()} | Preço: R$ {preco:.2f}")
                    except ValueError:
                        print(f"Erro ao ler o preço de: {nome.strip()}")
            return produtos
    except FileNotFoundError:
        print("O arquivo da loja não foi criado.")
        return []

def adicionar_ao_carrinho():
    """Permite adicionar um produto da loja ao carrinho."""
    produtos_loja = ver_loja()
    if not produtos_loja:
        return
    
    try:
        escolha = int(input("\nDigite o número do produto que deseja adicionar ao carrinho: "))
        # Verifica se o número escolhido é válido
        if 1 <= escolha <= len(produtos_loja):
            produto_selecionado = produtos_loja[escolha - 1]
            # Adiciona o produto ao arquivo do carrinho
            with open("carrinho.txt", "a", encoding="utf-8") as arquivo_carrinho:
                arquivo_carrinho.write(produto_selecionado)
            print("Produto adicionado ao carrinho com sucesso!")
        else:
            print("Opção inválida.")
    except ValueError:
        print("Por favor, insira um número válido.")

def ver_carrinho():
    """Exibe o conteúdo do carrinho e o valor total."""
    total = 0.0
    quantidade = 0
    try:
        with open("carrinho.txt", "r", encoding="utf-8") as arquivo:
            print("\n--- Seu Carrinho ---")
            for linha in arquivo:
                partes = linha.strip().split(':')
                if len(partes) == 2:
                    nome, preco_str = partes
                    try:
                        preco = float(preco_str)
                        total += preco
                        quantidade += 1
                        print(f"Produto: {nome.strip()} | Preço: R$ {preco:.2f}")
                    except ValueError:
                        pass # Ignora linhas com preço inválido
            
            print(f"\nTotal de produtos no carrinho: {quantidade}")
            print(f"Valor total da compra: R$ {total:.2f}")
            return total
    except FileNotFoundError:
        print("O carrinho está vazio.")
        return 0.0

def consultarSaldo():
    """Lê e exibe o saldo do usuário."""
    try:
        with open("conta.txt", "r", encoding="utf-8") as arquivoCler:
            for linha in arquivoCler:
                if "Saldo:" in linha:
                    saldo = float(linha.split(":")[1].strip())
                    print(f"Seu saldo atual é: R$ {saldo:.2f}")
                    return saldo
    except (FileNotFoundError, ValueError):
        print("Erro ao ler o saldo. Verifique o arquivo da conta.")
        return None

def finalizar_compra():
    """Processa a compra, verifica o saldo e atualiza os arquivos."""
    global historico_disponivel
    
    total_compra = ver_carrinho()
    if total_compra == 0.0:
        print("Seu carrinho está vazio. Adicione produtos antes de finalizar a compra.")
        return

    saldo_atual = consultarSaldo()
    if saldo_atual is None:
        return

    if saldo_atual >= total_compra:
        novo_saldo = saldo_atual - total_compra
        
        # 4. Atualiza o arquivo da conta com o novo saldo
        conteudo_conta = []
        with open("conta.txt", "r", encoding="utf-8") as arquivo:
            conteudo_conta = arquivo.readlines()
        
        with open("conta.txt", "w", encoding="utf-8") as arquivo:
            for linha in conteudo_conta:
                if "Saldo:" in linha:
                    arquivo.write(f"Saldo: {novo_saldo:.2f}\n")
                else:
                    arquivo.write(linha)
        
        print(f"\nCompra efetuada com sucesso! Seu novo saldo é R$ {novo_saldo:.2f}")
        
        # 5. Registra a compra no histórico
        import datetime
        data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        # Lê o carrinho para o histórico e depois o esvazia
        with open("carrinho.txt", "r", encoding="utf-8") as arquivo_carrinho:
            produtos_comprados = arquivo_carrinho.read().strip().replace('\n', ', ')

        with open("historico.txt", "a", encoding="utf-8") as historico:
            historico.write(f"Data: {data_hora} - Compra de R$ {total_compra:.2f}. Produtos: {produtos_comprados}\n")
        
        # Esvazia o carrinho após a compra
        with open("carrinho.txt", "w", encoding="utf-8") as arquivo:
            arquivo.write("")
        
        historico_disponivel = True
    else:
        print("Saldo insuficiente para realizar a compra.")

def verHistorico():
    """Exibe o histórico de compras."""
    try:
        with open("historico.txt", "r", encoding="utf-8") as historico:
            print("\n--- Histórico de Compras ---")
            print(historico.read())
    except FileNotFoundError:
        print("Nenhum histórico de compras encontrado.")

def adicionarProd():
    """Permite adicionar novos produtos ao arquivo de lista da loja."""
    nome = input("Insira o nome do produto: ")
    preco = input("Insira o preço do produto: ")
    try:
        with open("loja.txt", "a", encoding="utf-8") as arquivoPescrita:
            arquivoPescrita.write(f"{nome}:{preco}\n")
        print("Produto adicionado à loja com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# --- MENU PRINCIPAL E LOOP ---
print("-------------------------------------------")
print("   Seja bem-vindo ao açougue do Allen ")
print("-------------------------------------------\n")

while True:
    print("\n-------------------------------------------")
    print("Opções")
    print("1 - Ver produtos da loja")
    
    # Opção de login só aparece se não estiver logado
    if not logado:
        print("2 - Logar no sistema")
    
    print("3 - Adicionar produtos na loja")
    
    # Opções que só aparecem se o usuário estiver logado
    if logado:
        print("4 - Adicionar produto ao carrinho")
        print("5 - Ver carrinho")
        print("6 - Consultar saldo")
        print("7 - Finalizar compra")
        if historico_disponivel:
             print("8 - Ver histórico de compras")
    
    print("0 - Sair do sistema")
    print("-------------------------------------------")

    try:
        opcao = int(input("Insira uma opção: "))
    except ValueError:
        print("Por favor, insira um número válido.")
        continue

    # A lógica 'match' para as novas opções
    match opcao:
        case 1:
            ver_loja()
        case 2:
            if not logado:
                logar()
            else:
                print("Você já está logado.")
        case 3:
            adicionarProd()
        case 4:
            if logado:
                adicionar_ao_carrinho()
            else:
                print("Opção inválida ou você não tem permissão para acessá-la.")
        case 5:
            if logado:
                ver_carrinho()
            else:
                print("Opção inválida ou você não tem permissão para acessá-la.")
        case 6:
            if logado:
                consultarSaldo()
            else:
                print("Opção inválida ou você não tem permissão para acessá-la.")
        case 7:
            if logado:
                finalizar_compra()
            else:
                print("Opção inválida ou você não tem permissão para acessá-la.")
        case 8:
            if logado and historico_disponivel:
                verHistorico()
            else:
                print("Opção inválida ou você não tem permissão para acessá-la.")
        case 0:
            print("Saindo do sistema. Até mais!")
            break
        case _:
            print("Opção inválida.")