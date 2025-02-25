import socket

# Função para exibir o menu de opções
def exibir_menu():
    print("Escolha uma opção:")
    print("1- IPv4")
    print("2- IPv6")
    print("3- Sair")

# Conexão do cliente com o cliente
def iniciar_cliente():
    # Endereço do servidor (localhost)
    HOST = "127.0.0.1"
    # Porta do servidor
    PORT = 65432

    # Cria um socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Conecta ao servidor
        client_socket.connect((HOST, PORT))

        # Autenticação
        login = input(client_socket.recv(1024).decode())
        # Envio do login para o servidor
        client_socket.sendall(login.encode())

        senha = input(client_socket.recv(1024).decode())
        # Envio da senha para o servidor
        client_socket.sendall(senha.encode())

        # Resposta da autenticação recebida do servidor
        resposta = client_socket.recv(1024).decode()
        # Mostra a resposta do servidor
        print(resposta)
        
        # Encerra se falhar na autenticação
        if "Falha na autenticacao" in resposta:
            return

        while True:
            # Mostra o menu de opções
            exibir_menu()
            # Recebe a escolha do usuário
            opcao = input("Digite sua escolha: ")

            if opcao == "3":
                # Envia o comando de saída para o servidor
                client_socket.sendall(b"sair")
                print("Encerrando conexão")
                break

            if opcao in ["1"]:
                # Solicitação do endereço e máscara
                endereco = input("Informe o endereço com máscara (ex: 192.168.1.10/24): ")
                # Envio do endereço e da máscara para o servidor
                client_socket.sendall(endereco.encode())
                # Resposta recebida do servidor
                resposta = client_socket.recv(1024).decode()
                # Mostra a resposta ao usuário
                print(f"Resposta do servidor:\n{resposta}")
            elif opcao in ["2"]:
                # Solicitação do endereço e máscara
                endereco = input("Informe o endereço com máscara (ex: 2001:db8::/48): ")
                # Envio do endereço e da máscara para o servidor
                client_socket.sendall(endereco.encode())
                # Resposta recebida do servidor
                resposta = client_socket.recv(1024).decode()
                # Mostra a resposta ao usuário
                print(f"Resposta do servidor:\n{resposta}")   
            else:
                # Mostra mensagem de erro para opções inválidas
                print("Opção inválida. Tente novamente.")

# Inicia o cliente quando o código é executado
if __name__ == "__main__":
    iniciar_cliente()
