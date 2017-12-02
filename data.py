import json
import requests
import datetime
import time
_access_token = "2.00WEUbgG0ftSid4e7cdf92bfNwscEE"
_statuese_url = "https://api.weibo.com/2/statuses/home_timeline.json"
def getdata(ids, timeS):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	r = requests.get(("https://api.weibo.com/2/users/counts.json?access_token=%s&uids=" %_access_token) + ids)
	d = [json.loads(line) for line in r.iter_lines()]
	data = d[0]

		#print json.dumps(data)
	f = open('Followers%s.json' %timeS,'a+')
	for dic in data:
		dic['timestamp'] = st 
	f.write(json.dumps(data))
	f.write('\n')
		#print data[45]['timestamp']

def getstatuese(timeS):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	url = _statuese_url + "?access_token=" + _access_token
	r = requests.get(url)
	d = [json.loads(line) for line in r.iter_lines()]
	data = d[0]['statuses']

	print json.dumps(data)
	f = open('Statuess%s.json' %timeS,'a+')
	for dic in data :
		dic['timestamp'] = st 
	# add a new dict class here
	# just keep the info we want 
	f.write(json.dumps(data))
	f.write('\n')

def main():
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

	lines = open('uid.txt','r').read().split('\n')
	ids = lines[0]
	for i in range(1,len(lines)):
		ids = ids + ',' + lines[i]
	#print ids

	try:
		while True:
			getdata(ids, st)
			getstatuese(st)
			time.sleep(600)

	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
    main()