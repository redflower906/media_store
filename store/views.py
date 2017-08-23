from django.shortcuts import render, get_object_or_404
from django.template import context
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.forms.models import formset_factory, modelformset_factory
from .forms import Item_Model_Form, item_model_formset_factory, AnnouncementsForm
from .models import Inventory, Order, Announcements
import MySQLdb, sys


def index(request):
    context = {}
    return render (request, 'store/home.html', context)

def home(request):
    post = get_object_or_404(Announcements)
    #if staff member
    if request.method == "POST":
        AForm = AnnouncementsForm(request.POST, instance=post)
        if AForm.is_valid():
            AForm.save()
            messages.success(request, 
            'Annoucements have been updated')
            return HttpResponseRedirect('/store/')
    else:
        AForm = AnnouncementsForm(instance=post)
    #return render(request, 'store/home.html', {'AForm': AForm})
    return render(request, 'store/home.html', {'post': post} )
 
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/store/')
    else:
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
    # ordering = request.GET.get('o')
    # Items = InventoryItems.order_by('inventory_text')
    # if ordering:
    #     sort_by = ordering.split('.')

    #     if sort_by:
    #         Items = InventoryItems.order_by(*sort_by)

    #     sort_urls = {}
    #     sort_arrows = {}
    #     columns = ('inventory_text', 'product', 'container', 'volume', 'active' )
    #     for column in columns:
    #         sort_columns = ordering.split('.')
    #         url = '?o='
    #         try:
    #             position = sort_columns.index(column)
    #             sort_columns.pop(position)
    #             url += '-' + column
    #             sort_arrows[column] = 'down'
    #             if len(sort_columns):
    #                 url += '.' + '.'.join(sort_columns)
    #         sort_urls[column] = url
    # else:
    #     services = services.order_by('inventory_text')
    #     sort_urls = {'inventory_text': '?o=inventory_text', 'product': '?o=product', 'container': '?o=container', 'volume': '?o=volume', 'active': '?o=active'}
    #     sort_arrows = {}

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
    inventory = Inventory()

    if request.method == "POST":
        formset = ItemModelFormset(request.POST)
        # create item
        if formset.is_valid():
            formset.save()
            messages.success(request, 
            'Product was successfully created.')
            return HttpResponseRedirect('/inventory/')
    else: formset = ItemModelFormset(queryset=Inventory.objects.none())
    # just show the form
    return render(request, 
    'store/item_form.html', {
    'formset': formset,
    'inventory': inventory,
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
            '{0} was successfully updated.'.format(SingleItem.inventory_text))
            return HttpResponseRedirect('/inventory/')
    else:
         Item_form = Item_Model_Form(instance=SingleItem)
    # just show the form
    return render(request, 
    'store/item_form.html', {
    'Item_form': Item_form,
    'SingleItem': SingleItem,
    }, context)

def get_item(request, id):
    SingleItem = get_object_or_404(Inventory, pk=id)
    return render(request, 
    'store/item_details.html', {
    'SingleItem': SingleItem,
    })

# def delete_item(request, id):
#     SingleItem = get_object_or_404(Inventory, pk=id)

#     #can't delete an item that's associated with an order

#     if item.order_set.count() > 0:
#         return HttpResponseBadRequest(simplejson.dumps({'failed': 'This item is still associated with existing orders and cant be deleted. Please mark it as inactive instead'}), content_type="application/json")
#     item.delete()
#     return HttpResponse(simplejson.dumps({'deleted': id}), content_type="application/json")

def single_item(request, id):
    if request.method == "POST":
        return update_item(request, id)
    elif request.method == "DELETE":
        return delete_item(request, id)
    else:
        return get_item(request, id)
        
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
        'store/order_list.html', 
        {
        'OrderTotal' : OrderTotal,
        }, context)

def new_order(request):
    context = {}
    return render(request, 'store/order_create.html')

def past_order(request):
    context = {}
    return render(request, 'store/order_list.html')

def edit_past_order(request):
    context = {}
    return render(request, 'store/order_edit.html')

def recurring_order(request):
    context = {}
    return render(request, 'store/order_list.html')
