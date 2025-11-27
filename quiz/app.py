from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'quiz_secret_key'

perguntas = [
    {
        "id": 1,
        "pergunta": "Qual é a capital do Brasil?",
        "opcoes": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"],
        "correta": "Brasília"
    },
    {
        "id": 2, 
        "pergunta": "Quantos lados tem um triângulo?",
        "opcoes": ["2 lados", "3 lados", "4 lados", "5 lados"],
        "correta": "3 lados"
    },
    {
        "id": 3,
        "pergunta": "Qual planeta é conhecido como Planeta Vermelho?",
        "opcoes": ["Vênus", "Júpiter", "Marte", "Saturno"],
        "correta": "Marte"
    }
]

@app.route('/')
def index():
    # Reinicia o quiz
    session['pergunta_atual'] = 0
    session['respostas'] = []
    session['mostrar_resultado'] = False
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
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
                         pergunta=pergunta,
                         pergunta_numero=pergunta_atual + 1,
                         total_perguntas=len(perguntas),
                         respostas=respostas,
                         mostrar_resultado=mostrar_resultado)

@app.route('/proxima', methods=['POST'])
def proxima():

    session['pergunta_atual'] = session.get('pergunta_atual', 0) + 1
    session['mostrar_resultado'] = False
    return redirect(url_for('quiz'))

@app.route('/resultado')
def resultado():
    respostas = session.get('respostas', [])
    total_corretas = sum(1 for r in respostas if r['acertou'])
    
    return render_template('resultado.html',
                         respostas=respostas,
                         total_corretas=total_corretas,
                         total_perguntas=len(perguntas))

if __name__ == '__main__':
    app.run(debug=True)