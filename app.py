from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)
games = {}  # room -> player list


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('join')
def on_join(data):
    room = data['room']
    user = data['user']
    games.setdefault(room, [])
    if user not in games[room]:
        games[room].append(user)
    join_room(room)
    emit('players', games[room], room=room)


@socketio.on('spin')
def on_spin(data):
    room = data['room']
    if room in games and len(games[room]) > 1:
        chosen = random.choice(games[room])
        emit('spinResult', chosen, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True)
