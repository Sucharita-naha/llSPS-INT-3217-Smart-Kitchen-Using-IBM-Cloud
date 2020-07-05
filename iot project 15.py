import time
import sys
import ibmiotf.application
import ibmiotf.device
import requests
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
url = "https://www.fast2sms.com/dev/bulk"
#Provide your IBM Watson Device Credentials
organization = "kg0p6r"
deviceType = "raspberrypi"
deviceId = "project-15"
authMethod = "token"
authToken = "123456789"
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        if cmd.data['command']=='exhauston':
                print("EXHAUST ON IS RECEIVED")
        elif cmd.data['command']=='exhaustoff':
                print("EXHAUST OFF IS RECEIVED") 
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)

	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.connect()
cylinder_weight=10
jar_weight=1000
cyl_empty=0
jar_empty=0
while True:

        cylinder_weight=cylinder_weight-1
      
        jar_weight=jar_weight-14

        if(cylinder_weight>0 and cylinder_weight<=3):
                current_status="low"
        elif(cylinder_weight>3 and cylinder_weight<=7):
                current_status="medium"
        elif(cylinder_weight>7 and cylinder_weight<=10):
                current_status="high"
        else:
                cylinder_weight=0
                status="empty"
                if(cyl_empty==0):
                        
                        querystring = {"authorization":"CEBM7ZYzfkWlyPrtnmJNoH3xAGFLjhsX06ceg5UuiqQp2dS4RVMpPyG0vdxQOq5N1ktTiLhrERac6wWU","sender_id":"FSTSMS","message":"The cylinder is empty","language":"english","route":"p","numbers":"9952162247,7530015671,9500377352"}
                        headers = {'cache-control': "no-cache"}
                        response = requests.request("GET", url, headers=headers, params=querystring)
                        print(response.text)
                        cyl_empty=1



                        
        if(jar_weight>0 and jar_weight<=300):
                jar_status="low"
        elif(jar_weight>300 and jar_weight<=700):
                jar_status="medium"
        elif(jar_weight>700 and jar_weight<=1000):
                jar_status="high"
        else:
                jar_weight=0
                jar_status="empty"
                if(jar_empty==0):
                        querystring = {"authorization":"CEBM7ZYzfkWlyPrtnmJNoH3xAGFLjhsX06ceg5UuiqQp2dS4RVMpPyG0vdxQOq5N1ktTiLhrERac6wWU","sender_id":"FSTSMS","message":"The jar is empty","language":"english","route":"p","numbers":"9952162247,7530015671,9500377352"}
                        headers = {'cache-control': "no-cache"}
                        response = requests.request("GET", url, headers=headers, params=querystring)
                        print(response.text)
                        jar_empty=1
        gasleak=0               

        gasleak=gasleak+1
        
        if(gasleak==40):
                print('gas leak is detected')
                querystring = {"authorization":"CEBM7ZYzfkWlyPrtnmJNoH3xAGFLjhsX06ceg5UuiqQp2dS4RVMpPyG0vdxQOq5N1ktTiLhrERac6wWU","sender_id":"FSTSMS","message":"There is a gas leak","language":"english","route":"p","numbers":"9952162247,7530015671,9500377352"}
                headers = {'cache-control': "no-cache"}
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(response.text)
                jar_empty=1
        else:
                print('no gas leak')
                


        

                        
        data = {'cylinder_weight':cylinder_weight,'jar_weight':jar_weight,'current_status':current_status,'jar_status':jar_status}
        #print (data)


        def myOnPublishCallback():
            print ("Published cylinder_weight = %s " % cylinder_weight, "jar_weight = %s " % jar_weight ,"current_status = %s" % current_status,"jar_status = %s" % jar_status, "to IBM Watson")
        success = deviceCli.publishEvent("smart_kitchen", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        deviceCli.commandCallback = myCommandCallback

        client = Cloudant("fcf055c3-9b00-418e-a955-a88fd70d32d0-bluemix", "a10a022499db0fcd47dce369b941bb895d640c859923fae1fd2806ea5cbe4721",url="https://fcf055c3-9b00-418e-a955-a88fd70d32d0-bluemix:a10a022499db0fcd47dce369b941bb895d640c859923fae1fd2806ea5cbe4721@fcf055c3-9b00-418e-a955-a88fd70d32d0-bluemix.cloudantnosqldb.appdomain.cloud")
        client.connect()
        database_name = "project15"
        my_database = client.create_database(database_name)
        if my_database.exists():
                print(f"'{database_name}' successfully created.")
        record_data={'cylinder_weight':cylinder_weight,'jar_weight':jar_weight,'current_status':current_status,'jar_status':jar_status}
        new_document = my_database.create_document(record_data)
        if new_document.exists():
                print(f"Document  successfully created.")
        result_collection = Result(my_database.all_docs,include_docs=True)
        print(f"Retrieved minimal document:\n{result_collection[0]}\n")

# Disconnect the device and application from the cloud
deviceCli.disconnect()
















