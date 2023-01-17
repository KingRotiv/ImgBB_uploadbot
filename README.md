# ImgBB_uploadbot

### O que o bot faz?
Este é um bot no Telegram que faz upload de imagens para o site do [ImgBB](https://imgbb.com).

### Como o bot funciona?
O bot irá responder todas imagens que forem enviadas perguntando se deseja fazer o upload.

### Como configurar?
1. Clone o repositório para o local desejado.
2. Instale as dependências contidas no arquivo **requirements.txt**. Obs: o módulo python-dotenv é opcional, se não for definir as variáveis de ambiente por um arquivo .env não há necessidade deste módulo.
2. Defina as variáveis de ambiente **BOT_TOKEN** e **IMGBB_API_KEY**.
3. Execute o comando **python bot.py**

### Onde obter o BOT_TOKEN? 
Você pode obter o token do bot criando um novo bot no Telegram. Para mais informações inicie uma conversa com o bot [@BotFather](https://t.me/BotFather).

### Onde obter a IMGBB_API_KEY?
Para obter sua api key, primeiro você deve criar uma conta no site [ImgBB](https://imgbb.com) e em seguida gerar sua api key no menu.