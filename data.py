import json
import requests
import datetime
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('WeiboRisingStar.log',mode = 'a+')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

_access_token = "2.00WEUbgG0ftSid4e7cdf92bfNwscEE"
_statuese_url = "https://api.weibo.com/2/statuses/home_timeline.json"
_weibo_url = "https://api.weibo.com/2/statuses/show.json"
Users = {}

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
	url = _statuese_url + "?access_token=" + _access_token + "&count=100"
	r = requests.get(url)
	d = [json.loads(line) for line in r.iter_lines()]
	data = d[0]['statuses']

	f = open('ids.txt', 'r')
	ids = f.read()

	rf = requests.get(("https://api.weibo.com/2/users/counts.json?access_token=%s&uids=" %_access_token) + ids)
	df = [json.loads(line) for line in r.iter_lines()]
	datafo = df[0]

	#print json.dumps(data)
	f = open('Statuess%s.json' %timeS,'w+')
	idlist = []
	for dic in data :
		uid = dic['user']['id']
		weiboid = dic['id']
		cunUser = dic['user']
		for user in datafo:
			if user['id'] == uid:
				statuses_count = user['statuses_count']
				friends_count = user['friends_count']
				followers_count = user['followers_count']

		#idlist.append(dic['user']['id'])
		if str(uid) not in Users:
			logger.info("Initialize user id %d" % uid)
			Users[str(uid)] = {
					'weibo' : [],
					'statuses_count' : {st : statuses_count},
					'friends_count' : {st : friends_count},
					'followers_count' : {st : followers_count},
					'gender' : cunUser['gender'],
					'verified' : cunUser['verified'],
					'bi_followers_count' : cunUser['bi_followers_count'],
					'allow_all_comment' : cunUser['allow_all_comment']

			}
			Users[str(uid)]['weibo'] = {
					str(weiboid) : [getWeibobyid(weiboid, dic)]
			}
		else : 
			if str(weiboid) not in Users[str(uid)]['weibo']:
				Users[str(uid)]['weibo'][str(weiboid)] = [getWeibobyid(weiboid, dic)]
			else :
				Users[str(uid)]['weibo'][str(weiboid)].append(getWeibobyid(weiboid, dic))
			if st not in Users[str(uid)]['statuses_count']:
				Users[str(uid)]['statuses_count'][st] = statuses_count
			if st not in Users[str(uid)]['friends_count']:
				Users[str(uid)]['friends_count'][st] = friends_count
			if st not in Users[str(uid)]['followers_count']:
				Users[str(uid)]['followers_count'][st] = followers_count
		#print (dic['user']['id'])

	#print Users
	"""ids = str(idlist[0])
	for i in range(1,len(idlist)):
		ids = ids + ',' + str(idlist[i])
	
	print ids"""

	# add a new dict class here
	# just keep the info we want 
	f.write(json.dumps(Users, indent = 4))
	f.write('\n')
	#f = open('ids.txt','w+')
	#f.write(ids)

def getWeibobyid(id, data):
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	logger.info("Called the function getWeibobyid, with weiboid %d" % id)
	"""url = _weibo_url + "?access_token=" + _access_token + "&id=%d" % id
	r = requests.get(url)
	d = [json.loads(line) for line in r.iter_lines()]
	data = d[0]
 	print data """
	weibodata = {
			'time' : data["created_at"],
			'weiboid' : id,
			'text' : len(data['text']),
			'reposts_count' : data['reposts_count'],
			'comments_count' : data['comments_count'],
			'attitudes_count' : data['attitudes_count'],
			'timestamp' : st
	}

	if 'original_pic' in data : 
		weibodata['pic'] = True 
	else :
		weibodata['pic'] = False
	return weibodata

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
			#getdata(ids, st)
			getstatuese(st)
			time.sleep(10)

	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
    main()