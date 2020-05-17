
#*****************************Project developed in flask framework*********************


from flask import Flask,redirect,url_for,render_template,request
import socket			# Import socket module
import threading        # Import socket threading module
import time

HB_INTERVAL = 5.0	   #sending heartbeat packet from simulator to adapter at 5 sec intervel
GPS_INTERVAL = 15.0    #sending GPS location packet from simulator to adapter at 5 sec intervel
METHOD = "AUTO"        #sending packet from simulator to adapter automatically
#        or
#METHOD = "WEB"       # sending packet from simulator to adapter through web interface developded in flask framework

IS_LOGIN = False

#**************************** web interface part**************************************
app = Flask(__name__)

@app.route('/')
def Simulator():
	return render_template("home.html")

@app.route('/data',methods = ["POST"])
def Login_view():
	global IS_LOGIN
	if request.method == 'POST':
		if "login" in request.form:
			if not IS_LOGIN:
				concox_login_web="78 78 11 01 03 51 60 80 80 77 92 88 22 03 32 01 01 AA 53 36 0D 0A"
				concoxlogin_web_byte=concox_login_web.encode()
				client.send(concoxlogin_web_byte)
			return  render_template("home.html")


		elif "heartbeat" in request.form:
			if IS_LOGIN:
				concox_hb_web="78 78 0B 23 C0 01 22 04 00 01 00 08 18 72 0D 0A"
				concox_hb_web_byte=concox_hb_web.encode()
				client.send(concox_hb_web_byte)
			return render_template("home.html")


		elif "gps" in request.form:
			if IS_LOGIN:
				concox_gps_web="78 78 22 22 0F 0C 1D 02 33 05 C9 02 7A C8 18 0C 46 58 60 00 14 00 01 CC 00 28 7D 00 1F 71 00 00 01 00 08 20 86 0D 0A"
				concox_gps_web_byte=concox_gps_web.encode()
				client.send(concox_gps_web_byte)
			return render_template("home.html")

#******************************AUTO**********************************************************


#**********sending heartbeat packet at 5 sec intervel******
def send_auto_heartbeat_packet(client,enable_hb):
	heartbeat="78 78 0B 23 C0 01 22 04 00 01 00 08 18 72 0D 0A"
	heartbeat_byt=heartbeat.encode()
	if enable_hb:
		client.send(heartbeat_byt)
		timer = threading.Timer(HB_INTERVAL, send_auto_heartbeat_packet,args=(client,enable_hb)).start()


#**********sending GPS packet at 5 sec intervel***********
def send_auto_gps_packet(client,enable_gps):
	gps="78 78 22 22 0F 0C 1D 02 33 05 C9 02 7A C8 18 0C 46 58 60 00 14 00 01 CC 00 28 7D 00 1F 71 00 00 01 00 08 20 86 0D 0A"
	gps_byt=gps.encode()
	if enable_gps:
		client.send(gps_byt)
		timer = threading.Timer(GPS_INTERVAL, send_auto_gps_packet,args=(client,enable_gps)).start()


#********sending and receiving login,heartbeat,Gps from and into adapter with help of TCP*********
def Clientsocket():
	global IS_LOGIN,METHOD
	client.connect(('127.0.0.1', 4444))
	print("[INFO]: Server connectd!")
	if METHOD == "AUTO":
		concox_login="78 78 11 01 03 51 60 80 80 77 92 88 22 03 32 01 01 AA 53 36 0D 0A"
		concox_login_byt=concox_login.encode()
		client.send(concox_login_byt)

	while not IS_LOGIN:
		data = client.recv(4096)
		if not data: break
		Rdata=data[:].decode("utf-8")
		if(Rdata[9:11] == "01"):
			print("[RESPONSE]: Login packet")
			IS_LOGIN = True
			break

	if METHOD == "AUTO":
		send_auto_heartbeat_packet(client,1)
		send_auto_gps_packet(client,1)


	if IS_LOGIN:
		print("[INFO]: Login Successful!")
		while IS_LOGIN:
			data = client.recv(4096)
			if not data: break
			Rdata=data[:].decode("utf-8")
			if(Rdata[9:11] == "23"):
				print("[RESPONSE]: Heartbeat")
			if(Rdata[9:11] == "22"):
				print("[RESPONSE]: GPS")


#**************flask framework run at ip ="127.0.0.1 and port=8888 ***********
def flaskThreadclient():
    app.run("127.0.0.1",8888,debug=True,use_reloader=False)

if __name__ == '__main__':

	print("=========================================")
	print("             Concox Simulator")
	print("=========================================")

#**********Web part and Auto(sending and recieving packet without web)runs at different threads*****
	threads=[]

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if METHOD == "WEB":
		thread_client=threading.Thread(target=flaskThreadclient)
		thread_client.start()
		threads.append(thread_client)

	new_threadC=threading.Thread(target=Clientsocket)
	new_threadC.start()
	threads.append(new_threadC)
	for thread in threads:
		thread.join()
