from django import forms
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory, ModelForm
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.views import generic
from django.template import context, RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from dateutil import relativedelta
from datetime import datetime, date
from .forms import *
from .models import *
from .resources import *
import MySQLdb, sys
import json as simplejson
import csv
import time



def index(request):
    context = {}
    return render (request, 'store/home.html', context)

def home(request):
    post = get_object_or_404(Announcements)
    user = request.user
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
    return render(request, 'store/home.html', {
        'post': post,
        'AForm': AForm,
        'user': user,
        } 
    )
 
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

INVENTORY_LIST_HEADERS = (
    ('Name', 'inventory_text'),
    ('Product', 'product'),
    ('Container', 'container'),
    ('Volume', 'volume'),
    ('Active', 'active'),
)

def inventory(request):
    """
    # figure out who is logged in.
    user = request.user
    user_profile = UserProfile.objects.get(user=user.id)
    department_id = user_profile.department.id
    department_ids = [dept.id for dept in user_profile.alt_departments.all()]
    department_ids.append(department_id)
"""
    InventoryItemsAll = Inventory.objects.all()
    sort_headers = SortHeaders(request, INVENTORY_LIST_HEADERS)
    InventoryItems = Inventory.objects.order_by(sort_headers.get_order_by())
    user = request.user
    return render(request, 
        'store/inventory.html', 
        {
        'InventoryItems' : InventoryItems,
        'headers': list(sort_headers.headers()),
        'InventoryItemsAll': InventoryItemsAll,
        },)

@login_required(login_url='login')
def create_item(request):
    user = request.user
    ItemModelFormset = item_model_formset_factory(extra=1)
    inventory = Inventory()

    if request.method == "POST":
        formset = ItemModelFormset(request.POST)
        # create item
        if formset.is_valid():
            newItem = formset.save()
            messages.success(request, 
            'Product was successfully created.')
            print(newItem[0].pk)
            # put this in order create!
            send_mail(
                'New ',
                'Congrats, you created an item that is called {0}!'.format(newItem[0].inventory_text),
                'harrisons1@janelia.hhmi.com',
                ['coffmansr906@gmail.com'],
                fail_silently=False,
            )
            return HttpResponseRedirect('/inventory/')
    else: formset = ItemModelFormset(queryset=Inventory.objects.none())
    # just show the form
    return render(request, 
    'store/item_form.html', {
    'formset': formset,
    'inventory': inventory,
    'user': user,
    }, context)

@login_required(login_url='login')
def update_item(request, id):
    user = request.user
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

def single_item(request, id):
    if request.method == "POST":
        return update_item(request, id)
    elif request.method == "DELETE":
        return delete_item(request, id)
    else:
        return get_item(request, id)

'''def create_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    OrderLineInlineFormset = inlineformset_factory(Order, OrderLine, )
    InventoryInlineFormset = inlineformset_factory(Order)'''


def __build_inventory_groups():
   # build inventory lists grouped by mediatype. This data is used
    # on the front-end to build mediatype and inventory dropdowns
    inventory_lists = {}
    for type_val, display in MEDIA_CHOICES:
        inventory_choices = [{
            'id': inv.id,
            'desc': inv.inventory_text,
            'container': inv.container,
            'notes': inv.notes,
            'cost': str(inv.cost)
        } for inv
            in Inventory.objects.filter(media_type=type_val)]
        inventory_lists[type_val] = inventory_choices
    return simplejson.dumps(inventory_lists)

@login_required(login_url='login')
def create_order(request, copy_id=None):

    order = Order()
    initial_emptyorderline = {'inventory': None, 'id': None, 'DELETE': False, 'order': order}

    if request.method == "POST":
        
        order_form = OrderForm(request.POST, prefix='order', instance=order)
        orderlineformset = OrderLineInlineFormSet(
            request.POST, prefix='orderlines', instance=order)

        if order_form.is_valid() and orderlineformset.is_valid():
            # TODO for Scarlett and Amanda: decide desired behavior for date_submitted.
            #   Some options: 
            #       only set on create (but this is the same as date_created...)--handle in model
            #       update on edit or create only set on create--handle in model

            # TODO 2 for Scarlett and Amanda: descide if you want to copy Inventory.notes and save to Orderline.description
            # or just access orderline->inventory->notes to display in templates
            order = order_form.save()
            orderlineformset.save()
            messages.success(request,
                'Order {0} was successfully created.'.format(order_form.instance.id))
            return HttpResponseRedirect('/order/view')
        else:
            messages.error(request, 'There was a problem saving your order. Please review the errors below.')
    else:

        if copy_id:
            # TODO: implement
            pass
            # order_form, orderlineformset, = copy_order_form(
            #     copy_id, request, alternative, initial)
        else:
            order_form = OrderForm(prefix='order')
            orderlineformset = OrderLineInlineFormSet(
                prefix='orderlines')

    return render(request, 'store/order_create.html', {
        'copy_id' : copy_id,
        'order_form' : order_form,
        'formset': orderlineformset,
        'inventory_lists': __build_inventory_groups(),
        'media_types': MEDIA_CHOICES
    })

def past_order(request):
    context = {}
    return render(request, 'store/order_past.html')

def edit_past_order(request):
    context = {}
    return render(request, 'store/order_edit.html')

def recurring_order(request):
    context = {}
    return render(request, 'store/order_list.html')


