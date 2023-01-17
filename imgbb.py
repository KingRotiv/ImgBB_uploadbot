import os
import requests



# Enviar imagem
def enviar(url_imagem):
	api_key = os.environ.get("IMGBB_API_KEY")
	assert api_key, "API_KEY não definida."
	url = "https://api.imgbb.com/1/upload"
	
	args = {
		"key": api_key,
		"image": url_imagem
	}
	resposta = requests.post(url=url, params=args)
	if resposta.status_code == 200:
		_json = resposta.json()
		if _json["success"] == True:
			return {
				"retorno": True,
				"conteudo": _json
			}
		else:
			return {
				"retorno": False,
				"mensagem": "Imagem não enviada."
			}
	else:
		return {
			"retorno": False,
			"mensagem": "Não foi possível acessar o servidor! Tente novamente mais tarde."
		}