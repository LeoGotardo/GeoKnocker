import socket
from datetime import datetime

# Define o alvo
target = input("Insira o endereço IP ou o nome do host que você deseja verificar: ")

# Tenta resolver o endereço IP do alvo
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Nome do host não pode ser resolvido.")
    exit()

# Define a faixa de portas a serem escaneadas
start_port = int(input("Insira a porta inicial: "))
end_port = int(input("Insira a porta final: "))

print(f"\nIniciando o escaneamento em {target_ip}...")

# Inicia a contagem de tempo
start_time = datetime.now()

# Função para escanear uma única porta
def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((target_ip, port))
    except (socket.timeout, ConnectionRefusedError):
        return False
    else:
        return True
    finally:
        s.close()

# Loop para escanear as portas na faixa definida
for port in range(start_port, end_port + 1):
    if scan_port(port):
        print(f"Porta {port} está aberta.")
    else:
        print(f"Porta {port} está fechada.")

# Calcula o tempo total de execução
end_time = datetime.now()
total_time = end_time - start_time
print(f"\nEscaneamento concluído em: {total_time}")

