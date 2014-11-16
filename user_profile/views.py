from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.template import RequestContext
from user_profile.models import UserProfile
from user_profile.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



def profile(request, username):
	this_user = get_object_or_404(User, username=username)
	this_profile = get_object_or_404(UserProfile, user=this_user)
	args = {}
	args['this_user'] = this_user
	args['this_profile'] = this_profile 

	return render(request, 'user_profile/profile.html', args)

@login_required
def update_profile(request, username):
	if request.user.username == username:
		if request.method == 'POST':
			profile_instance = UserProfile.objects.get(user=request.user)
			form = UserProfileForm(request.POST, request.FILES, instance=profile_instance)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/user-account/profile/%s' %(request.user.username))

		else:
			profile_instance = UserProfile.objects.get(user=request.user)
			form = UserProfileForm(instance=profile_instance)

		args = {}
		args.update(csrf(request))

		args['form'] = form
		args['this_user'] = User.objects.get(username=request.user.username)
		args['this_profile'] = UserProfile.objects.get(user=request.user)
		return render(request, 'user_profile/update_profile.html', args)
	else:
		return HttpResponse(content="Forbidden", status=403)


@login_required
def profile_settings(request, username):
	this_user = get_object_or_404(User, username=username)
	this_profile = get_object_or_404(UserProfile, user=this_user)
	if request.user == this_user:        
		args = {}
		args['this_user'] = this_user
		args['this_profile'] = this_profile	

		return render(request, 'user_profile/profile_settings.html', args)
	else:
		return HttpResponse(content="Forbidden", status=403)


@login_required
def delete_user(request, username):
	if request.user.username == username:
		user = User.objects.get(username = username)
		args={}
		args['this_user'] = user

		if request.method == 'POST':
			typed_password = request.POST['password']  
			if user.check_password(typed_password):
				user.delete()
				return render('user_profile/deleted_account.html', args)
			else:
				return HttpResponse("Wrong password. User profile can't be deleted. Please try again.", status=400)
	
	else: 
		return HttpResponse(content="Forbidden", status=403)

