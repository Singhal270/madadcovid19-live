from django.shortcuts import render,redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from .models import *
from django.db.models import Q
from .form import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from json import loads
import requests
from logging import getLogger
from dialogflow_fulfillment import  QuickReplies,Card,Context, WebhookClient
import timeago
from datetime import datetime, timezone
import pytz
import math
# logger = getLogger('django.server.webhook')


def helpdata(city,res):
	output=Supplier.objects.filter(status="helpful",city__name=city,resources__name=res).first()
	print(output)
	if output:
		now  = datetime.now()
		tz=pytz.timezone('Asia/Kolkata')
		now = now.astimezone(tz)
		name=output.name
		number=str(output.Number)
		email=output.email
		des=output.description
		updated=str(timeago.format(output.date_created,now))
		dic={"name":name,"email":email,"des":des,"number":number,"updated":updated,"id":output.id,"isany":True}
		return(dic)
	else:
		dic={"isany":False}
		return(dic)



def handler(agent:WebhookClient)->None:
	con=Context(agent.context, agent.session)
	city=con.get("delivered")["parameters"]["geo-city"]
	resources=con.get("delivered")["parameters"]["resources"]
	print(city)
	print(resources)
	dic=helpdata(city,resources)
	if dic["isany"]:
		con.get("delivered")["parameters"]["id"]=dic['id']
		agent.add("Here is the detail we have found, might be helpful for you")
		agent.add(dic['name'] +'\n' + dic['number'] +'\n' + dic["email"] +'\n' +dic["des"] + '\n' +"last updated  " + dic['updated'])
		agent.add(" please give us you feedback on this supplier \n say helpful if it is useful,\n out of stock,\n say not answering or unresponsive if not replying,\n say fraud or scam,\n say wrong or invalid if it is wrong number")
	else:
		con.delete("delivered")
	

def handler2(agent:WebhookClient)->None:
	con=Context(agent.context, agent.session)
	city=con.get("delivered")["parameters"]["geo-city"]
	resources=con.get("delivered")["parameters"]["resources"]
	pk_id=con.get("delivered")["parameters"]["id"]
	feed=con.get("delivered")["parameters"]["feedback"]
	sup=Supplier.objects.get(pk=pk_id)
	sup.status=feed
	sup.save()
	print(city)
	print(resources)
	if not feed=="helpful":
		dic=helpdata(city,resources)
		if dic["isany"]:
			con.get("delivered")["parameters"]["id"]=dic['id']
			agent.add("Here is the detail we have found, might be helpful for you")
			agent.add(dic['name'] +'\n' + dic['number'] +'\n' + dic["email"] +'\n' +dic["des"] + '\n' +"last updated  " + dic['updated'])
			agent.add(" please give us you feedback on this supplier \n say helpful if it is useful,\n out of stock,\n say not answering or unresponsive if not replying,\n say fraud or scam,\n say wrong or invalid if it is wrong number")
		else:
			con.delete("delivered")
	else:
		agent.add("thanks for information, I am happy to help you")
		con.delete("delivered")


@csrf_exempt
def webhook(request:HttpRequest)->HttpResponse:
	if request.method=='POST':
		req=loads(request.body)

		# logger.info(f'Request headers:{dict(request.headers)}')
		# logger.info(f'Request body:{req}')

		agent = WebhookClient(req)
		if(agent.intent=="loop-back"):
			agent.handle_request(handler2)
		else:
			agent.handle_request(handler)

		# logger.info(f'Response body:{agent.response}')

		return JsonResponse(agent.response)
	return HttpResponse("hello")



def add(request):
	if request.method=='POST':
		fm = SupplierForm(request.POST)
		if fm.is_valid():
			print(request.POST.getlist("resources"))
			obj=fm.save(commit=False)
			obj.status="unvarified"
			# print(obj.resources)
			obj.save()
			fm.save_m2m()
			messages.success(request,'regitration sucessfully')
			return redirect('/add')
		else:
			messages.error(request,'somthing went wrong. Either you have entered wrong phone number or have not filled required field')
			return redirect('/add')
	else:
		fm = SupplierForm()
	return render(request, 'add.html',{'form':fm})