from django.shortcuts import render
from django.http import HttpResponse
from .forms import signInForm
from .models import TradeItem, IndividualTrades, TradeItemForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count


def index(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    else:
        # if you are loggedd in 
        # count the number of items you have.
        # number of people that will trade with you.
        # items added today by other people.
        # items added to items that they might want.
        # link to chain explorer.
        # request.user gets the user.. 
        users_items = TradeItem.objects.filter(owner=request.user)
        num_items = users_items.count()
        # num_possible_trades = IndividualTrades.objects.filter(ownerItem=request.user).count() harder query need something else.
        num_possible_trades = TradeItem.objects.annotate(num_trades=Count('askerItem')).filter(owner=request.user).count()  # deleted items are included.
        return render(request, 'tradesavante/home.html', {'num_items': num_items, 'num_possible_trades': num_possible_trades, 'users_items': users_items})


def signIn(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            msg = "You are now logged in!"
            return render(request, 'tradesavante/home.html', {'msg':msg})
        else:
            form = signInForm(request.POST)
            #form = signInForm()
            signin = True
            msg = 'login failed: bad username or password'
            return render(request, 'tradesavante/userInput.html', {'form': form, 'signin': signin, 'msg': msg})
    form = signInForm()
    signin = True
    return render(request, 'tradesavante/userInput.html', {'form': form, 'signin': signin})

def log_out(request):
    logout(request)
    msg = True
    return render(request, 'tradesavante/home.html', {'loggedout': msg})
    

def product(request):
    if not request.user.is_authenticated:
        loggedout = True
        # need feedback message here
        return render(request, 'tradesavante/home.html', {'loggedout': loggedout})
    else:
        return render(request, 'tradesavante/product.html')

def signUp(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pword = request.POST['password']
        # step 1 make sure there's no user with the same password.
        try:
            p = User.objects.get(username=uname)
            # in this case the user is available so create user and re-direct to home_page
            form = signInForm()
            signin = False
            msg = "Username already taken! Please choose a different name."
            return render(request, 'tradesavante/userInput.html', {'form': form, 'signin': signin, 'msg':msg})
        except User.DoesNotExist:
            # in this case the user is available so create user and re-direct to home_page
            User.objects.create_user(uname, pword)
            msg = 'New account created'
            return render(request, 'tradesavante/home.html', {'msg': msg})

    form = signInForm()
    signin = False
    return render(request, 'tradesavante/userInput.html', {'form': form, 'signin': signin})

# still need start_date, been_traded and active (should create default values for these should be able to default the
# date to todays date)

def additem(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    elif request.method == "POST":
        trade_form = TradeItemForm(request.POST, request.FILES)
        if trade_form.is_valid() and 'pkey' in request.POST:
            # then I want to get this item and then return the form with it
            resultid = request.POST['pkey']
            p = TradeItem.objects.get(id=resultid)
            trade_form = TradeItemForm(request.POST, request.FILES, instance=p)
            trade = trade_form.save()
            url = trade.image.url
            return render(request, 'tradesavante/display_item.html',{'url':url, 'trade_form': trade})
        elif trade_form.is_valid():
            #upload_form = UploadFileForm(request.POST)
            trade = trade_form.save(commit=False)
            trade.owner = User.objects.get(id=request.user.id)
            #trade.image.save('firstfile',trade_form.cleaned_data['image'], save=False)
            trade.save()
            url = trade.image.url
   			#trade.save()
			# now what I should do is if you have successfully submitted the image then display it with the option of editing.
			# now you want to display the form information and show the image.
            return render(request, 'tradesavante/display_item.html',{'url':url, 'trade_form': trade})
        else:
            errors = True
            return render(request, 'tradesavante/add_item_Form.html', {'form': trade_form, 'errors': errors, 'error':trade_form['image'].errors})
    trade_form = TradeItemForm()
    return render(request, 'tradesavante/add_item_Form.html', {'form': trade_form, 'errors': False})

def edititems(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    elif request.method == "GET":
        if 'delete' in request.GET:
            resultid = request.GET['delete']
            p = TradeItem.objects.get(id=resultid)
            p.delete()            
        elif 'edit' in request.GET:
            resultid = request.GET['edit']
            p = TradeItem.objects.get(id=resultid)
            p_form = TradeItemForm(instance=p)
            return render(request, 'tradesavante/add_item_Form.html', {'form': p_form, 'errors': False, "pkey":resultid})
    trade_list = TradeItem.objects.filter(owner=request.user)
    return render(request, 'tradesavante/edit_items.html', {'tradeitems': trade_list})

def network(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    elif request.method == "GET": 
        trade_list = TradeItem.objects.all()
        page = request.GET.get('page',1)
        paginator = Paginator(trade_list,10)
        try:
            trade = paginator.page(page)
        except PageNotAnInteger:
            trade = paginator.page(1)
        except EmptyPage:
            trade = paginator.page(paginator.num_pages)
        return render(request, 'tradesavante/network.html', {'trades': trade})
    return HttpResponse("<h2> Not successful! </h2>")

def explore(request):
    return render(request, 'tradesavante/explore.html')

def explore_step1(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    else:
        users_items = TradeItem.objects.filter(owner=request.user)
        return render(request, 'tradesavante/explore_first.html', {'users_items': users_items})

def search(request):
    if not request.user.is_authenticated:
        return HttpResponse("<h2> Not successful! </h2>")
    if request.method == "GET":
        if 'networksearch' in request.GET:
            trade_list = TradeItem.objects.filter(description__contains=request.GET["networksearch"])
            page = request.GET.get('page',1)
            paginator = Paginator(trade_list,10)
            try:
                trade = paginator.page(page)
            except PageNotAnInteger:
                trade = paginator.page(1)
            except EmptyPage:
                trade = paginator.page(paginator.num_pages)
        return render(request, 'tradesavante/network.html', {'trades': trade})
    return HttpResponse("<h2> Not successful! </h2>")

def tradescreen(request):
    if not request.user.is_authenticated:
        return HttpResponse("<h2> Not successful! </h2>")
    if request.method == "GET":
        # add exception for not int get
        pid = request.GET["id"]
        trade_item = TradeItem.objects.get(id=pid)
        trade_list = TradeItem.objects.filter(owner=request.user)
        # what you need 
        page = request.GET.get('page',1)
        paginator = Paginator(trade_list,2)
        try:
            trade = paginator.page(page)
        except PageNotAnInteger:
            trade = paginator.page(1)
        except EmptyPage:
             trade = paginator.page(paginator.num_pages)
        #return render(request, 'tradesavante/viewnetwork.html', {'trades': trade, 'trade_item': trade_item})
        return render(request, 'tradesavante/tradescreen.html', {'tradeitem': trade_item, 'trades': trade})
    elif request.method == "POST":
        myid = request.POST["myitem"]
        desiredid = request.POST["desireditem"]
        myitem = TradeItem.objects.get(id=myid)
        desireditem = TradeItem.objects.get(id=desiredid)
        p = IndividualTrades(askerItem=myitem,ownerItem=desireditem)
        p.save()
		# be nice to pass a message here that says successfully sent.
        return render(request, 'tradesavante/home.html')
    return HttpResponse("<h2> Trade Not Submitted! </h2>")

def seenetwork(request):
    if not request.user.is_authenticated:
        return HttpResponse("<h2> Not successful! </h2>")
    if request.method == "GET":
        # add exception for not int get -- want to see all of the 
        pid = request.GET["id"]
        trade_item = TradeItem.objects.get(id=pid) # this is the item that going to explore
        trades_list = IndividualTrades.objects.filter(askerItem=trade_item)
        # what you need 
        page = request.GET.get('page',1)
        paginator = Paginator(trades_list,2)
        try:
            trade = paginator.page(page)
        except PageNotAnInteger:
            trade = paginator.page(1)
        except EmptyPage:
             trade = paginator.page(paginator.num_pages)
        return render(request, 'tradesavante/viewnetwork.html', {'trades': trade, 'trade_item': trade_item})
    return HttpResponse("<h2> Not successful! </h2>")

