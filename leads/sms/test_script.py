from melipayamak import Api
#username = '09307267862'
#password = 'mgdfab6'
#api = Api(username,password)
#sms = api.sms()
#to = ['09307267862,09373150352']
#_from = '50004001267862'
#text = 'تست وب سرویس ملی پیامک'
#response = sms.send(to,_from,text)
#print(response)

def send_messege_to_customer(full_name, id,mobile):
	text="""جناب {full_name} سفارش درخواست شما ثبت شد.\nامداد موتور\nکد سرویس: {code}""".format(full_name=full_name,code = id)
	_from = '50004001267862'
	to 	  = mobile
	username = '09307267862'
	password = 'mgdfab6'
	api = Api(username,password)
	sms = api.sms()
	response = sms.send(to,_from,text)
	return response


def send_messege_to_technician(customer_phone,address,problem,mobile):
	text= """امداد موتور\n آدرس:\n{address}\nمشکل:\n{problem}\nشماره تماس:\n{customer_phone}\nجهت هماهنگی با مشتری تماس بگیرید\nامداد موتور.""".format(address=address,problem = problem, customer_phone = customer_phone)
	_from = '50004001267862'
	to 	  = mobile
	username = '09307267862'
	password = 'mgdfab6'
	api = Api(username,password)
	sms = api.sms()
	response = sms.send(to,_from,text)
	return response
