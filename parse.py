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
	idindex = 0
	for user in Users:
		idindex += 1
		#print json.dumps(user)
		(weibox,weibol) = getWeibo(_start_time,_end_time, Users[user]['weibo'],user)
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
			userinfo['idindex'] = idindex
			keylist = Users[user]['followers_count'].keys()
			keylist.sort()
			prev = ''
			diffl = []
			for key in keylist:
				if prev != '':
					difffo = Users[user]['followers_count'][key] - Users[user]['followers_count'][prev]
					diffl.append(difffo)
				prev = key 
			i = 0
			try:
				assert len(diffl) == len(weibol)
				for weibo in weibol: 
					weibo['difffo'] = diffl[i]
					weibo['timerank'] = i + 1
					i += 1
					weibo.update(userinfo)
				userX = userX + weibol
			except:
				print user
			

			


	#for user in userX:
		#print json.dumps(user, indent=4)
	f = open("Paneldata.json", "w+")
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
	prevweibo = {}
	weiboxl = []
	for records in sweibo:
		if records['timestamp'] == starttime:
			startpost = records
		if records['timestamp'] == endtime:
			endpost = records
		if prevweibo != {}:
			singleweibo = {
				'diffrepo' : records['reposts_count'] - prevweibo['reposts_count'],
				'diffco' : records['comments_count'] - prevweibo['comments_count'],
				'difflike' : records['attitudes_count'] - prevweibo['attitudes_count'],
				'timestamp' : records['timestamp']
			}
			weiboxl.append(singleweibo)
		prevweibo = records
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
	"""for singleweibo in weiboxl:
		singleweibo.update(weibox)
		print json.dumps(singleweibo, indent = 4)"""
	"""if weibox == {}:
		print "1 missing"
	weibox['uid'] = uid"""
	return (weibox, weiboxl) 

"""def getaverage():
	for user in Users:"""

		
if __name__ == "__main__":
    main()