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