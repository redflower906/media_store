from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template import context
## from nameform 
from .forms import NameForm, item_model_formset_factory, NumInput, Item_Model_Form 
from django.http import HttpResponseRedirect
from django.forms.models import formset_factory, modelformset_factory
from .models import Inventory, Order
import MySQLdb, sys
#from django.http import HttpResponse
'''
NOT WORKING
def current_URL(request, context):
    current = request.path
    print(current)
    current = current.strip("/")
    context.setdefault('current', current)
'''

def index(request):
    context = {}
    #current_URL(request, context)
    return render (request, 'store/home.html', context)

def home(request):
    context = {}
    return render(request, 'store/home.html', context)

def login(request):
    return render (request, 'store/login.html')

def get_items(request):
	result_set = []

#will we only use this for "order" views?
#@login_required(login_url='login')


def services(request):
    context = {}
    return render(request, 'store/services.html')

def add_item(request):
    context = {}
    return render(request, 'store/add_item.html')


def inventory(request):
    """
    # figure out who is logged in.
    user = request.user
    user_profile = UserProfile.objects.get(user=user.id)
    department_id = user_profile.department.id
    department_ids = [dept.id for dept in user_profile.alt_departments.all()]
    department_ids.append(department_id)
"""
    context = {}
    InventoryItems = Inventory.objects.all()
    #sort
    Items = InventoryItems.order_by('inventory_text')
    sort_urls = {'product': '?o=product','container': '?o=container','volume': '?o=volume'}
    sort_arrows = {}
    # render them in a list.
    return render(request, 
        'store/inventory.html', 
        {
        'InventoryItems' : InventoryItems,
        'sorting': sort_urls,
        'sort_arrows': sort_arrows
        }, context)

#@login_required(login_url='login')
def create_item(request):
    ItemModelFormset = item_model_formset_factory(extra=1)
    print(request)
    if request.method == "POST":
        formset = ItemModelFormset(request.POST)
        # create item
        if formset.is_valid():
            formset.save()
            # messages.success(request, 
            # 'Product {0} was successfully created.'.format(InventoryItems.product))
            return HttpResponseRedirect('/inventory/')
    else: formset = ItemModelFormset(queryset=Inventory.objects.none())
    # just show the form
    return render(request, 
    'store/item_form.html', {
    'formset': formset,
    }, context)
    
def update_item(request, id):
    SingleItem = get_object_or_404(Inventory, pk=id)
    Item_form = Item_Model_Form()
    if request.method == "POST":
        Item_form = Item_Model_Form(request.POST, instance=SingleItem)
        # create item
        if Item_form.is_valid():
            Item_form.save()
            messages.success(request, 
            'Product {SingleItem.id} was successfully updated.'.format(SingleItem.product))
            return HttpResponseRedirect('/inventory/'.format(SingleItem.id))
    else:
         Item_form = Item_Model_Form(instance=SingleItem)

    # just show the form
    return render(request, 
    'store/item_form.html', {
    'Item_form': Item_form,
    'SingleItem': SingleItem,
    }, context)

# def update_item(request, id):
#     ItemModelFormset = item_model_formset_factory(extra=0)
#     SingleItem = get_object_or_404(Inventory, pk=id)
#     qset = Inventory.objects.get(pk=id)
#     Item_form = modelformset_factory(Inventory, form = Item_Model_Form)
#     formset = Item_form()

#     #formset = ItemModelFormset(queryset=SingleItem)

#     if request.method == "POST":
#         #formset = ItemModelFormset(request.POST, queryset=SingleItem)
#         formset = Item_form(request.POST, queryset=qset)
#         Item_form = Item_Model_Form(request.POST)
#         # create item
#         if formset.is_valid():
#             formset.save()
#             messages.success(request, 
#             'Product {0} was successfully created.'.format(InventoryItems.product))
#             return HttpResponseRedirect('/inventory/{0}'.format(InventoryItems.id))

#     # just show the form
#     return render(request, 
#     'store/item_form.html', {
#     'Item_form': Item_form,
#     'formset': formset,
#     'SingleItem': SingleItem,
#     }, context)

def get_item(request, id):
    SingleItem = get_object_or_404(Inventory, pk=id)
    return render(request, 
    'store/item_details.html', {
    'SingleItem': SingleItem,
    })

def delete_item(request, id):
    SingleItem = get_object_or_404(Inventory, pk=id)

    #can't delete an item that's associated with an order

    if item.order_set.count() > 0:
        return HttpResponseBadRequest(simplejson.dumps({'failed': 'This item is still associated with existing orders and cant be deleted. Please mark it as inactive instead'}), content_type="application/json")
    item.delete()
    return HttpResponse(simplejson.dumps({'deleted': id}), content_type="application/json")

def single_item(request, id):
    if request.method == "POST":
        return update_item(request, id)
    elif request.method == "DELETE":
        return delete_item(request, id)
    else:
        return get_item(request, id)
        
    # from nameform
def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'store/name.html', {'form': form})
    result_set = []

# class FormCreate(CreateView):
#     model = Inventory
#     template_name = 'store/form.html'
#     fields = ['product','media_type','cost','container','volume','notes']
def order(request):
    context = {}
    OrderTotal = Order.objects.all()
    #sort
    # MC = Inventory(media_choices)
    # print(MC)
    History = OrderTotal.order_by('date_created')
#    sort_urls = {'product': '?o=product','container': '?o=container','volume': '?o=volume'}
 #   sort_arrows = {}
    # render them in a list.
    return render(request, 
        'store/order.html', 
        {
        'OrderTotal' : OrderTotal,
        }, context)

def new_order(request):
    context = {}
    return render(request, 'store/order.html')

def past_order(request):
    context = {}
    return render(request, 'store/order.html')

def edit_past_order(request):
    context = {}
    return render(request, 'store/order.html')

def recurring_order(request):
    context = {}
    return render(request, 'store/order.html')
