import json
f = open("testdata.json", "r")
Users = json.loads(f.read())


def main():

	getaverage()

def getaverage():
	for user in Users:
		
if __name__ == "__main__":
    main()