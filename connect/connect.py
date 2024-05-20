import sys
sys.path.append('C:/Users/moner/Documents/Projekty/lab08/')

from flask import Flask, request, jsonify, send_from_directory
from game.engine import ShishimaGame

game = ShishimaGame()
games = {}
app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/start', methods=['POST'])
def start_game():
    game_id = request.json.get('game_id')
    games[game_id] = ShishimaGame()  
    return jsonify({'message': f'Game {game_id} started'}), 200

@app.route('/setpawns', methods=['POST'])
def set_pawns():
    try:
        data = request.get_json()
        game_id = data.get('game_id')
        if game_id is None:
            return jsonify({'message': 'game_id is missing'}), 400
        player = data.get('player')
        positions = data.get('positions')
        game = games.get(game_id)
        if game is None:
            return jsonify({'message': 'Invalid game_id'}), 400
        game.set_pawns(player, positions)
        return jsonify({'message': f'Player {player} set pawns'}), 200

    except Exception as e:
        app.logger.error(f"Error in set_pawns: {e}")
        return jsonify({'message': 'Internal Server Error'}), 500

@app.route('/move', methods=['POST'])
def move_pawn():
    data = request.get_json()
    player = data.get('player')
    start = data.get('start')
    end = data.get('end')
    game.move_pawns(player, start, end)
    return jsonify({'message': 'Move successful'}), 200


@app.route('/check', methods=['GET'])
def check_win():
    player = request.args.get('player')
    if game.check_win(player):
        return jsonify({'message': f'Player {player} wins!'}), 200
    else:
        return jsonify({'message': 'Game continues'}), 200

@app.route('/save', methods=['POST'])
def save_game():
    game.save_game()
    return jsonify({'message': 'Game saved'}), 200

@app.route('/load', methods=['POST'])
def load_game():
    filename = request.get_json().get('filename')
    if filename is None:
        return jsonify({'message': 'Brakuje nazwy pliku'}), 400
    try:
        game.load_game(filename)
        return jsonify({'message': 'Gra została załadowana'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
