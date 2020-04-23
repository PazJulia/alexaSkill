from flask import Flask
from flask_ask import Ask, statement, request, context, question, session, convert_errors, version
import json
import requests
import time
import unidecode
import random

app = Flask(__name__)
ask = Ask(app, "/")

tipos_pintura_disponiveis = ['pintura', 'lapis', 'desenho', 'acrilica', 'guache', 'oleo', 'aquarela']
# pintura = 0
# lapis = 1
# desenho = 2
# acrilica = 3
# guache = 4
# oleo = 5
# aquarela = 6

cores_disponiveis = ['branco', 'preto', 'amarelo', 'azul', 'verde', 'laranja', 'vermelho', 'roxo', 'rosa', 'marrom']

frases_mistura_inexistente = ['Ops... não sei que cor é essa, melhor tentar outra combinação', 
								'Que pena, não consegui misturar estas cores. Tente novamente']
def paint_hints(paint):
	if paint == tipos_pintura_disponiveis[0]: # pintura
		return ['Atualmente, os principais tipos de pintura são feitas com tintas acrílica, guache, tintas a óleo e aquarela.']
	elif paint == tipos_pintura_disponiveis[1]: # lapis 
		return ['Lápis H são lápis duros que possuem uma linha fina e sua cor é cinza.',
				'Lápis do tipo B são macios e sua linha é grossa, sua cor é cinza escuro, quanto maior a numeração, mais escura a sua cor',
				'Para trabalhar sombras, pode ser utilizados diferentes materiais, são eles o algodão, limpa tipos e esfuminho.']
	elif paint == tipos_pintura_disponiveis[2]: # desenho 
		return ['O desenho pode ser artístico ou técnico. O primeiro serve para replicar a natureza ou expressar emoções, o segundo replica coisas reais e serve para comunicar informações práticas',
				'O desenho geralmente é feito com materiais de grafite, como lápis e lapiseira. Outra técnica é o desenho com carvão.']
	elif paint == tipos_pintura_disponiveis[3]: # acrilica 
		return ['A tinta acrílica é uma tinta sintética, solúvel em água e quando seca é impermeável e resistente a umidade.',
				'Pode ser aplicada em papel, telas ou em paredes.']
	elif paint == tipos_pintura_disponiveis[4]: # guache 
		return ['A tinta guache é similar a aquarela, porém é uma tinta opaca e fosca, além de ser mais espessa.',
				'A tinta pode ser diluída em água, ou aplicada diretamente no papel. Quanto menos água estiver presente, mais opaca será a tinta.',
				'A tinta pode ser utilizada depois de seca misturando-se com água, porém ela perde a espessidade inicial',
				'Para pintar com guache, pinte em camadas, comece pintando o fundo.']
	elif paint == tipos_pintura_disponiveis[5]: # oleo 
		return ['Para pintar com tinta a óleo, é necessário ter os materiais básicos como as cores essenciais: vermelho, azul, siena queimado e branco. Também é preciso ter em mãos solventes e óleos, o mais utilizado é o óleo de linhaça. Além disso, é necessário possuir pincéis e uma tela.',
				'Antes de pintar na tela, faça uma miniatura num caderno, tentando utilizar as cores desejadas, após isso, faça o esboço na tela.',
				'Para começar a pintar, inicie pintando o fundo e os tons mais escuros.',
				'Não coloque na paleta tinta em excesso, somente o necessário, pois quando exposta ao oxigênio, a tinta endurece e não pode mais ser utilizada.',
				'Pode ser que sua pintura leve alguns dias para ser finalizada pois as tintas demoram a secar. Por isso, deixe a pintura longe de poeira e luz solar para que não seja arruinada.']
	elif paint == tipos_pintura_disponiveis[6]: # aquarela 
		return ['Para utilizar aquarela corretamente, é preciso escolher os materiais de forma correta. Para o papel, prefira aqueles que são compostos por algodão pois absorvem melhor a tinta. Para os pincéis, é necessário escolher aqueles com cerdas macias, podem ser sintéticos ou naturais.',
		        'Ao pintar com aquarela, é sempre bom ter água limpa ao alcance. Para isso, utilize dois recipientes com água, o primeiro serve para retirar o excesso de tinta do pincel, o outro recipiente sempre terá água limpa para utilizar na pintura.',
		        'Como aquarela é uma tinta pouco opaca, ou seja, não se consegue sobrepor cores escuras com cores claras, comece pintando as partes mais claras da sua pintura, sem que sejam sobrepostas por cores escuras.',
		        'Para clarear uma cor, adicione água a mistura',
		        'Pode ser necessário deixar o papel secar antes de continuar a pintura, portanto, espere para que seque naturalmente, ou utilize um secador sem calor e em potência baixa.'
		        'Na técnica molhado no molhado, primeiramente, a superfície do papel é molhada e após isso, é aplicada a tinta que se espalha pela superfície molhada. É geralmente utilizada para a pintura de paisagens como o céu, ou para dar um efeito de fundo desfocado.']
	

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
		return 'break'

	elif cores_disponiveis[3] in [cor_um, cor_dois]: # azul
		if cores_disponiveis[6] in [cor_um, cor_dois]: # azul + vermelho = roxo
			return 'roxo'
		elif cores_disponiveis[4] in [cor_um, cor_dois]: # azul + verde = turquesa
			return 'turquesa'
		elif cores_disponiveis[1] in [cor_um, cor_dois]: # azul + preto = azul-escuro
			return 'azul-escuro'
		elif cores_disponiveis[0] in [cor_um, cor_dois]: # azul + branco = azul-claro
			return 'azul-claro'
		return 'break' 

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
		return 'break'

	return 'break'

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

