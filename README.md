# Conecta SSH
Programa desenvolvido para facilitar o acesso aos servidores SSH gerenciados pela empresa.

## Pré requisitos
### Instalar o SSHPASS:

```
sudo apt install sshpass
```



## Gerar executável

Passo a Passo para Criar um Executável no PyCharm

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
