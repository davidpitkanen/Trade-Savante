from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from .forms import signInForm
from .models import TradeItem, IndividualTrades, TradeItemForm, TradeSequence, MessageForm, Message, sequenceManager, SearchForm, KeyWordForm, SearchKeywords
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, Max
import queue as queue
import random
from django.db import connection
from numbers import Number

def redirectLogin(request, msgs=None):
    form = signInForm()
    signin = True
    return render(request, 'tradesavante/userInput.html', {'form': form, 'signin': signin})
    

def sendmessage(request):
    if not request.user.is_authenticated:
        msg = True
        return redirectLogin(request)
        #return render(request, 'tradesavante/home.html', {'loggedout': msg})
    elif request.method == "POST":
        msg_form = MessageForm(request.POST)
        if msg_form.is_valid():
            #upload_form = UploadFileForm(request.POST)
            msgs = msg_form.save(commit=False)
            msgs.sender = request.user #User.objects.get(id=request.user.id)
            #trade.image.save('firstfile',trade_form.cleaned_data['image'], save=False)
            msgs.reciever = User.objects.get(id=2)
            msgs.save()
            return render(request, 'tradesavante/display_item.html',{'trade_form': msgs})
        else:
            errors = True
            return render(request, 'tradesavante/add_item_Form.html', {'form': trade_form, 'errors': errors, 'error':trade_form['image'].errors})
    user_send = request.user
    user_recieve = User.objects.get(id=2)
    message_form = MessageForm()
    return render(request, 'tradesavante/sendmessage_form.html', {'mform': message_form, 'user_recieve': user_recieve})


def runbfsCode(request):
    my_items= TradeItem.objects.filter(owner=request.user)
    # here is where bfs code starts
    dict_nodes = TradeItem.objects.all().aggregate(Max('id'))
    num_nodes = dict_nodes['id__max']
    print("The biggest id is %d" % (num_nodes))
    marked = [False] * (num_nodes + 1)
    edgeTo = [0] * (num_nodes + 1)
    #self.s = s
    #self.bfsearch(s)
    for t in my_items:
        print("This is the id %d" % (t.id))
        if not marked[t.id]:
            marked, edgeTo = bfsearch(t.id, marked, edgeTo)
    return marked, edgeTo

