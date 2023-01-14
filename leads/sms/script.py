from .melipayamak import Api
# username = '09307267862'
# password = 'mgdfab6'
# api = Api(username,password)
# sms = api.sms()
# to = ['۰۹۳۰۷۲۶۷۸۶۲']
# _from = '50004001267862'
# text = 'تست وب سرویس ملی '
# response = sms.send(to,_from,text)
# print(response)

def send_messege_to_customer(id,mobile):
	text=""" درخواست شما ثبت شد.\nکد سرویس: {code}\nامداد موتور""".format(code = id)
	_from = '50004001267862'
	to 	  = mobile
	username = '09307267862'
	password = 'mgdfab6'
	api = Api(username,password)
	sms = api.sms()
	response = sms.send(to,_from,text)
	return response


def send_messege_to_technician(customer_phone,address,problem,model,mobile):
	text= """{customer_phone}\n {address}/ {problem}/ {model} \n با مشتری تماس بگیرید\nامداد موتور""".format(
		address=address,problem = problem, model = model,customer_phone = customer_phone)
	_from = '50004001267862'
	to 	  = mobile
	username = '09307267862'
	password = 'mgdfab6'
	api = Api(username,password)
	sms = api.sms()
	response = sms.send(to,_from,text)
	return response

def get_credit():
	username = '09307267862'
	password = 'mgdfab6'
	api = Api(username,password)
	sms = api.sms('rest')
	dic = sms.get_credit()
	val = dic["Value"]
	return int(float(val))

def send_messege(reciever,to_number:str,args:[]):
	import requests

	body_id={"technecian":96678,"customer":96679}
	data = {'bodyId': body_id[reciever], 'to': to_number, 'args': args}
	response = requests.post('https://console.melipayamak.com/api/send/shared/7d8081d8959147c0b3be58abd61ca650', json=data)
	print(response.json())


	