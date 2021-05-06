from flask import Flask
from flask import request
from flask import jsonify
import requests

app = Flask(__name__)

URL = 'https://api.telegram.org/bot1701407124:AAGgJGWIdsqTu653f6ftnVrvslDXppkmhtg/'
DATA_URL = 'https://playhearthstone.com/en-us/api/community/leaderboardsData?region='

def sendMessage(chat_id, text):
    url = URL+'sendMessage'
    message={'chat_id': chat_id, 'text': text}
    req = requests.post(url, json = message)
    return req.json()

def get_data(server, mode, season):
    url = DATA_URL + str(server) +'&leaderboardId=' + str(mode) + '&seasonId=' + str(season)
    req = requests.get(url).json()
    return req

def get_season(season):
    ses = (season - 63)%12
    year = 2019+(season - 63)//12
    month = 'none'
    if ses == 0:
        month = 'январь'
    elif ses == 1:
        month = 'февраль'
    elif ses == 2:
        month = 'март'
    elif ses == 3:
        month = 'апрель'
    elif ses == 4:
        month = 'май'
    elif ses == 5:
        month = 'июнь'
    elif ses == 6:
        month = 'июль'
    elif ses == 7:
        month = 'август'
    elif ses == 8:
        month = 'сентябрь'
    elif ses == 9:
        month = 'октябрь'
    elif ses == 10:
        month = 'ноябрь'
    else:
        month = 'декабрь'
    return (month, year)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        req = request.get_json()
        chat_id = req['message']['chat']['id']
        message = req['message']['text'].split()
        if message[0] == '/stat':
            nickname = message[1]
            server = message[2]
            form = message[3]
            season = message[4]
            stat = []
            for i in range(int(season), 91):
                if i != 79:
                    req = get_data(server, form, i)
                    for nick in req['leaderboard']['rows']:
                        if nick['accountid'] == nickname:
                            stat.append((nick['rank'], i))
            if len(stat) == 0:
                sendMessage(chat_id, text='Этот игрок не занимал место в топ 200 за указанный период')
            else:
                s = 'Результаты игрока ' + nickname + ':\n'
                for res in stat:
                    f = get_season(res[1])
                    s += str(res[0]) + ' место ' + f[0] + ' ' + str(f[1]) + ' года\n'
                sendMessage(chat_id, text=s)
        if message[0] == '/best':
            nickname = message[1]
            server = message[2]
            form = message[3]
            season = message[4]
            best_result = 201
            ses = 0
            for i in range(int(season), 91):
                if i != 79:
                    req = get_data(server, form, i)
                    for nick in req['leaderboard']['rows']:
                        if nick['accountid'] == nickname and nick['rank'] < best_result:
                            best_result = nick['rank']
                            ses = i
            if ses == 0:
                sendMessage(chat_id, text='Этот игрок не занимал место в топ 200 за указанный период')
            else:
                f = get_season(ses)
                s = 'Лучшая позиция игрока ' + nickname + ' за указанный период -- ' + str(best_result) +' место в сезоне '+f[0]+' ' + str(f[1]) + ' года'
                sendMessage(chat_id, text=s)
        return jsonify(req)
    return'<h1>AppBridge</h1>'


if __name__ == '__main__':
    app.run()
