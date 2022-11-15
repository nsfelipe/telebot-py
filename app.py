import os
import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


# Ativando os logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
PORT = int(os.environ.get('PORT', 8443))
TOKEN = os.environ['TOKEN']

# Defina alguns manipuladores de comandos. Estes geralmente levam a atualização de dois argumentos e
# contexto. Os manipuladores de erro também recebem o objeto TelegramError gerado com erro.


def start(update, context):
    # Responde quando o comando /hello é enviado
    text = '✅----✅ SERVIDOR ONLINE ✅----✅\n\n\nVEJA OS COMANDOS DISPONIVEL USANDO /info\n\n\nchatbot by: @nsfelipe™️'
    update.message.reply_text(text.upper())


def info(update, context):
    # Responde quando o comando /help é enviado
    text = '✅----✅ LISTA COMANDOS ✅----✅\n\n\n- Busca de dados de empresas:\n\n/cnpj 01123123000101\n\n\n- Busca de cep:\n\n/cep 30044000\n\n\nchatbot by: @nsfelipe™️'
    update.message.reply_text(text.upper())


def handle_response(text: str) -> str:
    # Retornando os dados do CNPJ informado

    texto = None

    def comando_errado():

        resposta = '⚠️------⚠️ ATENÇÃO ⚠️------⚠️\n\n\nO comando informado não está no padrão.\n\nDigite /info para ver as instruções!\n\n\nchatbot by: @nsfelipe™️'

        return resposta.upper()

    def requisicao_invalida(tipo):
        resposta = f'⚠️------⚠️ ATENÇÃO ⚠️------⚠️\n\n\nNão foi possivel realizar a sua consulta pois o {tipo} informado não é valido.\n\nDigite /info para ver as instruções!\n\n\nchatbot by: @nsfelipe™️'

        return resposta.upper()

    # Comando que vai acionar a busca por cnpj: /cnpj 19112659000168
    if '/cnpj' in text:

        # Filtra mensagem e busca pelo cnpj informado na API
        msg = text.split()
        cnpj = msg[1]

        # Filtra a quantidade de caracteres do cnpj
        if len(cnpj) == 14:

            url = f"https://publica.cnpj.ws/cnpj/{cnpj}"
            resp = requests.get(url)

            if resp.status_code == 200:
                dados = json.loads(resp.content)

                # Segmenta dicionário em listas menores para acessar os elementos
                estabelecimento = dados['estabelecimento']
                atividade_principal = estabelecimento['atividade_principal']
                estado = estabelecimento['estado']
                cidade = estabelecimento['cidade']

                # Dicionário com dados da empresa ja filtrados
                try:
                    empresa = {
                        'cnpj': estabelecimento['cnpj'],
                        'razao_social': dados['razao_social'],
                        'nome_fantasia': estabelecimento['nome_fantasia'],
                        'situacao_cadastral': estabelecimento['situacao_cadastral'],
                        'tipo_logradouro': estabelecimento['tipo_logradouro'],
                        'logradouro': estabelecimento['logradouro'],
                        'numero': estabelecimento['numero'],
                        'complemento': estabelecimento['complemento'],
                        'bairro': estabelecimento['bairro'],
                        'cep': estabelecimento['cep'],
                        'cidade': cidade['nome'],
                        'estado': estado['nome'],
                        'ddd1': estabelecimento['ddd1'],
                        'telefone1': estabelecimento['telefone1'],
                        'ddd2': estabelecimento['ddd2'],
                        'telefone2': estabelecimento['telefone2'],
                        'email': estabelecimento['email'],
                        'atividade_principal': atividade_principal['descricao'],
                        'atualizado_em': estabelecimento['atualizado_em']}

                    resposta = f"""✅----✅ RESULTADO: CNPJ ✅----✅\n\n\n- Razão Social: {empresa['razao_social']}\n\n- Nome Fantasia: {empresa['nome_fantasia']}\n\n- Status: {empresa['situacao_cadastral']}\n\n- CNPJ: {empresa['cnpj']}\n\n- E-mail: {empresa['email']}\n\n- Atividade principal: {empresa['atividade_principal']}\n\n- Telefone: {empresa['ddd1'] + empresa['telefone1']}\n\n\nDados atualizados em: {empresa['atualizado_em']}\n\nchatbot by: @nsfelipe 🚀™️"""
                    return resposta.upper()

                except:
                    resposta = '⚠️------⚠️ ATENÇÃO ⚠️------⚠️\n\n\nHouve um erro ao processar sua solcitação 🤔\n\nNão vou conseguir buscar informações desse CNPJ\n\n\nchatbot by: @nsfelipe™️'
                    return resposta.upper()

            else:
                return requisicao_invalida('cnpj')
        
        else:
            return comando_errado()

    # Busca informações do CEP
    if '/cep' in text:
        
        # Filtra mensagem e busca pelo cep informado na API
        msg = text.split()
        cep = msg[1]  # 34004481

        if len(cep) == 8:

            url = f'https://viacep.com.br/ws/{cep}/json/'
            resp = requests.get(url)

            if resp.status_code == 200:
                cep_response = json.loads(resp.content)
                
                if len(cep_response) == 1:
                    
                    return requisicao_invalida('cep')
                
                else:
                    resposta = f"""✅----✅ RESULTADO: CEP ✅----✅\n\n\n- CIDADE: {cep_response['localidade']}\n\n- BAIRRO: {cep_response['bairro']}\n\n- ESTADO: {cep_response['uf']}\n\n- LONGRADOURO: {cep_response['logradouro']}\n\n\nchatbot by: @nsfelipe 🚀™️"""
                    return resposta.upper()
            
            else:
                return requisicao_invalida('cep')
        
        else:
            return comando_errado()
    
    # Responde comando repositório
    if '/repositorio' in text:
        resposta = f'✅----✅ CÓDIGO FONTE ✅----✅\n\n\nLINK DO GITHUB: https://github.com/nsfelipe/telebot-py \n\n\nchatbot by: @nsfelipe 🚀'
        return resposta

    else:
        return comando_errado()


def handle_message(update, context):
    text = str(update.message.text).lower()
    response = handle_response(text)

    update.message.reply_text(response)


def echo(update, context):
    # Repete a mensagem enviada pelo usuario
    update.message.reply_text(update.message.text)


def error(update, context):
    # Erros de log causados ​​por atualizações.
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("info", info))
    #dp.add_handler(CommandHandler('cnpj', cnpj))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url='https://telebot-py.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
