from flask import Flask, request, jsonify, render_template
import nltk
import Levenshtein
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from flask_cors import CORS

# Inicializar o NLTK
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Inicializar lematizador e stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('portuguese'))

# Função de pré-processamento de texto
def preprocess_text(text):
    words = nltk.word_tokenize(text, language='portuguese')
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words]
    return ' '.join(words)

# Carregar perguntas e respostas
perguntas_respostas = {
    "o que é cidadania italiana": "É o status legal que reconhece uma pessoa como cidadã da Itália, com direitos e deveres.",
    "quais são os requisitos para obter a cidadania italiana por descendência": "Provar descendência de um antepassado italiano e que a cidadania não foi renunciada na linha direta.",
    "posso obter cidadania italiana por casamento": "Sim, após um período de residência na Itália ou três anos de casamento fora da Itália.",
    "quanto tempo leva para reconhecer a cidadania italiana": "Geralmente leva entre 2 a 4 anos.",
    "quais documentos são necessários para a cidadania italiana por descendência": "Certidões de nascimento, casamento e óbito dos ascendentes italianos e prova da continuidade da cidadania.",
    "preciso saber falar italiano para obter a cidadania": "Para algumas modalidades, como por residência, é necessário conhecimento básico de italiano.",
    "posso ter dupla cidadania italiana": "Sim, a Itália permite a dupla cidadania.",
    "como é o processo de naturalização": "Requer residência legal na Itália, prova de integração na sociedade e exame de língua italiana.",
    "o que é jure sanguinis": "É o princípio que permite obter a cidadania com base na nacionalidade dos antepassados.",
    "filhos de italianos nascidos no exterior têm direito à cidadania": "Sim, mas é importante registrar o nascimento no consulado italiano."
}

# Função para encontrar a resposta
def encontrar_resposta(pergunta):
    menor_distancia = float("inf")
    melhor_resposta = ""

    pergunta_processada = preprocess_text(pergunta)
    print(f"Pergunta pré-processada: {pergunta_processada}")

    for p, r in perguntas_respostas.items():
        distancia = Levenshtein.distance(pergunta_processada, preprocess_text(p))
        print(f"Comparando com: {p}, Distância: {distancia}")
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_resposta = r

    if menor_distancia <= 10:  # Ajuste o limiar de distância conforme necessário
        return melhor_resposta
    else:
        return "Pergunta não encontrada."


# Inicializar o Flask
app = Flask(__name__)
CORS(app)  # Permitir todas as origens por padrão (em desenvolvimento)

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar perguntas
@app.route('/perguntar', methods=['POST'])
def perguntar():
    data = request.json
    pergunta = data.get('pergunta')
    resposta = encontrar_resposta(pergunta)
    return jsonify({'resposta': resposta})

if __name__ == '__main__':
    app.run(debug=True)
