from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'quiz_secret_key'

quizzes = {
    'geografia': {
        'id': 'geografia',
        'titulo': 'Geografia Geral',
        'descricao': 'Teste seus conhecimentos sobre o mundo',
        'icon': '🌍',
        'perguntas': [
            {
                "id": 1,
                "pergunta": "Qual é a capital do Brasil?",
                "opcoes": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"],
                "correta": "Brasília"
            },
            {
                "id": 2,
                "pergunta": "Qual o maior país do mundo em extensão territorial?",
                "opcoes": ["China", "Estados Unidos", "Rússia", "Canadá"],
                "correta": "Rússia"
            }
        ]
    },
    
    'matematica': {
        'id': 'matematica',
        'titulo': 'Matemática Básica',
        'descricao': 'Desafios de cálculo e lógica',
        'icon': '🧮',
        'perguntas': [
            {
                "id": 1,
                "pergunta": "Quanto é 15 + 27?",
                "opcoes": ["32", "42", "52", "62"],
                "correta": "42"
            },
            {
                "id": 2,
                "pergunta": "Quantos lados tem um triângulo?",
                "opcoes": ["2 lados", "3 lados", "4 lados", "5 lados"],
                "correta": "3 lados"
            }
        ]
    },
    
    'ciencias': {
        'id': 'ciencias',
        'titulo': 'Ciências Naturais',
        'descricao': 'Conhecimentos sobre natureza e ciência',
        'icon': '🔬',
        'perguntas': [
            {
                "id": 1,
                "pergunta": "Qual planeta é conhecido como Planeta Vermelho?",
                "opcoes": ["Vênus", "Júpiter", "Marte", "Saturno"],
                "correta": "Marte"
            },
            {
                "id": 2,
                "pergunta": "Quantos ossos tem o corpo humano adulto?",
                "opcoes": ["156", "206", "256", "306"],
                "correta": "206"
            },
            {
                "id": 3,
                "pergunta": "Qual planeta habitam os seres humanos?",
                "opcoes": ["Marte", "Terra", "Plutão", "Júpiter"],
                "correta": "Terra"
            }
        ]
    },
    'quimica': {
        'id': 'quimica',
        'titulo': 'Química Básica',
        'descricao': 'Conhecimentos básicos de química',
        'icon': '🧑‍🔬',
        'perguntas': [
            {
                "id": 1,
                "pergunta": "Qual o número atômico do oxigênio?",
                "opcoes": ["8", "16", "24", "12"],
                "correta": "8"
            },
            {
                "id": 2,
                "pergunta": "Qual o número atômico do carbono?",
                "opcoes": ["14", "76", "24", "6"],
                "correta": "6"
            }
        ]
    }
}

@app.route('/')
def home():
    "Página inicial - Lista todos os quizzes"
    return render_template('home.html', quizzes=quizzes)

@app.route('/quiz/<quiz_id>')
def selecionar_quiz(quiz_id):
    "Seleciona um quiz específico e inicia"
    if quiz_id not in quizzes:
        return redirect(url_for('home'))
    
    session['quiz_id'] = quiz_id
    session['pergunta_atual'] = 0
    session['respostas'] = []
    session['mostrar_resultado'] = False
    
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    "Página do quiz em andamento"
    quiz_id = session.get('quiz_id')
    
    if not quiz_id or quiz_id not in quizzes:
        return redirect(url_for('home'))
    
    quiz_atual = quizzes[quiz_id]
    perguntas = quiz_atual['perguntas']
    pergunta_atual = session.get('pergunta_atual', 0)
    respostas = session.get('respostas', [])
    mostrar_resultado = session.get('mostrar_resultado', False)
    
    if pergunta_atual >= len(perguntas):
        return redirect(url_for('resultado'))
    
    pergunta = perguntas[pergunta_atual]
    
    if request.method == 'POST':
        resposta = request.form.get('resposta')
        if resposta:
            acertou = (resposta == pergunta['correta'])
            respostas.append({
                'pergunta': pergunta['pergunta'],
                'resposta_usuario': resposta,
                'resposta_correta': pergunta['correta'],
                'acertou': acertou
            })
            session['respostas'] = respostas
            session['mostrar_resultado'] = True
            return redirect(url_for('quiz'))
    
    return render_template('quiz.html',
                         quiz=quiz_atual,
                         pergunta=pergunta,
                         pergunta_numero=pergunta_atual + 1,
                         total_perguntas=len(perguntas),
                         respostas=respostas,
                         mostrar_resultado=mostrar_resultado)

@app.route('/proxima', methods=['POST'])
def proxima():
    "Avança para próxima pergunta"
    session['pergunta_atual'] = session.get('pergunta_atual', 0) + 1
    session['mostrar_resultado'] = False
    return redirect(url_for('quiz'))

@app.route('/resultado')
def resultado():
    "Mostra resultado final do quiz"
    quiz_id = session.get('quiz_id')
    
    if not quiz_id:
        return redirect(url_for('home'))
    
    quiz_atual = quizzes[quiz_id]
    respostas = session.get('respostas', [])
    total_corretas = sum(1 for r in respostas if r['acertou'])
    
    return render_template('resultado.html',
                         quiz=quiz_atual,
                         respostas=respostas,
                         total_corretas=total_corretas,
                         total_perguntas=len(quiz_atual['perguntas']))

@app.route('/voltar')
def voltar():
    "Volta para a página inicial"
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)