@login_required
def view_order(request):
    ORDER_LIST_HEADERS_INCOMP = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Requester', 'requester'),
        ('Date Submitted', 'date_submitted'),
        ('Location', 'location'),
        ('Status', 'status'),
    )

    ORDER_LIST_HEADERS_RECUR = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Requester', 'requester'),
        ('Date Submitted', 'date_submitted'),
        ('Start Date', 'date_recurring_start'),
        ('End Date', 'date_recurring_stop'),
        ('Location', 'location'),
        ('Status', 'status'),
    )

    ORDER_LIST_HEADERS_CNB = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Requester', 'requester'),
        ('Date Submitted', 'date_submitted'),
        ('Date Complete', 'date_complete'),
        ('Location', 'location'),
        ('Status', 'status'),
    )        

    ORDER_LIST_HEADERS_CB = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Requester', 'requester'),
        ('Date Submitted', 'date_submitted'),
        ('Date Billed', 'date_billed'),
        ('Location', 'location'),
        ('Status', 'status'),
    )    
    sort_headers1 = SortHeaders(request, ORDER_LIST_HEADERS_INCOMP)
    sort_headers2 = SortHeaders(request, ORDER_LIST_HEADERS_RECUR)
    sort_headers3 = SortHeaders(request, ORDER_LIST_HEADERS_CNB)
    sort_headers4 = SortHeaders(request, ORDER_LIST_HEADERS_CB)
    
    # how to associate "orders" in html (either incomp, CNB, CB) to also associate with paginator
    # page = request.GET.get('page', 1)
    # paginator = Paginator(orders, 2)
    # try:
    #     pages = paginator.page(page)
    # except PageNotAnInteger:
    #     pages = paginator.page(1)
    # except EmptyPage:
    #     pages = paginator.page(paginator.num_pages)


    if request.method == 'POST':
        # for each order category, check to see if the form had been updated and save
        order_formset = OrderStatusFormSet(request.POST, prefix='incomp')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

        order_formset = OrderStatusFormSet(
            request.POST, prefix='recur')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

        order_formset = OrderStatusFormSet(
            request.POST, prefix='compNotBill')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

        order_formset = OrderStatusFormSet(
            request.POST, prefix='compBill')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

    user = request.user

    if user.userprofile.is_privileged is False:
        orders = Order.objects.preferred_order().filter(submitter=request.user)
    else:
        orders = Order.objects.preferred_order().all()

    today = date.today()
    nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date()
    lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-1)

    if today >= nextbill:
        nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=1)
        lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date()

    print(today)
    print(nextbill)
    print(lastbill)
    print((nextbill - today).days)
    item = Order.objects.values('date_billed').get(pk=1)
    # print(item.clean())
    # if item < lastbill:
    #     print('hi!')
    # print(type(item))
    incomp_queryset = orders.filter(is_recurring=False).exclude(status__icontains='Complete').exclude(status__icontains='Billed').exclude(status__icontains='Auto').exclude(date_billed__isnull=False).prefetch_related('orderline_set').exclude(orderline__inventory__id='686')    
    recur_queryset = orders.filter(is_recurring=True).exclude(date_billed__isnull=False).prefetch_related('orderline_set').exclude(orderline__inventory__id='686') 
    compNotBill_queryset = orders.filter(status__icontains='Complete').exclude(date_billed__isnull=False).order_by('date_complete').prefetch_related('orderline_set').exclude(orderline__inventory__id='686') 
    compBill_queryset = orders.filter(status__icontains='Billed').filter(date_billed=lastbill).order_by('date_billed').prefetch_related('orderline_set').exclude(orderline__inventory__id='686') 

    incomp = OrderStatusFormSet(queryset=incomp_queryset, prefix='incomp')
    recur = OrderStatusFormSet(queryset=recur_queryset, prefix='recur')
    compNotBill = OrderStatusFormSet(queryset=compNotBill_queryset, prefix='compNotBill')
    compBill = OrderStatusFormSet(queryset=compBill_queryset, prefix='compBill')

    return render(request,
        'store/order_view2.html',{
        'compNotBill': compNotBill,
        'incomp': incomp,
        'headers1': list(sort_headers1.headers()),
        'headers2': list(sort_headers2.headers()),
        'headers3': list(sort_headers3.headers()),
        'headers4': list(sort_headers4.headers()),
        'compBill': compBill,
        'recur': recur,
        'user':user,
        # 'pages': pages,
        })

def export_orders(request):
    orders = Order.objects.all()    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    p = UserFullName.objects.all()
    print(p)
    writer = csv.writer(response)
    writer.writerow(['order num', 'requester', 'date_wth_dep', 'product', 'qty', 'price', 'email'])

    compNotBill = orders.filter(status__icontains='Complete').exclude(date_billed__isnull=False).prefetch_related('orderline_set').values_list('id','requester__userprofile__employee_id', 'date_submitted', 'orderline__inventory__inventory_text', 'orderline__qty', 'orderline__inventory__cost', 'requester__email')
    
    for record in compNotBill:
        writer.writerow(record)
    return response

@login_required
def current_sign_outs (request):
    ORDER_LIST_HEADERS_CORN = (
        ('Order ID', 'order'),
        ('Department to Bill', 'department_name'),
        ('Date Submitted', 'date_submitted'),
        ('Location', 'location'),
    )

    ORDER_LIST_HEADERS_CORN_B = (
        ('Order ID', 'order'),
        ('Department to Bill', 'department_name'),
        ('Date Submitted', 'date_submitted'),
        ('Date Billed', 'date_billed'),
        ('Location', 'location'),
    )

    sort_headers1 = SortHeaders(request, ORDER_LIST_HEADERS_CORN)
    sort_headers2 = SortHeaders(request, ORDER_LIST_HEADERS_CORN_B)
    orders = OrderLine.objects.all()
    cornmeal = orders.filter(Q(inventory__id=686)| Q(inventory__id=668)).filter(order__date_billed__isnull=False)
    corn_b = orders.filter(Q(inventory__id=686)| Q(inventory__id=668)).filter(order__date_billed__isnull=True)

    today = date.today()
    nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date()
    lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-1)

    return
