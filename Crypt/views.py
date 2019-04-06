from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, logout
from .models import Profile
from django.conf import settings
from .blockchain import Block
from .blockchain import Blockchain
from django.http import HttpResponse
from django.core.mail import send_mail
import json

BlockChain = Blockchain()
api_list = []

def index(request):
	return render(request,"Crypt/index.html",{})

def logIn(request):
	if request.method=='POST':
		name= request.POST['name']
		password=request.POST['password']
		user = authenticate(username= name, password= password)
		request.session['sessionId'] = user.id;
		return redirect('home')
	return render(request,"Crypt/login.html")

def signUp(request):
	if request.method == "POST":
		name = request.POST['name']
		email = request.POST['email']
		password = request.POST['password']
		user = User.objects.create_user(name, email, password)
		profile = Profile.objects.create(user=user)
		s=name+' gets 100 coins'
		BlockChain.mine(Block(s))
		updateAPI()
		return logIn(request)

	return render(request,"Crypt/signup.html",{})

def home(request):
	user = get_user(request)
	profile = Profile.objects.get(user= user)
	return render(request,"Crypt/user.html",{'user':user, 'profile':profile})


def sendCoin(request):
	user = get_user(request);
	if request.method == "POST":
		email = request.POST['email']
		reciever = User.objects.get(email=email)
		amount = float(request.POST['amount'])
		password = request.POST['password']
		u = authenticate(username=user.username, password=password)
		profile=Profile.objects.get(user=u)
		if u and profile.balance >= amount :
			s = ' '.join([user.username,'-->',reciever.username,' amount :',str(amount)]);
			BlockChain.mine(Block(s))
			receiver_profile=Profile.objects.get(user=reciever)
			receiver_profile.balance+=amount
			receiver_profile.save()
			profile.balance-=amount
			profile.save()
			send_mail(
				'this mail is from bytecoin', 
				str(amount)+' coins added to your account from '+user.username,
				settings.EMAIL_HOST_USER,
				[reciever.email],
				fail_silently=False,

				)
			send_mail(
				'this mail is from bytecoin', 
				'hii '+user.username +str(amount)+' coins transfered from your account to'+reciever.username,
				settings.EMAIL_HOST_USER,
				[u.email],
				fail_silently=False,

				)


		else:
			return HttpResponse('you do not have sufficient balance')

		updateAPI()
	return redirect('home')

def api_view(request):
	context = {
	"chain":api_list,
	}
	return render(request,'Crypt/test.html',context)

def get_user(request):				## A function which get user_id from the session key (if not present it return false)
	if 'sessionId' in request.session:
		return User.objects.get(id = request.session['sessionId']);
	return False;

def updateAPI():
	temp = BlockChain.head
	blockchain = BlockChain
	api_list.clear()
	while blockchain.head != None:
		x = str(blockchain.head)
		x = json.dumps(x)
		api_list.append(x)
		blockchain.head = blockchain.head.next
	BlockChain.head = temp
	print(api_list)


def logout(request):			
    try:
        request.session.flush();
    except KeyError:
        return HttpResponse('Error Occur While Logging You Out, Please Try Again')
    return redirect('index')