#!/usr/bin/env python
from __future__ import print_function
import sys
import os
import requests
import json
from var import DIR
SPARK_URI="https://api.ciscospark.com/v1/"

def check_dir(dir, message):

    if not os.path.isdir(dir):
        print ("FAILED: (%s) Could not find directory %s" % (message, dir))
        return False
    else:
        print ("PASSED: (%s) Located directory %s" % (message, dir))
        return True

def check_modules():
    with open("requirements.txt", "r") as f:
        status = True
        for module in f.read().splitlines():
            # hack for enum34, needs to be imported as enum
            if module == "enum34":
                module= "enum"
            try:
                __import__(module)
                print ("PASSED: Found module %s" % module)
            except ImportError:
                print ("FAILED Module %s not found" % module)
                status = False
    return status

def check_python():
    ispython3 = sys.version_info.major == 3
    if not ispython3:
        print ("FALIED: You are running python version %d.%d, not python3" %(sys.version_info.major, sys.version_info.minor))
        return False
    else:
        print ("PASSED: Found Python version %d.%d" %(sys.version_info.major, sys.version_info.minor))
        return True

def spark_get(sparkToken, uri):
    headers = {"Authorization" : "Bearer " + sparkToken, "Content-type": "application/json"}
    response = requests.get(url=SPARK_URI+uri, headers=headers)
    response.raise_for_status()
    return response.json()

def check_spark(sparkToken):
    try:
        response = spark_get(sparkToken, "people/me")
        print ("PASSED: you are registered on spark as %s" % response['emails'])
        return True
    except requests.exceptions.HTTPError as error:
        print ("FAILED: Spark could not get your identity. Error %s" % error)
        return False

def find_DNE_spark_room(sparkToken):
    # what is there are multiple
    try:
        response = spark_get(sparkToken, "rooms")
        for room in response['items']:
            if "DevNet Express Workshop" in room['title']:
                #print (room['title'], room['id'])
                return room['id']
        return None

    except requests.exceptions.HTTPError as error:
        print ("FAILED: Could not get roomlist. Error %s" % error)
        return None

def post_DNE_spark_room(sparkToken):
    message = "I just validated my DevNet Express Environment... looking forward to joining "
    roomId = find_DNE_spark_room(sparkToken)
    if roomId is None:
        print("ERROR: you are not subscribed to a DevNet Express Workshop room")
        raise ValueError("No spark room found")
    # append roomname to message
    data = { "roomId" : roomId, "text" : message}
    headers = {"Authorization": "Bearer " + sparkToken, "Content-type": "application/json"}
    response = requests.post(url=SPARK_URI + "messages", data=json.dumps(data), headers=headers)
    response.raise_for_status()
    return True

def main(sparkToken):
    print ("DIR: %s" % DIR)

    checkPython3 = check_python()

    checkGit = check_dir("%s/devnet-express-code-samples/.git" % DIR, "Git")

    checkEnv = check_dir("%s/env" %DIR, "Python Virual Environment")

    checkPostman = check_dir("/Applications/Postman.app/Contents/MacOS/", "Postman")

    checkModules = check_modules()

    checkSpark = check_spark(sparkToken)

    status = checkPython3& checkGit & checkEnv & checkPostman & checkModules & checkSpark
    print ("Verifcation status:", "SUCCESS" if status else "FAILED")
    # this should be if status
    if status:
        print("Posting success to spark room")
        try:
            post_DNE_spark_room(sparkToken)
            print("Setup completed")
        except ValueError as error:
            pass
        print ("ERROR: Spark Posting failed")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print ("Error## usage: %s <spark-token> " %sys.argv[0])
        exit(1)
    else:
        SPARK_TOKEN = sys.argv[1]
        main(SPARK_TOKEN)



