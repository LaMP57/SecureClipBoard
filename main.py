from flask import Flask, request, render_template
from redis import Redis
import json
import datetime
import jiami

app = Flask(__name__)
redis = Redis()

@app.route('/', methods=['GET'])
def pagePost():
    return render_template('post.html')

@app.route('/get', methods=['GET'])
def pageGet():
    scKey = request.args.get("sc")
    if scKey == None:
        scKey = ''
    return render_template('get.html', scKey=scKey)

@app.route('/result/get', methods=['POST'])
def pageResultGet():
    scKey = request.form['sc']
    data = getData(scKey)
    return render_template('resultGet.html', data=data)

@app.route('/result/post', methods=['POST'])
def pageResultPost():
    text = request.form['text']
    expiration = request.form['expiration']
    if expiration == '1h':
        exTime = 3600
    elif expiration == '1d':
        exTime = 86400
    else:
        exTime = 604800
    if expiration == '1t':
        isOneTime = True
    else:
        isOneTime = False
    scKey = postData(text, exTime, isOneTime)
    return render_template('resultPost.html', scKey=scKey)

@app.template_filter('formatdatetime')
def format_datetime(ts):
    return "{:0>8}".format(str(datetime.timedelta(seconds=ts)))

def postData(text, exTime, isOneTime):
    index = jiami.getRandomString(8)
    aes = jiami.AES()
    eText = aes.encrypt(text)
    key = aes.getKey()
    data = json.dumps({'text': eText, 'isOneTime': isOneTime, 'readTimes': 0})
    redis.set(index, data, ex = exTime)
    return index + ':' + key

def getData(token):
    try:
        index = token.split(':')[0]
        key = token.split(':')[1]
        data = json.loads(redis.get(index))
        ttl = redis.ttl(index)
        data['readTimes'] += 1
        redis.set(index, json.dumps(data), ex = ttl)
        aes = jiami.AES(key)
        data['text'] = aes.decrypt(data['text'])
        data['status'] = 1
        data['ttl'] = ttl
        if data['isOneTime']:
            redis.delete(index)
    except:
        data = {'status': 0}
    return data

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=12700)