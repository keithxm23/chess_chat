from flask import Flask, render_template, session, copy_current_request_context, request
from flask_socketio import SocketIO, emit, disconnect, join_room, leave_room
import pytchat
import re
from datetime import datetime
from db import insert_yt_id, check_id_present
from move_parser import detect_move



async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_.async_mode)

@app.route('/changelog')
def changelog():
    return render_template('changelog.html', async_mode=socket_.async_mode)

@app.route('/moves')
def moves():
    return render_template('moves/index.html', async_mode=socket_.async_mode)

@socket_.on('my_event', namespace='/test')
def test_message(message):
    print(message)
    yt_id = message['yt_id']
    processing = check_id_present(yt_id)
    if processing:
        print('already processing ytid, skipping')
        join_room(yt_id)
        pass
    else:
        print('adding ytid to db and emitting events')
        insert_yt_id(yt_id)
        join_room(yt_id)
        session['receive_count'] = session.get('receive_count', 0) + 1
        chat = pytchat.create(video_id=message['yt_id'], interruptable=False)
        #chat = pytchat.create(video_id='rS-FpbFuP0M', interruptable=False)
        #chat = pytchat.create(video_id='CULDhDOFEKw', interruptable=False)
        #chat = pytchat.create(video_id='CULDhDOFEKw', interruptable=False, seektime=900)
        #chat = pytchat.create(video_id='rS-FpbFuP0M', interruptable=False, seektime=900)
        while chat.is_alive():
            for c in chat.get().sync_items():
                #print(f"PROCESSING: {c.datetime} [{c.author.name}]- {c.message}")
                move = detect_move(c.message)
                time_obj = datetime.strptime(f"{c.datetime} EST", '%Y-%m-%d %H:%M:%S %Z')
                utc_time = time_obj.strftime('%m/%d/%Y %H:%M:%S %Z')


                print(f"PROCESSING: {c.datetime} {c.timestamp} [{c.author.name}]- {c.message} {c.elapsedTime}")

                if move == None:
                    print(f"SKIPPING: {c.datetime} [{c.author.name}]- {c.message}")
                    continue
                print(f"{session['receive_count']} EMITTING MOVE: {move} :::: {c.datetime} [{c.author.name}]- {c.message}")
                emit('my_response',
                    {'move': move,
                      'count': session['receive_count'],
                      'author': c.author.name,
                      'author_id': c.author.channelId,
                      'img_url': c.author.imageUrl,
                      'badge_url': c.author.badgeUrl,
                      'isMod': c.author.isChatModerator,
                      'utctime': utc_time
                      },
                    to=yt_id
                    )
                session['receive_count'] = session.get('receive_count', 0) + 1
        leave_room(yt_id)
        disconnect()



#@socket_.on('my_broadcast_event', namespace='/test')
#def test_broadcast_message(message):
#    session['receive_count'] = session.get('receive_count', 0) + 1
#    emit('my_response',
#         {'data': message['data'], 'count': session['receive_count']},
#         broadcast=True)


@socket_.on('disconnect_request', namespace='/test')
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()

    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']},
         callback=can_disconnect)


if __name__ == '__main__':
    #socket_.run(app, host='0.0.0.0', debug=True)
    socket_.run(app, debug=True)
