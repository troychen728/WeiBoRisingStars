import json

def parsejson(textname):
	lines = open(textname, 'r').read().split('\n')
	#print lines
	data = []
	j = ''
	for line in lines:
		if line != '':
			j = json.loads(line)
			data.append(j)

	return data 
	#print json.dumps(j)

def main():
	parsejson('data.json')

if __name__ == "__main__":
    main()