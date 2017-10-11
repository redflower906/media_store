from django.shortcuts import render, get_object_or_404, HttpResponse
from django.db.models import Q
from django.views import generic
from django.template import context, RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory, ModelForm
from .forms import Item_Model_Form, item_model_formset_factory, AnnouncementsForm, OrderForm, order_inline_formset_factory, OrderLineForm
from .models import Inventory, Order, Announcements, OrderLine, SortHeaders, Department, Vendor
import MySQLdb, sys
import csv
import time



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
    return render(request, 
        'store/inventory.html', 
        {
        'InventoryItems' : InventoryItems,
        'headers': list(sort_headers.headers()),
        'InventoryItemsAll': InventoryItemsAll,
        },)

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
        
def check_total_is_not_zero(formset, request, message):
    total=0
    for form in formset:
        if form.is_valid():
            qty = form.cleaned_data.get('qty')
            cost = form.cleaned_data.get('cost')
            if qty and cost:
                total += qty * cost
    if total == 0:
        messages.error(request, message)
        return flag

    return True

def have_minimum(formset, count, request, message):
    line_count = 0
    for form in formset:
        if form.is_valid():
            deleted = form.cleaned_data.get('DELETE')
            if deleted == False:
                line_count = 1
    if line_count < 1:
        messages.error(request, message)
        return False

    return True

def order(request):
    OrdersAll=Order.objects.all()
    return render(request, 
        'store/order_list.html',{
        'OrdersAll': OrdersAll,
        }, context)


'''def create_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    OrderLineInlineFormset = inlineformset_factory(Order, OrderLine, )
    InventoryInlineFormset = inlineformset_factory(Order)'''


def create_order(request, copy_id=None):
    OrderInlineFormset = order_inline_formset_factory
    order_line = OrderLine()
    inventory = Inventory()
    total_message = 'The total billed is $0. Please review.'


    initial ={
#        'submitter': user.id,
        'date_complete': time.strftime('%Y-%m-%d'),
#        'department': department.id,
#        'logged-in': user_profile,
    }
    if request.method == "POST":
            order = Order()
            formset = OrderInlineFormset(request.POST)
            order_form = OrderForm(request.POST, extra=1)
            orderline_form = OrderLineForm(request.POST, extra=1)
            if all([have_minimum(orderline_form, 1, request), order_form.is_valid(), orderline_form.is_valid(), check_total_is_not_zero(orderline_form,request, total_message)  ]):
                order_form.save()
                orderline_form.save()
                message.success(request,
                    'Order {0} was successfully created.'.format(order_form.instance.id))
                if request.POST.get('order_submit') == 'Save':
                    return HttpResponseRedirect('/')
                else :
                    return HttpResponseRedirect('/order_list.html')
            elif not orderline_form.is_valid():
                messages.error(request, 'There was a problem with one of the order lines. Please review.')
    else :
        if copy_id : 
            order_form, orderline_form, = copy_order_form(copy_id, request, alternative, initial)
        else:
            order_form = OrderForm(initial=initial)
            orderline_form = OrderLineForm(prefix='orderlines')

    return render(request, 'store/order_create.html', {
        'copy_id' : copy_id,
        'order_form' : order_form,
        'orderline_form' : orderline_form
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






ORDER_LIST_HEADERS = (
    ('Order ID', 'order'),
    ('Department to Bill', 'department_name'),
    ('Requester', 'requester'),
    ('Date Submitted', 'date_submitted'),
    ('Start Date', 'date_recurring_start'),
    ('End Date', 'date_recurring_stop'),
    ('Location', 'location'),
    ('Status', 'status'),
)

class OrderListView(generic.ListView):
    model = Order
    billed = Order.objects.get(id=1)
    dep = billed.department
    billed1 = billed.already_billed()
    print(dep)
    context_object_name = 'order_list'
    tab1 = Order.objects.filter(status__icontains='submitted')|Order.objects.filter(status__icontains='in-progress')|Order.objects.filter(is_recurring=True)
    tab2 = Order.objects.filter(status__icontains='complete')
    tab3 = Order.objects.filter(status__icontains='complete')

def view_order(request):
    Orders = Order.objects.all()
    # thing = Order.objects.all()[3]
    sort_headers = SortHeaders(request, ORDER_LIST_HEADERS)
    Not_C = Orders.filter(
        Q(status__icontains='In_progress')| Q(status__icontains='Submitted')| Q(is_recurring=True),
        )
    C_not_B = Orders.filter(status__icontains='Complete').exclude(date_billed__isnull=True)


    return render(request, 
        'store/order_view2.html',{
        'C_not_B': C_not_B,
        'Not_C': Not_C,
        'headers': list(sort_headers.headers()),
        })

# @login_required(login_url='login')
def order_view(request):
    order_list = []
    billed_to_list = []
    OrdersAll = Order.objects.all()
    last_billed_list = []
    o = Order()
    # billed_date = o.date_billed()
    billed = o.already_billed()
    billed_total = 0
    order_total = 0

    p1_filters = {'status': 'Submitted', 'status': 'In_Progress', 'is_recurring': True,}
    order_list = _orders_view_page(request, filters=p1_filters, page_arg='p1')
    # for order in order_list:
    #     # add the update flag here as we can't check it in the template
    #     order_total += order.total()

    C_not_B_filters = {'status':'Complete'}
    C_not_B_list = _orders_view_page(request, filters=C_not_B_filters, page_arg='p2')
    # for billed_to in billed_to_list:
    #     billed_total += billed_to.total()

    last_billed_filters = {'status':'Complete','billed': True,}
    last_billed_list = _orders_view_page(request, filters=last_billed_filters, page_arg='p3')

    if request.GET.get('p2'):
        active_tab = 'p2'
    elif request.GET.get('p3'):
        active_tab = 'p3'
    else:
        active_tab = 'p1'

    return render(request, "store/order_view2.html", {
        'order_list': workorder_list,
        # 'wo_page_range': _trimmed_page_range(workorder_list),
        # 'workorder_total': workorder_total,
        # 'billed_total': billed_total,
        'C_not_B': C_not_B_list,
        # 'billed_to_range': _trimmed_page_range(billed_to_list),
        'last_billed': last_billed_list,
        # 'last_billed_range': _trimmed_page_range(last_billed_list),
        'billed_date': billed_date,
        # 'version': TimeMatrixVersion, necessary??
        # 'search_form': WorkOrderSearch(initial=workorder_filters),
        # 'billed_to_search': WorkOrderSearch(initial=billed_to_filters),
        # 'last_billed_search': WorkOrderSearch(initial=last_billed_filters),
        'active_tab': active_tab,
        'OrdersAll': OrdersAll,
    })


def _orders_view_page(request, filters, page_arg):
    # for user view
    # user = request.user
    # order_list = _workorder_list(user, filters=filters)

    order_list = Order.objects.all

    paginator = Paginator(order_list, 30)

    try:
        orders = paginator.page(request.GET.get(page_arg))
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        orders = paginator.page(paginator.num_pages)

    return orders