def index(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    else:
        # get items people will trade with you that are not yours.
        # can do this with the bfs search.
        # find the number of items that are true.
        marked, edgeTo = runbfsCode(request)
        # set your values to false
        your_items = TradeItem.objects.filter(owner=request.user)
        num_items = TradeItem.objects.filter(owner=request.user).count()
        if num_items > 0:
            one_of_your_items = your_items[0]
        else:
            one_of_your_items = None
        # next step is trades
        your_trades = IndividualTrades.objects.filter(askerItem__in=your_items)
        num_wanted_items = your_trades.count()
        if num_wanted_items > 0:
            one_of_your_trades = your_trades[0]
        else:
            one_of_your_trades = None
        # next step is explorations
        your_explorations = TradeSequence.objects.filter(tradeConnection__in=your_trades)
        num_explorations = TradeSequence.objects.filter(linkNumber=0).count()
        #yourList = yourItems.values_list('id', flat=True)
        #yourSize = yourList.count()
        # this is repeated code
        #for x in yourList:
        #    marked[x] = False
        # get the coefficients where True
        #true_values = [x for x in range(len(marked)) if marked[x]]
        # next pick 5 at random (if there is 5)
        #picks = min(len(true_values), 5)
        #true_values = random.sample(true_values,picks)
        # get the items that match
        #trades_to_display = TradeItem.objects.filter(id__in=true_values)
        # show these items on the view.
        # to do 1. number of tradesequences, names, first item name, # of items,
        # is it closed?
        sequences = TradeSequence.objects.filter(sequencer=request.user)
        # define a dictionary
        sequence_dict = {"name": [], "item_name": [], "num_items": [], "id_val":[]}
        # 
        #sequence_dict['name'] = sequences.filter(linkNumber=0).values_list('name', flat=True)
        #p = TradeSequence.objects.raw('SELECT '
        #sequence_dict['item_name']
        #users_items = TradeItem.objects.filter(owner=request.user)
        #num_items = users_items.count()
        #sequence_zip = TradeSequence.objects.with_counts()
        num_possible_trades = TradeItem.objects.annotate(num_trades=Count('askerItem')).filter(owner=request.user).count()  # deleted items are included.
        return render(request, 'tradesavante/home.html', {'num_explorations':num_explorations, 'num_items': num_items, 'num_wanted_items': num_wanted_items, 'users_item': one_of_your_items, 'one_of_your_trades': one_of_your_trades})


					  
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
        return render(request, 'tradesavante/home.html', {'loggedout': loggedout})
    else:
        return render(request, 'tradesavante/product.html')

def signUp(request):
    if request.method == 'POST':
        uname = request.POST['username']
        pword = request.POST['password']
        try:
            p = User.objects.get(username=uname)
            form = signInForm()
            signin = False
            msg = "Username already taken! Please choose a different name."
            return render(request, 'tradesavante/userInput.html', {'form': form, 'signin': signin, 'msg':msg})
        except User.DoesNotExist:
            User.objects.create_user(uname, pword)
            msg = 'New account created'
            return render(request, 'tradesavante/home.html', {'msg': msg})
    form = signInForm()
    signin = False
    return render(request, 'tradesavante/userInput.html', {'form': form, 'signin': signin})

def addkeywords(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    elif request.method == "POST":
        key_form = KeyWordForm(request.POST)
        if key_form.is_valid() and 'itemid' in request.POST:
            # then I want to get this item and then return the form with it
            key_words = request.POST['key_word']
            # just split the words at the commas and for each word enter it into the database.
            key_list = [x.strip() for x in key_words.split(',')]
            item_id = request.POST['itemid']
            try:
                item_key = TradeItem.objects.get(id=item_id)
                for x in key_list:
                    k = SearchKeywords(key_word=x, itemsearch=TradeItem.objects.get(id=item_id))
                    k.save()
                name = item_key.name
                msg = 'The keywords for %s have been entered:' % (name)
                return render(request,'tradesavante/home.html', {'msg':msg, 'key_list': key_list})
            except TradeItem.DoesNotExist:
                # you want to send home with a failure message.. not sure what to say keywords not added
                msg = 'Item keywords failed.  Keywords not added.'
                return render(request,'tradesavante/home.html', {'msg':msg})
            
            
    return render(request, 'tradesavante/home.html')
 


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
            # here have to get the 
            #key_words = trade.key_words
            # just split the words at the commas and for each word enter it into the database.
            #key_list = [x.strip() for x in key_words.split(',')]
            #for x in key_list:
            trade.save()
            return explore(request)
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



def askforitems(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    elif request.method == "GET": 
        #trade_list = TradeItem.objects.all()
        #my_items= TradeItem.objects.filter(owner=request.user)
        # here is where bfs code starts
        #dict_nodes = TradeItem.objects.all().aggregate(Max('id'))
        #num_nodes = dict_nodes['id__max']
        #print("The biggest id is %d" % (num_nodes))
        #marked = [False] * (num_nodes + 1)
        #edgeTo = [0] * (num_nodes + 1)
        #self.s = s
        #self.bfsearch(s)
        #for t in my_items:
        #    print("This is the id %d" % (t.id))
        #    if not marked[t.id]:
        #        marked, edgeTo = bfsearch(t.id, marked, edgeTo)
        # step 1 is to generate a page system of items that you want.
        #wanted_items = IndividualTrades.objects.filter(asker=request.user)
        # now generate a page system for this.
        #page = request.GET.get('page',1)
        #paginator = Paginator(wanted_item,3)
        #try:
        #    wanted_page = paginator.page(page)
        #except PageNotAnInteger:
        #    wanted_page = paginator.page(1)
        #except EmptyPage:
        #    wanted_page = paginator.page(paginator.num_pages)
        #zippers = zip(trade,marked)
        search_f = SearchForm()
        return render(request, 'tradesavante/askforitems.html', {'search_form':search_f})
    return HttpResponse("<h2> Not successful! </h2>")


def bfsearch(s, marked, edgeTo):
    q = queue.Queue()
    marked[s] = True
    q.put(s)
    while not q.empty():
        print('another round')
        v = q.get()
        try:
            t_item = TradeItem.objects.get(id=v)
            t = IndividualTrades.objects.filter(askerItem=t_item)
            for node_item in t:
                w = node_item.id
                print(w)
                if not marked[w]:
                    edgeTo[w] = v
                    marked[w] = True
                    q.put(w)
        except TradeItem.DoesNotExist:
             print("does not exist %d",(v))
    return marked, edgeTo

def hasPathTo(self, v):
    return self.marked[v]


def explore(request):
    # for one should show your items and then explore them instead of a create button
    # two need to show your current explorations
    #user_id = request.user.id
    #wanted_items = TradeItem.objects.raw("""SELECT t.id as id FROM trade_savante_IndividualTrades as p 
	#INNER JOIN trade_savante_TradeItem as t ON p.askerItem = t.id """)
    #p = TradeSequence.objects.filter(sequencer=request.user, linkNumber=0)
    #wanted_items = IndividualTrades.objects.filter(askerItem.owner=request.user)
    u = TradeItem.objects.filter(owner=request.user)
    wanted_items = IndividualTrades.objects.filter(askerItem__in=u)
    # want this to be a paginator.
    print(wanted_items)
    sequence_zip = TradeSequence.objects.with_counts()  # then this returns a table 
    return render(request, 'tradesavante/explore.html', {'wanted_items': wanted_items, 'sequence_info':sequence_zip})


def explore_first(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    elif request.method == 'POST':
        trade_id = request.POST['trade_id']
        try:
            trade_item = IndividualTrades.objects.get(id=trade_id)
            # now create the sequences
            seqid = TradeSequence.objects.all().aggregate(Max('sequenceid'))['sequenceid__max']
            if isinstance(seqid, Number):
                seqid =seqid + 1
            else:
                seqid = 1
            p = TradeSequence(linkNumber=0, tradeConnection=trade_item, sequencer = request.user, sequenceid=seqid)
            p.save()
            q = IndividualTrades.objects.filter(askerItem=trade_item.ownerItem)
            currentItem = trade_item.ownerItem
            return render(request, 'tradesavante/explore_repeat.html', {'trades': q, 'seqid': seqid, 'currentItem': currentItem})
        except IndividualTrades.DoesNotExist:
            ohwell = 1 # need to return an error page maybe reload the original page say error
    return explore(request)

def explore_repeat(request):
    if not request.user.is_authenticated:
        msg = True
        return render(request, 'tradesavante/home.html', {'loggedout': msg})
    elif request.method == 'POST':
        # need the itemid, need the sequence id
        itemid = request.POST['picture']
        try:
            item = TradeItem.objects.get(id=itemid)
            chainId = request.POST['seqkey']
            chain_item = TradeSequence.objects.filter(sequenceid=chainId)[1]
            chain_name = chain_item.name
            linkNum = TradeSequence.objects.filter(sequenceid=chainId).aggregate(Max('linkNumber'))['linkNumber__max'] + 1
            # get the sequence name
            p = TradeSequence(name=chain_name, linkNumber=linkNum, tradeConnection=item, sequencer = request.user)
            p.save()
            q = IndividualTrades.objects.filter(askerItem=item)
            return render(request, 'tradesavante/explore_repeat.html', {'trades': q, 'seqid': chainId, 'currentItem': item})
        except TradeItem.DoesNotExist:
            ohwell = 1
    return render(request, 'tradesavante/home.html')


def mark_as_wanted(request):
    if not request.user.is_authenticated:
        return HttpResponse("<h2> Not successful! </h2>")
    if request.method == "GET":
        item_id = request.GET['item_id']
        # now get all this users items
        item = TradeItem.objects.get(id=item_id)
        users_items = TradeItem.objects.filter(owner=request.user)
        page = request.GET.get('page',1)
        paginator = Paginator(users_items,10)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages) 
        return render(request, 'tradesavante/create_trade.html', {'tradeitem': item, 'trades': items}) # {'users_page_items': items})
    return HttpResponse("<h2> Not successful! </h2>")



def search(request):
    if not request.user.is_authenticated:
        return HttpResponse("<h2> Not successful! </h2>")
    if request.method == "GET":
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            items = TradeItem.objects.filter(description__contains=request.GET["search"])
            if isinstance(request.GET['max_price'], Number):
                items = items.filter(price__lte=request.GET['max_price'])
            if isinstance(request.GET['min_price'], Number):
                items = q1.filter(price__gte=request.GET['min_price'])
            if request.GET['category'] == 'na':
                trade_list = items
            else:
                trade_list = items.filter(category=request.GET['category'])
            print(request.GET['category'])
            page = request.GET.get('page',1)
            paginator = Paginator(trade_list,10)
            try:
                trade = paginator.page(page)
            except PageNotAnInteger:
                trade = paginator.page(1)
            except EmptyPage:
                trade = paginator.page(paginator.num_pages)
            search_form = SearchForm()
            return render(request, 'tradesavante/search_results.html', {'trades': trade, 'search_form':search_form})
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

