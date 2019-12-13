import requests
import socket
import glob


#
# you have to provide your own .mp4
#
#files = {'file': open('keypoints.json')}

ip = "10.153.108.91"
for json in glob.glob("*.json"):
    #files = {'file': open(json)}
    with open (json, "r") as myfile:
        data = myfile.read()
        #print(data)
        responce = requests.post("http://" + ip + ":8080/json", data=data)
        print(json, responce.content.decode('utf-8'))