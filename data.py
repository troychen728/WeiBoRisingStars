import json
import requests
import datetime
import time

def getdata(ids, duration):
	while 1: 
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		r = requests.get("https://api.weibo.com/2/users/counts.json?access_token=2.00xusAWD0YuxsZ10f9689fa7sIoHJC&uids=" + ids)
		d = [json.loads(line) for line in r.iter_lines()]
		data = d[0]

		#print json.dumps(data)
		f = open('data%s.json' %st,'a+')
		for dic in data:
			dic['timestamp'] = st 
		f.write(json.dumps(data))
		f.write('\n')
		print data[45]['timestamp']
		time.sleep(duration)

def main():
	lines = open('uid.txt','r').read().split('\n')
	ids = lines[0]
	for i in range(1,len(lines)):
		ids = ids + ',' + lines[i]
	#print ids

	try:
		while True:
			getdata(ids, 10)

	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
    main()