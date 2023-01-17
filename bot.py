import os
import json
import logging

from dotenv import load_dotenv
load_dotenv()

import telebot

from telebot.util import escape
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from telebot import custom_filters
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

import imgbb





### DIRETÓRIO  ###
diretorio_completo = os.path.realpath(__file__)
diretorio = os.path.dirname(diretorio_completo)

### TEXTOS ###
with open(diretorio + "/textos.json", "r", encoding="utf-8") as _:
	TEXTOS = json.load(_)

### BOT ###
BOT_TOKEN = os.environ.get("BOT_TOKEN")
assert BOT_TOKEN, "TOKEN do bot não foi definido."
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage, parse_mode="html")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)



### COMANDO START ###

# Responder
@bot.message_handler(commands=["start"])
def responder_start(mensagem):
	nome = escape(mensagem.from_user.first_name)
	texto = TEXTOS["inicio"].format(nome)
	bot.send_message(
		chat_id=mensagem.chat.id,
		text=texto
	)
	
	
	
	
### CANCELAR PROCESSO ###

# Comando
@bot.message_handler(state="*", text=["Cancelar"])
def cancelar_processo(mensagem):
	bot.delete_state(
		user_id=mensagem.from_user.id
	)
	bot.send_message(
		chat_id=mensagem.from_user.id,
		text="Processo cancelado!",
		reply_markup=ReplyKeyboardRemove()
	)
	
	

		
### RECEBENDO IMAGENS ###

# Etapas
class Etapas(StatesGroup):
	enviando = State()


# Respondendo mensagem
@bot.message_handler(content_types=["photo"])
def responder_imagem(mensagem):
	imagem = sorted(mensagem.photo, key=lambda _: _.file_size, reverse=True)[0]
	bot.set_state(
		user_id=mensagem.from_user.id,
		state=Etapas.enviando
	)
	if imagem.file_size > 20971520:
		bot.send_message(
			chat_id=mensagem.from_user.id,
			text="Essa imagem é muito grande."
		)
	else:
		with bot.retrieve_data(user_id=mensagem.from_user.id) as dados:
			dados["file_id"] = imagem.file_id
		menu = ReplyKeyboardMarkup(resize_keyboard=True)
		menu.add("Sim", "Cancelar")
		bot.send_message(
			chat_id=mensagem.from_user.id,
			text="Deseja enviar essa imagem?",
			reply_markup=menu
		)
	
	

# Enviando imagem
@bot.message_handler(state=Etapas.enviando)
def enviando(mensagem):
	texto = mensagem.text
	if texto == "Sim":
		bot.send_message(
			chat_id=mensagem.from_user.id,
			text="Enviando...",
			reply_markup=ReplyKeyboardRemove()
		)
		bot.send_chat_action(
			chat_id=mensagem.from_user.id,
			action="typing"
		)
		with bot.retrieve_data(user_id=mensagem.from_user.id) as dados:
			pass
		url_imagem = bot.get_file_url(dados["file_id"])
		enviado = imgbb.enviar(url_imagem)
		if enviado["retorno"]:
			conteudo = enviado["conteudo"]
			informacoes = TEXTOS["informacoes"].format(
				conteudo["data"]["url_viewer"],
				conteudo["data"]["url"],
				conteudo["data"]["delete_url"]
			)
			bot.send_message(
				chat_id=mensagem.from_user.id,
				text=informacoes,
				disable_web_page_preview=True
			)
			bot.delete_state(
				user_id=mensagem.from_user.id
			)
		else:
			bot.send_message(
				chat_id=mensagem.from_user.id,
				text=f"Erro: {enviado['mensagem']}"
			)
			cancelar_processo(mensagem)
	else:
		bot.send_message(
			chat_id=mensagem.from_user.id,
			text="Escolha uma das opções abaixo:"
		)


### INICIANDO BOT ###
if __name__ == "__main__":
	bot.add_custom_filter(custom_filters.StateFilter(bot))
	bot.add_custom_filter(custom_filters.TextMatchFilter())
	bot.infinity_polling()