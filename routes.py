import redis
import shortuuid

from flask import Flask, render_template, request, redirect, url_for
from forms import AddAlarmForm

app = Flask(__name__) 
persist = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/alarms', methods=['GET'])		
def index_alarm():
	alarms = map(lambda key : (key, persist.hgetall('alarm:'+key)) ,persist.smembers('alarms'))
	return render_template('alarms.html', alarms=alarms)	

@app.route('/alarm/new', methods=['GET', 'POST'])
def new_alarm():
	form = AddAlarmForm(csrf_enabled=False)
	if request.method == 'POST':
		uuid = shortuuid.uuid()
		key = 'alarm:'+uuid
		persist.hset(key, 'hour', form.hour.data)
		persist.hset(key, 'minute', form.minute.data)
		persist.hset(key, 'name', form.name.data)
		persist.hset(key, 'mode', form.mode.data)
		persist.sadd('alarms', uuid)
		return redirect(url_for('index_alarm'))
  	return render_template('new.html', form=form)	
		
@app.route('/alarm/<key>')
def delete_alarm(key):
	persist.delete('alarm:'+key)
	persist.srem('alarms', key)
	return redirect(url_for('index_alarm'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80, debug=True)