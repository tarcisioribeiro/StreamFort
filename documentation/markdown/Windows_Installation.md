# Instalação em ambientes Microsoft Windows

O **StreamFort** possui duas formas de execução e instalação em sistemas operacionais Windows, sendo uma nativa, onde são configurados manualmente o banco de dados e serviço de execução. A outra forma é a execução do WSL. Começaremos pela instalação padrão.

## Instalação Padrão

   ### *Requisitos necessários*

   - Git - **[Download](https://git-scm.com/downloads)**
   - Python 3.11.3 - **[Download](https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe)**
   - MySQL Server 5.7 - **[Download](https://dev.mysql.com/downloads/file/?id=523570)**

   ### Configuração do Git

   Após baixar o instalador do Git, execute-o e faça a instalação padrão.

   ### Configuração do Python

   Após baixar o instalador do Python, execute o instaldor e marque as duas caixas de seleção, prosseguindo com a instalação.

   ### Configuração do MySQL

   Após realizar o download do instalador do MySQL, execute-o e faça a instalação padrão, definindo uma senha para o banco de dados. Recorde e armazene esta senha, pois ela será utilizada posteriormente.

   * Após finalizar a instalação, copie este diretório:

         C:\Program Files\MySQL\MySQL Server 5.7

   * Edite as variáveis de ambiente, pressionando a tecla ***Windows*** do teclado, e pesquise por:
      
         Editar as variáveis de ambiente do sistema
   
   * Ao abrir as variáveis de ambiente, clique sobre a opção **PATH**, e então clique em **Novo**;
   * Cole o caminho copiado anteriormente e clique em **Ok**;

   * Abra o explorador de arquivos, e na barra de endereço, copie e cole o caminho abaixo, após isso, pressione **ENTER**:

         C:\ProgramData\MySQL\MySQL Server 5.7

   * Abra em um bloco de notas ou editor de texto o arquivo my.ini, e procure pela linha que contém o seguinte conteúdo:

         #enable-named-pipe

      Descomente a linha removendo a hashtag, e salve a alteração.

   * Reinicie o serviço do MySQL, digitando ***Serviços*** na barra de pesquisa, e procurando pelo nome *MySQL57*;

   * Abra o prompt de comando (**CMD**), e digite o seguinte comando:

         git clone https://github.com/tarcisioribeiro/StreamFort.git

      Pressione **ENTER** e aguarde.

   * Após realizar o download do StreamFort, execute estes comandos em sequência:

         cd StreamFort
         py -m venv venv
         .\venv\Scripts\Activate.ps1
         pip install -r requirements.txt

   * Por fim, para executar a aplicação, digite o seguinte comando:

         streamlit run main.py

## Configuração da aplicação através do WSL

   Para instalar a aplicação no WSL pelo Ubuntu 22.04, execute a aplicação do Ubuntu 22.04 que foi instalada anteriormente, e siga o passo a passo abaixo:

   1. Ao executar o Ubuntu 22.04, será necessário definir um nome de usuário, o qual deve ser **serveruser**, para que a aplicação possa ser instalada.
      
      **OBS.:** Defina uma senha que possa lembrar, e a armazene, pois ela será utilizada algumas vezes durante a instalação.

   2. Após definir uma senha, execute os seguintes comandos na aplicação do Ubuntu 22.04:

   ```bash
   cd ~
   sudo apt update
   sudo apt upgrade -y
   mkdir -p ~/repos
   sudo apt install build-essential git curl wget neofetch net-tools unzip -y
   cd ~/repos
   wget https://github.com/tarcisioribeiro/StreamFort/archive/refs/heads/main.zip
   unzip main.zip
   mv StreamFort-main StreamFort
   cd StreamFort/
   sudo ./services/linux/install_service.sh
   ```

   3. Após executar os comandos acima, será disponibilizado através do terminal o link de acesso, o qual deve ser copiado e colado em seu navegador de preferência.

   Antes de tudo, certifique-se de ter o **[Git](https://git-scm.com/downloads)** instalado em sua máquina, para que seja possível clonar o código do projeto.

   Nas versões mais recentes do Windows 10/11, foi implementada a ferramenta **[WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/)**, que permite o download e instalação de diversos softwares que estão agrupados e disponibilizados na plataforma **[winget.run](https://winget.run/)**. Basta procurar pelo software desejado, neste caso, o Git, e copiar o seu comando de download/instalação e executá-lo em uma janela do PowerShell.

   Para utilizar o StreamFort em ambiente **Windows**, execute o **Windows PowerShell** como **administrador**, executando em sequência os comandos abaixo:

   ```powershell
   Set-ExecutionPolicy Unrestricted
   winget install -e --id Git.Git
   cd ~
   ```

   Feche o PowerShell, e o execute novamente, desta vez sem a necessidade dos privilégios de administrador, e execute estes comandos:

   ```powershell
   git clone https://github.com/tarcisioribeiro/StreamFort.git
   whoami
   ```
   Anote o nome de usuário que aparecerá ao executar o comando **whoami**, que deve retornar algo como "*desktop-q6nbvq\dev*". Anote os caracteres que são mostrados após a "\\".

   Execute novamente o PowerShell como administrador, e execute estes comandos:

   ```powershell
   cd C:\Users\'usuario_anotado'
   .\StreamFort\services\windows\InstallWSL.ps1
   ```

   Após executar os comandos acima, reinicie a máquina, executando o Windows PowerShell com permissões de administrador novamente, e execute o seguinte comando:

   ```powershell
   cd C:\Users\'usuario_anotado'
   .\StreamFort\services\windows\InstallWSL_Ubuntu22_04.ps1
   ```

   A execução do script **InstallWSL.ps1** automaticamente realizará a instalação do **[WSL](https://learn.microsoft.com/en-us/windows/wsl/)**, que é o Subsistema Linux para Windows. O script **InstallWSL_Ubuntu22_04.ps1** realizará a instalação do **[Ubuntu 22.04](https://ubuntu.com/)** sobre o WSL.