@ask.intent('Hint', convert={'paint': str})
def say_age(paint):
    frases_duvida = ['Poderia repetir qual dica precisa?',
                     'Pode repetir que sua dúvida?']

    frases_solicitar_cor = [ 'Peça uma dica sobre pintura ou desenho',
                             'Vamos lá. Peça-me informações sobre desenho ou pintura',
                             'Vá em frente, diga-me algo como: dica de pintura com guache']

    if 'paint' in convert_errors:
        return question(random.choice(frases_duvida))
    
    if paint is None:
        return question(random.choice(frases_solicitar_cor))

    paint_without_accentuation = unidecode.unidecode(paint)

    if paint_without_accentuation in tipos_pintura_disponiveis:
    	msg = paint_hints(paint_without_accentuation)
    	return statement(random.choice(msg))

    return question('Ainda não sei sobre esta categoria. Pode tentar outra?')

@ask.intent('MatchingColors', convert={'cor': str})
def say_age(cor):
    frases_duvida = ['Poderia repetir uma cor?',
                     'Poderia me dizer uma cor válida?']

    frases_solicitar_cor = [ 'Diga-me uma cor.',
                             'Que cor quer consultar?',
                             'Para saber a combinação de cores, diga uma cor válida']

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

    frases_resposta = [  'A cor resultante é {}',
                         'A minha mistura deu {}',
                         'Misturei, misturei e misturei. Deu {}"']

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
        if msg == "break":
        	return question(random.choice(frases_mistura_inexistente))

        return statement(random.choice(frases_resposta).format(msg))
  
    return question('Ops... não sei misturar estas cores. Utilize cores como: preto, branco, azul, amarelo ou vermelho')




@ask.intent('AMAZON.StopIntent')
def stop():
    return statement("Até mais")


@ask.intent('AMAZON.HelpIntent')
def help():
    return statement("Olá terráqueo. Eu sei coisas sobre arte e estou pronta para compartilhar conhecimento com você." 
    				 "Se quer saber como misturar cores diga algo como: mistura de amarelo com azul."
    				 "Você também pode descobrir combinações de cores básicas. Você pode dizer por exemplo: qual cor combina com azul?"
    				 "Para receber dicas relacionadas a pintura ou desenho, fale algo como: dica de pintura com guache.")


@ask.intent('AMAZON.CancelIntent')
def cancel():
    return statement("Até mais")


@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == "__main__":
    app.run(debug=True)