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

def mix_result(cor_um, cor_dois):
	if cores_disponiveis[2] in [cor_um, cor_dois]:
		return 'amarelo'

	return 'não entrou no amarelo'

@app.route("/")
def homepage():
    return "Olá, Mundo!"

@ask.launch
def start_skill():
    welcome_message = "Olá terráqueo, em que posso ajudar?"
    return question(welcome_message).reprompt("Consigo acessar os contatos, abrir um chamado no iProtocolo e outras coisas mais.")


@ask.intent('MatchingColors', convert={'cor': str})
def say_age(age):
    frases_duvida = ["Poderia repetir uma cor?",
                    "Pode me dizer uma cor válida?"]

    frases_solicitar_idade = [  "Diga-me uma cor.",
                                "Que cor quer consultar?",
                                "Para conhecer a combinação de cores, diga uma cor válida"]
    
    # frases_resposta = [ "Você possui {} anos.",
    #                     "Você tem {} anos.",
    #                     "Você possui apenas {} primaveras"]

    if 'age' in convert_errors:
        return question(random.choice(frases_duvida))
    
    if age is None:
        return question(random.choice(frases_solicitar_idade))

    return statement(random.choice(frases_resposta).format(age))


@ask.intent('ColorMix', convert={'cor_um': str, 'cor_dois': str})
def color_mixing(cor_um, cor_dois):
    frases_duvida = ["Ops, pode informar duas cores novamente?",
                    "Pode me contar quais cores quer misturar?"]

    frases_solicitar_cor = [  "Poderia informar duas cores?",
                                "Quais cores deseja misturar?",
                                "Diga-me duas cores"]
    
    # frases_resposta = [ "Você possui {} anos.",
    #                     "Você tem {} anos.",
    #                     "Você possui apenas {} primaveras"]

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
            return question("Diga-me duas cores diferentes")
  
        msg = mix_result(cor_um, cor_dois)
        return statement(msg)
  
    return question("Ops... não sei misturar estas cores. Utilize cores como: preto, branco, azul, amarelo ou vermelho")




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