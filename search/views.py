from django.contrib.gis.geos import *
from django.contrib.gis.measure import D
from search.models import *
from forms import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.gis.geos import Point
from django.contrib import messages
import json


def search_view(request):


	if request.is_ajax():


		lat = request.GET['lat']
		lng = request.GET['lng']
		distance = request.GET['dist']
		c = "Uganda"

		search_point = fromstr("POINT(%s %s)" % (lng,lat))
		msg = Services.objects.filter(location__distance_lte=(search_point, D(km=distance)))

		to_json ={}
		to_jsonList =[]

		if msg.exists():

			for i in msg:

				
				to_json = {
					"center_id":i.id,
					"country":i.country,
					"city":i.city,
					"roadAddress":i.roadAddress,
					"centerName":i.centerName,
					"telephone":i.telephone,

					"lat":i.location.y,
					"lng":i.location.x
				}
				to_jsonList.append(to_json)
                     

	return HttpResponse(json.dumps({'ok':True,'msg':to_jsonList,'lng':"DANIEL"}),content_type='application/json')


def cdc_reg(request):

	if request.method == 'POST':


		form = ServicesForm(request.POST)

		if form.is_valid():
			new_point = Services()
			cd = form.cleaned_data
			coordinates = cd['coordinates'].split(',')
			
			new_point.country = cd['country']
			new_point.city = cd['city']
			new_point.roadAddress = cd['roadAddress']
			new_point.centerName = cd['centerName']
			new_point.telephone = cd['telephone']
			new_point.location = Point(float(coordinates[0]), float(coordinates[1]))

			new_point.save()
			messages.success(request, 'Registration successfull!')
			args = {}
			args.update(csrf(request))
			args['form'] = ServicesForm()

			return render_to_response('registration.html',args,context_instance=RequestContext(request))

		else:

			args = {}
			args.update(csrf(request))
			args['form'] = ServicesForm()
			messages.error(request, 'Registration failed!')
			return render_to_response('registration.html',args,context_instance=RequestContext(request))
	else:
		form = ServicesForm()

	args = {}
	args.update(csrf(request))
	args['form'] = ServicesForm()

	
	return render_to_response('registration.html', args)
def get_center_detail(request,center_id):
	
	center_detail = Services.objects.get(id = center_id)

	return render_to_response('center_detail.html',
								{'center_response':center_detail},
								context_instance=RequestContext(request))
def report_abuse(request,center_id):

	if request.method == 'POST':

		form = AbuseForm(request.POST)

		if form.is_valid():

			model_instance = Abuse()
			cd = form.cleaned_data
			model_instance.description = cd['description']
			model_instance.center_id = center_id
			model_instance.save()
			messages.success(request, 'Report received !')

			return render_to_response('abuse.html',{'form':form,'center_id':center_id},context_instance=RequestContext(request))
		else:

			form = AbuseForm()	
			messages.error(request, 'Report failed!')
			return render_to_response('abuse.html',{'form':form,'center_id':center_id},context_instance=RequestContext(request))
	else:

			form = AbuseForm()
			return render_to_response('abuse.html',{'form':form,'center_id':center_id},context_instance=RequestContext(request))

def prevention_tips(request):

	return render_to_response('tips.html',context_instance=RequestContext(request))

def tool_functionality(request):

	return render_to_response('how_it_works.html',context_instance=RequestContext(request))
def contact_us(request):

	return render_to_response('contact.html',context_instance=RequestContext(request))
def about_us(request):

	return render_to_response('about.html',context_instance=RequestContext(request))
