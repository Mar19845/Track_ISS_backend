import requests
import json
class Utils():
    @staticmethod
    def ReadFile(file):
        tuples_list = []

        f = open(file)
        lines = [line.replace('\n','').rstrip().lstrip() for line in f.readlines()]

        for index in range(len(lines)):
            if 'ISS' in lines[index]:
                tuples_list.append([lines[index+1],lines[index+2]])

        f.close()
        return tuples_list
    @staticmethod
    def make_request(id):
        r = requests.get('https://api.wheretheiss.at/v1/satellites/'+str(id)+'/tles')
        response = json.loads(r.content.decode("utf-8"))
        return response
from datetime import datetime

# time_in_utc variable will be the utc time 
time_in_utc = datetime.utcnow()

# If you want to make it more fancier:
formatted_time_in_utc = time_in_utc.strftime('%Y-%m-%d %H:%M:%S')

gt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print(gt)
print(formatted_time_in_utc)
print(time_in_utc)