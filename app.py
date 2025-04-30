from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, send
import requests

app = Flask(__name__)
socketio = SocketIO(app)

PANDASCORE_API_KEY = 'WqcdmxmHGmmd5eH4Ag4mCOxXqyMWFLSYo61BJpWhwqTgVSdcPz0'

furia_id = 129384

# Função para obter resultados da FURIA
def get_furia_match_results():
    headers = {'Authorization': f'Bearer {PANDASCORE_API_KEY}'}

    url = f'https://api.pandascore.co/csgo/matches?filter[opponent_id]={furia_id}&filter[status]=finished&sort=-begin_at&page[size]=5'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            return response.json()
        except Exception as e:
            print("Erro ao processar resposta:", e)
            return []
    else:
        print(f"Erro ao acessar a API: {response.status_code} - {response.text}")
        return []




# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para obter resultados da FURIA
@app.route('/get_furia_results')
def get_furia_results():
    furia_matches = get_furia_match_results()
    return jsonify(furia_matches)


# Rota de recebimento e envio de mensagens
@socketio.on('message')
def handle_message(msg):
    print('Mensagem recebida: ' + msg)
    send(msg, broadcast=True)

# Evento de conexão
@socketio.on('connect')
def handle_connect():
    print("Novo usuário conectado!")
    send("Novo fã entrou no chat!", broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
