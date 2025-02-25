import socket
# Biblioteca para manipulação de endereços IP
import ipaddress 

# Dados de autenticação no servidor
USERNAME = "admin"
PASSWORD = "1234"

# Função para calcular a sub-rede
def calcular_subrede(endereco):
    try:
        # Cria uma rede a partir do endereço fornecido
        rede = ipaddress.ip_network(endereco, strict=False)
        # Ajuste para incluir o primeiro endereço útil do IPv6 e da quantidade de endereços úteis  
        if isinstance(rede, ipaddress.IPv6Network):
            enderecos_uteis = rede.num_addresses
            inicio = rede.network_address
            fim = rede.broadcast_address 
        else:
            # Retira o endereço da rede e o endereço de broadcast
            enderecos_uteis = rede.num_addresses - 2
            inicio = rede.network_address + 1
            fim = rede.broadcast_address - 1

        # Retorna a quantidade de endereços úteis e os endereços inicial e final
        return {
            "enderecos_uteis": enderecos_uteis,
            "inicio_util": str(inicio),
            "fim_util": str(fim),
        }
    # Retorna um erro caso o endereço seja inválido
    except ValueError:
        return {"erro": "Endereço ou máscara inválidos"}


# Função que trata cada cliente conectado ao servidor
def tratar_cliente(conn, addr):
    # Mostra o endereço do cliente conectado
    print(f"Cliente conectado: {addr}")

    # Autenticação
    conn.sendall(b"Login: ")
    # Recebe o login enviado pelo cliente
    username = conn.recv(1024).decode().strip()
    conn.sendall(b"Senha: ")
    # Recebe a senha enviada pelo cliente
    password = conn.recv(1024).decode().strip()

    # Verifica se os dados são válidos
    if username != USERNAME or password != PASSWORD:
        # Informa que a autenticação falhou
        conn.sendall(b"Falha na autenticacao. Encerrando conexao.\n")
        conn.close()
        return

    # Informa que a autenticação foi bem-sucedida
    conn.sendall(b"Autenticacao bem-sucedida\n")

    while True:
        # Recebe dados do cliente
        dados = conn.recv(1024).decode()
        # Verifica se a conexão deve ser encerrada
        if not dados or dados.lower() == "sair":
            conn.sendall(b"Conexao encerrada.\n")
            break

        # Calcula a sub-rede com base nos dados recebidos
        resultado = calcular_subrede(dados)
        # Verifica se ocorreu um erro
        if "erro" in resultado:
            resposta = resultado["erro"]
        # Monta a resposta com os resultados    
        else:
            resposta = (
                f"Quantidade de enderecos uteis disponiveis: {resultado['enderecos_uteis']}\n"
                f"Endereco util inicial: {resultado['inicio_util']}\n"
                f"Endereco util final: {resultado['fim_util']}\n"
            )
        # Envia a resposta ao cliente    
        conn.sendall(resposta.encode())
    # Encerra a conexão com o cliente quando for False
    conn.close()

# Função principal do servidor
def iniciar_servidor():
    # Endereço do servidor (localhost)
    HOST = "127.0.0.1"
    # Porta para escutar conexões
    PORT = 65432

    # Cria um socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Associa o socket ao endereço e porta
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print("Servidor escutando em", (HOST, PORT))

        while True:
            # Conexão de clientes
            conn, addr = server_socket.accept()
            # Trata o cliente conectado
            tratar_cliente(conn, addr)

# Inicia o servidor quando o código é executado
if __name__ == "__main__":
    iniciar_servidor()
