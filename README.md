# 🔐 ConectaSSH

**ConectaSSH** é um gerenciador de conexões SSH com interface gráfica, que permite a usuários armazenar, organizar e acessar múltiplos servidores de forma segura e prática. Ideal para equipes que precisam conectar-se frequentemente a servidores remotos, evitando a digitação constante de comandos e senhas.

## ✨ Funcionalidades

- Interface gráfica amigável (Tkinter)
- Login seguro com senha criptografada
- Armazenamento individual de servidores por usuário
- Dados criptografados com senha única por usuário
- Exportação e importação de servidores com proteção por senha
- Conexão automatizada com servidores via SSH
- Integração com `sshpass` e terminal GNOME
- Compatível com Linux (interface GNOME)

## 📦 Requisitos

- Linux com GNOME
- Python 3.8 ou superior
- Pacotes Python:
  - `tkinter`
  - `cryptography`
- Pacote do sistema:
  - `sshpass`
- Terminal GNOME disponível (`gnome-terminal`)

## Como baixar e usar o repositório?

### 1. Clone o repositório

```
git clone https://github.com/seu-usuario/conectassh.git
cd conectassh
```

⚠️ Se você está usando Linux com GNOME, pode simplesmente rodar o executável em `dist/` sem instalar dependências!

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```
# crie o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # ou: source ./venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Se você ainda não tem o sshpass instalado, instale com:

```
sudo apt install sshpass
```

### 4. Execute o programa

```
python3 main.py
```

## 🧩 Criando um Atalho Gráfico no Linux

### 1. Crie o atalho .desktop

```
nano ~/.local/share/applications/conectassh.desktop
```

### 2. Cole o conteúdo abaixo:

```
[Desktop Entry]
Version=1.0
Type=Application
Name=ConectaSSH
Comment=Gerenciador gráfico de conexões SSH seguras
Exec=/CAMINHO/ABSOLUTO/DO/EXECUTAVEL
Icon=/CAMINHO/DO/ICONE/conectassh.png
Terminal=false
Categories=Utility;Network;
StartupNotify=true
```

### 3. Ajuste o caminhos
 
* Substitua Exec= com o caminho real do executável (dist/main)
* Substitua Icon= com o caminho do ícone .png ou .svg

### 4. Torne o atalho executável

```
chmod +x ~/.local/share/applications/conectassh.desktop
```

### 5. Atualize os atalhos

```
update-desktop-database ~/.local/share/applications
```
Agora você poderá abrir o **ConectaSSH** diretamente pelo menu de aplicativos do seu sistema Linux.

## Gerar executável

### Estrutura do projeto

```
conectassh/
├── users/                  # Base de dados dos usuários
├── main.py                 # Arquivo principal do programa
├── requirements.txt        # Lista de dependências do projeto
└── README.md               # Este arquivo
```

## Passo a Passo para Criar um Executável no PyCharm

### **Instalar o PyInstaller no PyCharm**

Primeiro, precisamos garantir que o PyInstaller está instalado no ambiente virtual do seu projeto. Para isso:

1. Abra seu projeto no PyCharm.
2. Vá até File > Settings (ou PyCharm > Preferences no macOS).
3. No menu à esquerda, selecione Project: [nome do seu projeto] > Python Interpreter.
4. Clique no ícone de "+" para adicionar pacotes.
5. No campo de pesquisa, digite pyinstaller e clique em Install Package.


### **Criar o Executável com o PyInstaller**
Agora que o PyInstaller está instalado, podemos gerar o executável diretamente do PyCharm.

1. Abrir o Terminal no PyCharm:
    * Vá para View > Tool Windows > Terminal para abrir o terminal integrado no PyCharm.
2. Rodar o PyInstaller: No terminal do PyCharm, execute o seguinte comando para gerar o executável:

```
pyinstaller --onefile --windowed --distpath=./dist --workpath=./build --specpath=./conecta_ssh_v1.spec main.py
```
### Testar o executável
1. Vá até a pasta dist criada no seu diretório de trabalho.

2. Você encontrará o arquivo executável (no caso do Windows, será nome_do_seu_arquivo.exe; no Linux/Mac será apenas nome_do_seu_arquivo).

3. Teste o executável clicando nele para garantir que tudo está funcionando corretamente, sem a necessidade do Python ou bibliotecas externas instaladas.

## 📄 Licença

Este projeto está licenciado sob os termos da [Licença MIT](LICENSE).  
Saiba mais sobre essa licença em [opensource.org/licenses/MIT](https://opensource.org/licenses/MIT).
