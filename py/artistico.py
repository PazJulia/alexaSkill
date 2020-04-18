from flask import Flask
from flask_ask import Ask, statement, request, context, question, session, convert_errors, version
import json
import requests
import time
import unidecode
import random

app = Flask(__name__)
ask = Ask(app, "/")

cores_disponiveis = ['branco', 'preto', 'amarelo', 'azul', 'verde', 'laranja', 'vermelho', 'roxo', 'rosa', 'marrom']
# branco = 0
# preto = 1
# amarelo = 2
# azul = 3
# verde = 4
# laranja = 5
# vermelho = 6
# roxo = 7
# rosa = 8
# marrom = 9

frases_mistura_inexistente = ['Ops... acho que essa cor parece meio feia, melhor tentar outra combinação', 
								'Que pena, não consegui misturar estas cores']

def mix_result(cor_um, cor_dois):
	if cores_disponiveis[2] in [cor_um, cor_dois]: # amarelo
		if cores_disponiveis[3] in [cor_um, cor_dois]: # amarelo + azul = verde
			return 'verde'
		elif cores_disponiveis[0] in [cor_um, cor_dois]: # amarelo + branca = amarelo-claro
			return 'amarelo-claro'	
		elif cores_disponiveis[6] in [cor_um, cor_dois]: # amarelo + vermelho = laranja
			return 'laranja'
		elif cores_disponiveis[5] in [cor_um, cor_dois]: # amarelo + laranja = amarelo-alaranjado
			return 'amarelo-alaranjado'
		elif cores_disponiveis[4] in [cor_um, cor_dois]: # amarelo + verde = verde-claro
			return 'verde-claro'
		elif cores_disponiveis[8] in [cor_um, cor_dois]: # amarelo + rosa = alaranjado
			return 'alaranjado'
		elif cores_disponiveis[7] in [cor_um, cor_dois]: # amarelo + roxo = marrom
			return 'marrom'
		elif cores_disponiveis[9] in [cor_um, cor_dois]: # amarelo + marrom = amarelo-queimado
			return 'amarelo-queimado'
		elif cores_disponiveis[1] in [cor_um, cor_dois]: # amarelo + preto = tom de verde-oliva
			return 'tom de verde-oliva'
		return random.choice(frases_mistura_inexistente) 

	elif cores_disponiveis[3] in [cor_um, cor_dois]: # azul
		if cores_disponiveis[6] in [cor_um, cor_dois]: # azul + vermelho = roxo
			return 'roxo'
		elif cores_disponiveis[4] in [cor_um, cor_dois]: # azul + verde = turquesa
			return 'turquesa'
		elif cores_disponiveis[1] in [cor_um, cor_dois]: # azul + preto = azul-escuro
			return 'azul-escuro'
		elif cores_disponiveis[0] in [cor_um, cor_dois]: # azul + branco = azul-claro
			return 'azul-claro'
		return random.choice(frases_mistura_inexistente) 

	elif cores_disponiveis[6] in [cor_um, cor_dois]: # vermelho
		if cores_disponiveis[0] in [cor_um, cor_dois]: # vermelho + branco = rosa
			return 'rosa'
		elif cores_disponiveis[1] in [cor_um, cor_dois]: # vermelho + preto = vermelho-escuro
			return 'vermelho-escuro'
		elif cores_disponiveis[4] in [cor_um, cor_dois]: # vermelho + verde = marrom
			return 'marrom'
		elif cores_disponiveis[5] in [cor_um, cor_dois]: # vermelho + laranja = tom de laranja
			return 'tom de laranja'
		elif cores_disponiveis[7] in [cor_um, cor_dois]: # vermelho + roxo = tom de magenta
			return 'tom de magenta'
		return random.choice(frases_mistura_inexistente) 

	return random.choice(frases_mistura_inexistente)

def match_of_colors(cor):
	if cor == cores_disponiveis[0]: # branco
		return 'Branco combina com diversas cores, cai muito bem com o roxo ou com o preto!'
	elif cor == cores_disponiveis[1]: # preto
		return 'Preto combina com várias cores, como branco, vermelho, verde ou azul!'
	elif cor == cores_disponiveis[2]: # amarelo
		return 'Amarelo combina com laranja e vermelho, azul e verde, ou roxo'
	elif cor == cores_disponiveis[3]: # azul
		return 'Azul combina com branco, principalmente, e vermelho'
	elif cor == cores_disponiveis[4]: # verde
		return 'Tons de bege e azul combinam muito bem com o verde'
	elif cor == cores_disponiveis[5]: # laranja
		return 'Azul e branco fazem ótima combinação com o laranja'
	elif cor == cores_disponiveis[6]: # vermelho
		return 'Verde e amarelo combinam com tonalidades de vermelho'
	elif cor == cores_disponiveis[7]: # roxo
		return 'Vermelho e cinza combinam bem com tons de roxo'
	elif cor == cores_disponiveis[8]: # rosa
		return 'O branco é uma ótima combinação com o rosa, assim como o preto'
	elif cor == cores_disponiveis[9]: # marrom
		return 'O marrom combina com cores neutras e cores quentes, como oamarelo e o azul' 


@app.route("/")
def homepage():
    return "Olá, Mundo!"

@ask.launch
def start_skill():
    welcome_message = 'Olá terráqueo, em que posso ajudar?'
    return question(welcome_message).reprompt("Consigo acessar os contatos, abrir um chamado no iProtocolo e outras coisas mais.")


@ask.intent('MatchingColors', convert={'cor': str})
def say_age(cor):
    frases_duvida = ['Poderia repetir uma cor?',
                    'Poderia me dizer uma cor válida?']

    frases_solicitar_cor = [  'Diga-me uma cor.',
                                'Que cor quer consultar?',
                                'Para conhecer a combinação de cores, diga uma cor válida']
    
    # frases_resposta = [ "Você possui {} anos.",
    #                     "Você tem {} anos.",
    #                     "Você possui apenas {} primaveras"]

    if 'cor' in convert_errors:
        return question(random.choice(frases_duvida))
    
    if cor is None:
        return question(random.choice(frases_solicitar_cor))

    if cor in cores_disponiveis:
    	msg = match_of_colors(cor)
    	return statement(msg)

    return question('Ainda não conheço combinações com essa cor. Pode tertar outra menos difícil?')


@ask.intent('ColorMix', convert={'cor_um': str, 'cor_dois': str})
def color_mixing(cor_um, cor_dois):
    frases_duvida = ['Ops, pode informar duas cores novamente?',
                    'Pode me contar quais cores quer misturar?']

    frases_solicitar_cor = [  'Poderia informar duas cores?',
                                'Quais cores deseja misturar?',
                                'Diga-me duas cores']

    if 'cor_um' in convert_errors:
        return question(random.choice(frases_duvida))

    if 'cor_dois' in convert_errors:
        return question(random.choice(frases_duvida))
    
    if cor_um is None:
        return question(random.choice(frases_solicitar_cor))

    if cor_dois is None:
        return question(random.choice(frases_solicitar_cor))

    if (cor_um and cor_dois) in cores_disponiveis:
        if cor_um == cor_dois:
            return question('Diga-me duas cores diferentes')
  
        msg = mix_result(cor_um, cor_dois)
        return statement(msg)
  
    return question('Ops... não sei misturar estas cores. Utilize cores como: preto, branco, azul, amarelo ou vermelho')




@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Até mais")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Até mais")


@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == "__main__":
    app.run(debug=True)