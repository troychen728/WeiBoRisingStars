import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('WeiboParsing.log',mode = 'a+')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

f = open("testdata.json", "r")
Users = json.loads(f.read())

_ustart_time = "2017-12-05 03:12:45"
_uend_time = "2017-12-05 16:17:50"
_start_time = "2017-12-05 03:12:49"
_end_time = "2017-12-05 16:17:53"
missing = 0

def main():
	userX = []

	for user in Users:
		#print json.dumps(user)
		weibox = getWeibo(_start_time,_end_time, Users[user]['weibo'],user)
		if weibox != {}:
			try :
				assert Users[user]['followers_count'][_uend_time] != 0
			except:
				logger.warning("key missing for user %s" % user)
			assert Users[user]['followers_count'][_ustart_time] != 0
			assert Users[user]['statuses_count'][_uend_time] != 0
			assert Users[user]['statuses_count'][_ustart_time] != 0
			assert Users[user]['friends_count'][_uend_time] != 0 
			follower = Users[user]['followers_count'][_uend_time] - Users[user]['followers_count'][_ustart_time]
			statuses = Users[user]['statuses_count'][_uend_time] - Users[user]['statuses_count'][_ustart_time] 
			friends = Users[user]['friends_count'][_uend_time] 
			userinfo = weibox 
			userinfo['follower'] = follower
			userinfo['statuses'] = statuses
			userinfo['friends'] = friends
			if Users[user]['gender'] == 'f':
				userinfo['gender'] = 1
			else:
				userinfo['gender'] = 0
			userinfo['startfo'] = Users[user]['followers_count'][_ustart_time]
			userinfo['startsta'] = Users[user]['statuses_count'][_ustart_time]
			userinfo['verified'] = Users[user]['verified']
			userinfo['percentfo'] = float (userinfo['follower']) / userinfo['startfo'] * 10000
			userinfo['percentrepo'] = float (userinfo['repost']) / userinfo['startrepost'] * 100
			userinfo['percentlike'] = float (userinfo['likes']) / userinfo['startlikes'] * 100
			userinfo['percentco'] = float (userinfo['comment']) / userinfo['startcomment'] * 100
			userinfo['bi_follow'] = Users[user]['bi_followers_count']
			userX.append(userinfo)

	for user in userX:
		print json.dumps(user, indent=4)
	f = open("Tabledata.json", "w+")
	f.write (json.dumps(userX, indent = 4))
	print len(userX)

def getWeibo(starttime, endtime, weibo, uid):
	max = 0
	picindex = 0
	count = 0
	lenindex = 0
	for weiboid in weibo:
		count += 1
		if len(weibo[weiboid]) >= max :
			max = len(weibo[weiboid])
			sweibo = weibo[weiboid]
		if weibo[weiboid][0]['pic'] == True:
			picindex += 1
		lenindex += weibo[weiboid][0]['text']
	endpost = {}
	startpost = {}
	for records in sweibo:
		if records['timestamp'] == starttime:
			startpost = records
		if records['timestamp'] == endtime:
			endpost = records
	weibox = {}
	if endpost !={} and startpost != {}:
		weibox = {
			'picindex' : picindex / count,
			'lenindex' : lenindex / count,
			'repost' : endpost['reposts_count'] - startpost['reposts_count'],
			'likes' : endpost['attitudes_count'] - startpost['attitudes_count'],
			'comment' : endpost['comments_count'] - startpost['comments_count'],
			'startrepost' : startpost['reposts_count'],
			'startlikes' : startpost['attitudes_count'],
			'startcomment' : startpost['comments_count'],
			'time' : startpost['time'],
			'uid' : uid
		}
	"""if weibox == {}:
		print "1 missing"
	weibox['uid'] = uid"""
	return weibox

"""def getaverage():
	for user in Users:"""

		
if __name__ == "__main__":
    main()