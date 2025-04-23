import os
import json
import base64
import subprocess
import secrets
import datetime
from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter import filedialog
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend

VERSAO_SISTEMA = "1.0.0"

# Diretório para armazenar os arquivos dos usuários
USER_DIR = 'users'
if not os.path.exists(USER_DIR):
    os.makedirs(USER_DIR)


def gerar_chave(senha: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(senha.encode()))


class SSHManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador SSH")
        self.username = ""
        self.user_file = ""
        self.fernet = None
        self.servidores = []
        self.salt = None

        self.tela_login()

    def tela_login(self):
        self.limpar_janela()

        Label(self.root, text="Login", font=("Helvetica", 16, "bold")).pack(pady=(10, 5))

        Label(self.root, text="Usuário:", anchor='w').pack(fill=X, padx=20)
        usuario_entry = Entry(self.root)
        usuario_entry.pack(fill=X, padx=20)

        Label(self.root, text="Senha:", anchor='w').pack(fill=X, padx=20, pady=(10, 0))
        senha_entry = Entry(self.root, show="*")
        senha_entry.pack(fill=X, padx=20)

        def entrar(event=None):  # <== aceita ser chamado por botão ou Enter
            usuario = usuario_entry.get().strip()
            senha = senha_entry.get().strip()

            if not usuario or not senha:
                messagebox.showwarning("Campos obrigatórios", "Usuário e senha são obrigatórios.")
                return

            self.username = usuario
            self.user_file = os.path.join(USER_DIR, f"{usuario}.json.encrypted")

            if os.path.exists(self.user_file):
                with open(self.user_file, 'rb') as f:
                    conteudo = f.read()
                    self.salt = conteudo[:16]
                    encrypted_data = conteudo[16:]
                try:
                    chave = gerar_chave(senha, self.salt)
                    self.fernet = Fernet(chave)
                    dados = self.fernet.decrypt(encrypted_data)
                    self.servidores = json.loads(dados.decode())
                    self.tela_principal()
                except InvalidToken:
                    messagebox.showerror("Erro", "Senha incorreta!")
            else:
                if messagebox.askyesno("Novo usuário", "Usuário não encontrado. Deseja criar um novo?"):
                    self.salt = secrets.token_bytes(16)
                    chave = gerar_chave(senha, self.salt)
                    self.fernet = Fernet(chave)
                    self.servidores = []
                    self.salvar_dados()
                    self.tela_principal()

        Button(self.root, text="Entrar", command=entrar).pack(pady=10)

        # Permite usar ENTER para login
        self.root.bind('<Return>', entrar)

    def tela_principal(self):
        self.limpar_janela()
        Label(self.root, text=f"Bem-vindo, {self.username}", font=("Helvetica", 14, "bold")).pack(pady=(10, 5))

        frame_servidores = Frame(self.root)
        frame_servidores.pack(pady=5, fill=X, padx=20)

        for srv in self.servidores:
            Button(frame_servidores, text=srv['nome'], command=lambda s=srv: self.conectar_ssh(s)).pack(fill=X, pady=2)

        Frame(self.root, height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=20, pady=10)

        Button(self.root, text="Adicionar Servidor", command=self.adicionar_servidor).pack(fill=X, padx=20, pady=2)
        Button(self.root, text="Exportar servidores", command=self.exportar_servidores).pack(fill=X, padx=20, pady=2)
        Button(self.root, text="Importar servidores", command=self.importar_servidores).pack(fill=X, padx=20, pady=2)

        # Botão "Sobre"
        Button(self.root, text="Sobre", command=self.mostrar_sobre).pack(fill=X, padx=20, pady=(10, 2))

        Button(self.root, text="Sair", command=self.tela_login).pack(fill=X, padx=20, pady=(10, 10))

    def adicionar_servidor(self):
        nome = simpledialog.askstring("Nome", "Nome do servidor:")
        host = simpledialog.askstring("Host", "Endereço do servidor:")
        porta = simpledialog.askstring("Porta", "Porta SSH:", initialvalue="22")
        usuario = simpledialog.askstring("Usuário", "Usuário SSH:")
        senha = simpledialog.askstring("Senha", "Senha SSH:", show="*")

        if not all([nome, host, porta, usuario, senha]):
            messagebox.showwarning("Campos obrigatórios", "Todos os campos devem ser preenchidos!")
            return

        try:
            porta_int = int(porta)
            if not (1 <= porta_int <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror("Porta inválida", "Informe uma porta numérica válida entre 1 e 65535.")
            return

        if any(s['nome'] == nome for s in self.servidores):
            messagebox.showerror("Duplicado", f"O servidor '{nome}' já está cadastrado.")
            return

        self.servidores.append({
            "nome": nome,
            "host": host,
            "porta": porta_int,
            "usuario": usuario,
            "senha": senha
        })
        self.salvar_dados()
        self.tela_principal()

    def salvar_dados(self):
        dados = json.dumps(self.servidores).encode()
        conteudo = self.salt + self.fernet.encrypt(dados)
        with open(self.user_file, 'wb') as f:
            f.write(conteudo)

    def conectar_ssh(self, servidor):
        # comando = f"gnome-terminal -- bash -c \"sshpass -p '{servidor['senha']}' ssh -p {servidor['porta']} {servidor['usuario']}@{servidor['host']}; exec bash\""
        comando = (
            f"gnome-terminal -- bash -c \""
            f"sshpass -p '{servidor['senha']}' ssh -o StrictHostKeyChecking=no "
            f"-o UserKnownHostsFile=~/.ssh/known_hosts "
            f"-p {servidor['porta']} {servidor['usuario']}@{servidor['host']}; exec bash\""
        )

        subprocess.Popen(comando, shell=True)

    def limpar_janela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def exportar_servidores(self):
        senha = simpledialog.askstring("Senha", "Digite uma senha para proteger o arquivo exportado:", show="*")
        if not senha:
            return

        caminho = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not caminho:
            return

        try:
            salt = secrets.token_bytes(16)
            chave = gerar_chave(senha, salt)
            fernet_export = Fernet(chave)

            export_data = {
                "usuario_exportador": self.username,
                "data_exportacao": datetime.datetime.now().isoformat(),
                "versao_sistema": VERSAO_SISTEMA,
                "dados": self.servidores
            }

            dados = json.dumps(export_data).encode()
            criptografado = fernet_export.encrypt(dados)

            with open(caminho, 'wb') as f:
                f.write(salt + criptografado)

            messagebox.showinfo("Exportação", "Servidores exportados com sucesso com senha!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar: {e}")

    def importar_servidores(self):
        caminho = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not caminho:
            return

        senha = simpledialog.askstring("Senha", "Digite a senha usada na exportação:", show="*")
        if not senha:
            return

        try:
            with open(caminho, 'rb') as f:
                conteudo = f.read()
                salt = conteudo[:16]
                dados_criptografados = conteudo[16:]

            chave = gerar_chave(senha, salt)
            fernet_import = Fernet(chave)

            dados = fernet_import.decrypt(dados_criptografados)
            dados_importados = json.loads(dados.decode())

            exportador = dados_importados.get("usuario_exportador", "desconhecido")
            data_exportacao = dados_importados.get("data_exportacao", "desconhecida")
            versao = dados_importados.get("versao_sistema", "1.0.0")
            servidores = dados_importados.get("dados", [])

            nomes_existentes = {s['nome'] for s in self.servidores}
            novos = [s for s in servidores if s['nome'] not in nomes_existentes]
            self.servidores.extend(novos)

            self.salvar_dados()
            self.tela_principal()

            messagebox.showinfo("Importação", (
                f"{len(novos)} servidor(es) importado(s) com sucesso!\n\n"
                f"Exportado por: {exportador}\n"
                f"Em: {data_exportacao}\n"
                f"Versão do sistema: {versao}"
            ))
        except InvalidToken:
            messagebox.showerror("Erro", "Senha incorreta ou arquivo corrompido.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar: {e}")

    def mostrar_sobre(self):
        # Criando a janela popup personalizada
        popup = Toplevel(self.root)
        popup.title("Sobre o ConectaSSH")

        # Definindo tamanho e centralizando a janela
        popup.geometry("400x300+{}+{}".format(
            self.root.winfo_screenwidth() // 2 - 200,  # Centralizando horizontalmente
            self.root.winfo_screenheight() // 2 - 150  # Centralizando verticalmente
        ))

        # Texto sobre o programa
        texto_sobre = """
        Nome do programa: ConectaSSH
        Versão: 1.0
        Autor: Cristian
        Copyright: © 2025 Todos os direitos reservados.
        """

        # Criando o label que exibe o texto
        label = Label(popup, text=texto_sobre, font=("Helvetica", 12), padx=10, pady=10, justify="left")
        label.pack(expand=True)

        # Adicionando um botão "Fechar"
        button_fechar = Button(popup, text="Fechar", command=popup.destroy)
        button_fechar.pack(pady=10)


if __name__ == '__main__':
    root = Tk()
    app = SSHManagerApp(root)
    root.mainloop()
