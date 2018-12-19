from django import forms
from django.forms.models import formset_factory, modelformset_factory, inlineformset_factory, ModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.db.models import Q, Sum
from django.views import generic
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.template import Context, RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpRequest, HttpResponse,  JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core import serializers
from dateutil import relativedelta
from datetime import datetime, date
from .forms import *
from .models import *
from .resources import *
import MySQLdb, sys
import json as simplejson
import csv
import time
import socket
import platform
import os


def index(request):
    context = {}
    return render (request, 'store/home.html', context)

def home(request):
    post = get_object_or_404(Announcements)
    user = request.user
    #if staff member
    if request.method == "POST" and 'aform' in request.POST:
        AForm = AnnouncementsForm(request.POST, instance=post)
        if AForm.is_valid():
            AForm.save()
            messages.success(request,
            'Annoucements have been updated')
            return HttpResponseRedirect('/store/')
    else:
        AForm = AnnouncementsForm(instance=post)    
    if not request.user.is_authenticated:
        Email_form = Email_Form(initial={'To': 'harrisons1@janelia.hhmi.org'})
        sender = ''
    else:
        Email_form = Email_Form(initial={'To': 'harrisons1@janelia.hhmi.org', 'From': user.user_profile.email_address})
        sender = user.get_full_name()
    if request.method == "POST" and 'eform' in request.POST:
        Email = Email_Form(request.POST)
        if Email.is_valid():
            form_to = Email.cleaned_data['To']
            form_from = Email.cleaned_data['From']
            form_content = Email.cleaned_data['Text']
            ctx = Context({
                'form_to': form_to,
                'form_from': form_from,
                'form_content': form_content,
                'sender': sender,
            })
            subject = 'Feedback about mediastore'
            msg_plain = render_to_string('feedback_email.txt', ctx.flatten())
            msg_html = render_to_string('feedback_email.html', ctx.flatten())
            send_mail(
                subject,
                msg_plain,
                form_from,
               [form_to],
               html_message=msg_html,
                )
            messages.success(request,
            'Email was successfully sent')
            return HttpResponseRedirect('/store/')
        else:
            messages.error(request, "Sorry, your email can't be sent at this time. Please email coffmans@janelia.hhmi.org directly.")
            return HttpResponseRedirect('/store/')

    return render(request, 'store/home.html', {
        'post': post,
        'AForm': AForm,
        'user': user,
        'Email_form': Email_form,
        }
    )

def login(request, user):
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
            return HttpResponseRedirect('/inventory/')
    else: formset = ItemModelFormset(queryset=Inventory.objects.none())
    # just show the form
    return render(request,
    'store/item_form.html', {
    'formset': formset,
    'inventory': inventory,
    'user': user,
    })

@login_required(login_url='login')
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
    })

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
        return delete_item(request, id) #what is this doing? ~FIX~
    else:
        return get_item(request, id)

def __build_inventory_groups():
    """ build inventory lists grouped by mediatype.

        This data is used on the front-end to build mediatype and inventory dropdowns
    """
    inventory_lists = {}
    for type_val, display in MEDIA_CHOICES:
        inventory_choices = [{
            'id': inv.id,
            'desc': inv.inventory_text,
            'container': inv.container,
            'notes': inv.notes_inv,
            'vol': inv.volume,
            'cost': str(inv.cost),
            'media_code': type_val
        } for inv
            in Inventory.objects.filter(media_type=type_val)]
        inventory_lists[type_val] = inventory_choices
    return simplejson.dumps(inventory_lists)


def __build_signout_groups():
    """ build inventory lists grouped by mediatype.

        This data is used on the front-end to build mediatype and inventory dropdowns
    """
    signout_lists = {}
    for type_val, display in MEDIA_CHOICES:
        signout_choices = [{
            'id': inv.id,
            'desc': inv.inventory_text,
            'container': inv.container,
            'notes': inv.notes_inv,
            'vol': inv.volume,
            'cost': str(inv.cost),
            'media_code': type_val
        } for inv
            in Inventory.objects.filter(media_type=type_val)]
        signout_lists[type_val] = signout_choices
    return simplejson.dumps(signout_lists)

@login_required(login_url='login')
def create_order(request, copy_id=None):

    order = Order()
    user = request.user

    if request.method == "POST":

        order_form = OrderForm(request.POST, request.FILES, prefix='order', instance=order, initial={
            'submitter': request.user, 'requester': request.user, 'department': user.user_profile.department, 'project_code': user.user_profile.hhmi_project_id})
        orderlineformset = OrderLineInlineFormSet(
            request.POST, prefix='orderlines', instance=order)

        if order_form.is_valid() and orderlineformset.is_valid():
            # TODO for Scarlett and Amanda: decide desired behavior for date_submitted.
            #   Some options:
            #       only set on create (but this is the same as date_created...)--handle in model
            #       update on edit or create only set on create--handle in model

            # order = order_form.save(commit=False)
            # order.submitter = user
            # order.save()
            order_form.save()
            orderlineformset.save()
            domain = 'http://mediastore.int.janelia.org' #NOT BEST SOLUTION ~FIX~
            subject,from_email,to = 'MediaStore Order #{0} Submitted'.format(order_form.instance.id), 'mediafacility@janelia.hhmi.org', order_form.instance.requester.user_profile.email_address
            context = Context({
                'id': order_form.instance.id,
                'location': order_form.instance.location,
                'c_or_e': 'created',            
                'upload': order_form.instance.doc,
                'domain': domain,
            })
            m_plain = render_to_string('create_email.txt', context.flatten())
            m_html = render_to_string('create_email.html', context.flatten())
            email =EmailMultiAlternatives(
               subject,
               m_plain,
               from_email,
               [to],
               cc=[
                # order_form.instance.submitter.user_profile.email_address, 
               'mediafacility@janelia.hhmi.org'],
            )
            email.attach_alternative(m_html, "text/html")
            email.send()
            messages.success(request,
            'Order {0} was successfully created.'.format(order_form.instance.id))
            return HttpResponseRedirect('/order/view')
        else:
            messages.error(request, 'There was a problem saving your order. Please review the errors below.')
    else:

        if copy_id:
            try:
                order = Order.objects.get(pk=copy_id)
            except Order.DoesNotExist:
                messages.error(
                    request, 'Could not find order #{} for copy. Order does not exist.'.format(copy_id))
                return HttpResponseRedirect('/order/view')
            order_form = OrderForm(prefix='order', instance=order)
            orderlineformset = OrderLineInlineFormSet(prefix='orderlines')
            orderlineformset.copy_orderline_data(order)

        else:
            order_form = OrderForm(prefix='order', instance=order, initial={
            'submitter': request.user, 'requester': request.user, 'department': user.user_profile.department, 'project_code': user.user_profile.hhmi_project_id})
            orderlineformset = OrderLineInlineFormSet(
                prefix='orderlines', instance=order)



    return render(request, 'store/order_create.html', {
        'copy_id' : copy_id,
        'order_form' : order_form,
        'formset': orderlineformset,
        'inventory_lists': __build_inventory_groups(),
        'media_types': MEDIA_CHOICES,
        'user': user,
    })

@login_required(login_url='login')
def edit_order(request, id):
    #TODO: Need to check if user is permitted to edit this order. Otherwise, should create a
    # new order/view/{id} view and template, and redirect the user there if they are allowed to view
    # but not edit
    try:
        order = Order.objects.get(pk=id)
    except Order.DoesNotExist:  # expression as identifier:
        messages.error(
            request, 'Could not edit order #{}. Order does not exist.'.format(id))
        return HttpResponseRedirect('/order/view')

    if request.method == "POST":

        order_form = OrderForm(request.POST, request.FILES, prefix='order', instance=order,)
        orderlineformset = OrderLineInlineFormSet(
            request.POST, prefix='orderlines', instance=order)

        if order_form.is_valid() and orderlineformset.is_valid():
            order = order_form.save()
            orderlineformset.save()
            domain = 'http://mediastore.int.janelia.org' #NOT BEST SOLUTION ~FIX~
            subject,from_email,to = 'MediaStore Order #{0} Edited'.format(order_form.instance.id), 'mediafacility@janelia.hhmi.org', order_form.instance.requester.user_profile.email_address
            context = Context({
                'id': order_form.instance.id,
                'location': order_form.instance.location,
                'c_or_e': 'edited',
                'domain': domain,
            })
            m_plain = render_to_string('create_email.txt', context.flatten())
            m_html = render_to_string('create_email.html', context.flatten())
            email =EmailMultiAlternatives(
               subject,
               m_plain,
               from_email,
               [to],
               cc=[order_form.instance.submitter.user_profile.email_address, 'mediafacility@janelia.hhmi.org'],
            )
            email.attach_alternative(m_html, "text/html")
            email.send()
            messages.success(request,
                'Order #{0} was successfully updated.'.format(order_form.instance.id))
            return HttpResponseRedirect('/order/view')
        else:
            messages.error(request, 'There was a problem saving your order. Please review the errors below.')
    else:
        order_form = OrderForm(prefix='order', instance=order)
        orderlineformset = OrderLineInlineFormSet(
            prefix='orderlines', instance=order)

    return render(request, 'store/order_create.html', {
        'order_form': order_form,
        'formset': orderlineformset,
        'inventory_lists': __build_inventory_groups(),
        'media_types': MEDIA_CHOICES
    })

#neither one of these delete views work WHY?? ~fix~
class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'delete_order.html'

    def get_success_url(self):
        return reverse('view_order')

@login_required(login_url='login')
def delete_order(request, id):
    delOrder = get_object_or_404(Order, pk=id)
    if delOrder:
        delOrder.delete()
        messages.success(request,'Order #{0} was successfully deleted.'.format(id))
        return HttpResponseRedirect('/order/view')
    else:
        messages.error(request, 'Could not delete order #{}. Order does not exist.'.format(id))
    return HttpResponseRedirect('/order/view')
    # try:
    #     delOrder = Order.objects.get(pk=id)
    # except Order.DoesNotExist:  # expression as identifier:
    #     messages.error(request, 'Could not delete order #{}. Order does not exist.'.format(id))
    #     return HttpResponseRedirect('/order/view')
    # delOrder.delete()
    # messages.success(request,'Order #{0} was successfully deleted.'.format(id))
    # return render(request, 'store/order_view2.html')

@login_required
def view_order(request):

    ORDER_LIST_HEADERS_INCOMP = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Submitted', 'date_created'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )

    ORDER_LIST_HEADERS_RECUR = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Submitted', 'date_created'),
        ('Due Date', 'due_date'),
        ('Start Date', 'date_recurring_start'),
        ('End Date', 'date_recurring_stop'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )

    ORDER_LIST_HEADERS_CNB = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Submitted', 'date_created'),
        ('Date Complete', 'date_complete'),
        ('Recurring', 'is_recurring'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )

    ORDER_LIST_HEADERS_CB = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Submitted', 'date_created'),
        ('Date Billed', 'date_billed'),
        ('Recurring', 'is_recurring'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )

    ORDER_LIST_HEADERS_CAN = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Submitted', 'date_created'),
        ('Canceled', 'date_modified'),
        ('Recurring', 'is_recurring'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )
    sort_headers1 = SortHeaders(request, ORDER_LIST_HEADERS_INCOMP)
    sort_headers2 = SortHeaders(request, ORDER_LIST_HEADERS_RECUR)
    sort_headers3 = SortHeaders(request, ORDER_LIST_HEADERS_CNB)
    sort_headers4 = SortHeaders(request, ORDER_LIST_HEADERS_CB)
    sort_headers5 = SortHeaders(request, ORDER_LIST_HEADERS_CAN)


    user = request.user
    
    # if user is not staff, only show orders where user is requester OR submitter. eventually add manager to view all department/lab orders ~FIX~
    if user.is_staff is False:
        orders = Order.objects.preferred_order().filter(Q(submitter=user)|Q(requester=user))
    else:
        orders = Order.objects.preferred_order().all()

    today = date.today()
    nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date()
    lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '24','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-1)
    twobills = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '28','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-2)

    if today >= nextbill:
        nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=1)
        lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '24','%Y-%m-%d' ).date()
        twobills = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '28','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-1)
    
    days = (nextbill - today).days

    #delete canceled orders that were created over 31 days ago
    dates = Order.objects.all()
    for x in dates:
        dc = x.date_created
        days_to_delete = (today-dc).days
        if x.status == 'Canceled' and days_to_delete > 31:
            x.delete()

    incomp_queryset = orders.filter(is_recurring=False).exclude(status__icontains='Complete').exclude(status__icontains='Billed').exclude(status__icontains='Auto').exclude(
    status__icontains='Canceled').exclude(date_billed__isnull=False).prefetch_related('orderline_set').order_by(sort_headers1.get_order_by())
    #exclude date_recurring_stop takes the end date for recurring orders, checks if it is before today. If so, it is excluded from the view.
    recur_queryset = orders.filter(is_recurring=True).exclude(status__icontains='Complete').exclude(status__icontains='Billed').exclude(status__icontains='Auto').exclude(
    status__icontains='Canceled').exclude(date_recurring_stop__lt = today).prefetch_related('orderline_set').order_by(sort_headers2.get_order_by())
    compNotBill_queryset = orders.filter(status__icontains='Complete').exclude(date_billed__isnull=False).order_by('date_complete').prefetch_related('orderline_set').order_by(
    sort_headers3.get_order_by())
    compBill_queryset = orders.filter(status__icontains='Billed').filter(date_billed__range=[twobills, today]).order_by('-date_billed').prefetch_related('orderline_set').order_by(
    sort_headers4.get_order_by())
    cancel_queryset = orders.filter(status__icontains='Canceled').order_by('date_created').prefetch_related('orderline_set').order_by(sort_headers5.get_order_by())

    #pagination
    page = request.GET.get('page')
    paginatorI = Paginator(incomp_queryset, 50)
    paginatorR = Paginator(recur_queryset, 50)
    paginatorCNB = Paginator(compNotBill_queryset, 150)
    paginatorCB = Paginator(compBill_queryset, 150)
    paginatorCAN = Paginator(cancel_queryset, 50)

    try:
        pagesI = paginatorI.page(page)
        pagesR = paginatorR.page(page)
        pagesCNB = paginatorCNB.page(page)
        pagesCB = paginatorCB.page(page)
        pagesCAN = paginatorCAN.page(page)
    except PageNotAnInteger:
        pagesI = paginatorI.page(1)
        pagesR = paginatorR.page(1)
        pagesCNB = paginatorCNB.page(1)
        pagesCB = paginatorCB.page(1)
        pagesCAN = paginatorCAN.page(1)
    except EmptyPage:
        pagesI = paginatorI.page(paginatorI.num_pages)
        pagesR = paginatorR.page(paginatorR.num_pages)
        pagesCNB = paginatorCNB.page(paginatorCNB.num_pages)
        pagesCB = paginatorCB.page(paginatorCB.num_pages)
        pagesCAN = paginatorCAN.page(paginatorCAN.num_pages)

    pageI_query = incomp_queryset.filter(id__in=[pageI.id for pageI in pagesI])
    pageR_query = recur_queryset.filter(id__in=[pageR.id for pageR in pagesR])
    pageCNB_query = compNotBill_queryset.filter(id__in=[pageCNB.id for pageCNB in pagesCNB])
    pageCB_query = compBill_queryset.filter(id__in=[pageCB.id for pageCB in pagesCB])
    pageCAN_query = cancel_queryset.filter(id__in=[pageCAN.id for pageCAN in pagesCAN])
    
    incomp = OrderStatusFormSet(queryset=pageI_query, prefix='incomp')
    recur = OrderStatusFormSet(queryset=pageR_query, prefix='recur')
    compNotBill = OrderStatusFormSet(queryset=pageCNB_query, prefix='compNotBill')
    compBill = OrderStatusFormSet(queryset=pageCB_query, prefix='compBill')
    cancel = OrderStatusFormSet(queryset=pageCAN_query, prefix='cancel')

    if request.method == 'POST':
        # for each order category, check to see if the form had been updated and save
        order_formset = OrderStatusFormSet(request.POST, prefix='incomp')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

        order_formset = OrderStatusFormSet(request.POST, prefix='recur')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

        order_formset = OrderStatusFormSet(request.POST, prefix='compNotBill')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

        order_formset = OrderStatusFormSet(request.POST, prefix='compBill')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

        order_formset = OrderStatusFormSet(request.POST, prefix='cancel')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

    return render(request,
        'store/order_view2.html',{
        'headers1': list(sort_headers1.headers()),
        'headers2': list(sort_headers2.headers()),
        'headers3': list(sort_headers3.headers()),
        'headers4': list(sort_headers4.headers()),
        'headers5': list(sort_headers5.headers()),
        'user': user,
        'orders': orders,
        'pagesI': pagesI,
        'pagesR': pagesR,
        'pagesCNB': pagesCNB,
        'pagesCB': pagesCB,
        'pagesCAN': pagesCAN,
        'incomp':incomp,
        'recur':recur,
        'compNotBill':compNotBill,
        'compBill':compBill,
        'cancel': cancel,
        'days': days,
        })

def export_ordersCNB(request):
    
    orders = Order.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Complete_not_billed.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order_ID','Date_Created', 'Product', 'Qty', 'Price', 'Requester_Email'])
    compNotBill = orders.filter(status__icontains='Complete').exclude(date_billed__isnull=False).prefetch_related('orderline_set').values_list(
    'id','date_created','orderline__inventory__inventory_text', 'orderline__qty', 'orderline__inventory__cost','requester__user_profile__email_address')

    for record in compNotBill:
        writer.writerow(record)            

    return response

def export_ordersIP(request):
    
    orders = Order.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="In_Progress.csv"'
    writer = csv.writer(response)
    writer.writerow(['order_id', 'Requester', 'Submitter', 'Date_Submitted', 'Is_Recurring', 'Due_Date', 'Product', 'Qty', 'Unit_Price', 'Special_Instructions', 'Location'])
    inProgress = orders.filter(status__icontains='Progress').exclude(date_billed__isnull=False).exclude(is_recurring=True).prefetch_related('orderline_set').values_list(
    'id','requester__username', 'submitter__username', 'date_created', 'is_recurring', 'due_date', 'orderline__inventory__inventory_text', 
    'orderline__qty', 'orderline__inventory__cost', 'notes_order','location')
    today = date.today()
    iplist = []
    for x in orders:
        if x.due_date:
            due = x.due_date
            days_to_due = (due-today).days
            if -6 <= days_to_due <= 6:
                iplist.append(x.id)
    ipRecur = Order.objects.filter(pk__in=iplist).values_list('id','requester__username', 'submitter__username', 'date_created', 'is_recurring', 'due_date', 'orderline__inventory__inventory_text', 
    'orderline__qty', 'orderline__inventory__cost', 'notes_order','location')            
    for record in ipRecur:
        writer.writerow(record)
    
    for record in inProgress:
        writer.writerow(record)

    return response


@login_required(login_url='login')
def email_form(request, id):

    user = request.user
    order_info = get_object_or_404(Order, pk=id)
    domain = 'http://mediastore.int.janelia.org'

    if user.is_staff is True:
        Email_form = Email_Form(initial={'To': order_info.submitter.user_profile.email_address, 'From': 'mediafacility@janelia.hhmi.org'}) 
        sender = 'The Media Facility'
    else:
        Email_form = Email_Form(initial={'To': 'mediafacility@janelia.hhmi.org', 'From': order_info.submitter.user_profile.email_address}) 
        sender = order_info.requester.get_full_name()
    if request.method == "POST":
        Email = Email_Form(request.POST)
        if Email.is_valid():
            form_to = Email.cleaned_data['To']
            form_from = Email.cleaned_data['From']
            form_content = Email.cleaned_data['Text']
            ctx = Context({
                'form_to': form_to,
                'form_from': form_from,
                'form_content': form_content,
                'order_id':order_info.id,
                'domain': domain,
                'sender': sender,
            })
            subject = 'Message regarding MediaStore Order {0}'.format(order_info.id)
            msg_plain = render_to_string('details_email.txt', ctx.flatten())
            msg_html = render_to_string('details_email.html', ctx.flatten())
            send_mail(
                subject,
                msg_plain,
                form_from,
               [form_to],
               html_message=msg_html,
                )
            messages.success(request,
            'Email was successfully sent')
            return HttpResponseRedirect('/order/view/')
    return render(request,
    'store/email_form.html',{
        'Email_form': Email_form,
        'order_info': order_info,
    })

@login_required
def current_sign_outs (request):
    ORDER_LIST_HEADERS_CORN = (
        ('Order ID', 'order'),
        ('Department to Bill', 'department__department_name'),
        ('Date Submitted', 'date_created'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total'),
    )

    ORDER_LIST_HEADERS_CORN_B = (
        ('Order ID', 'order'),
        ('Department to Bill', 'department__department_name'),
        ('Date Submitted', 'date_created'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total'),
        ('Date Billed', 'date_billed'),
    )

    sort_headers1 = SortHeaders(request, ORDER_LIST_HEADERS_CORN)
    sort_headers2 = SortHeaders(request, ORDER_LIST_HEADERS_CORN_B)
    orders = Order.objects.all()
    today = date.today()
    nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date()
    lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '24','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-1)
    twobills = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '28','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-2)

    if today >= nextbill:
        nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=1)
        lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '24','%Y-%m-%d' ).date()
        twobills = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '28','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-1)
    days = (nextbill - today).days

    current_queryset = orders.filter(notes_order__icontains='signout').exclude(status__icontains='Canceled').exclude(status__icontains='Billed')
    billed_queryset = orders.filter(date_billed__isnull=False).exclude(status__icontains='Canceled').filter(date_billed__range=[twobills, today]).order_by('-date_billed').filter(notes_order__icontains='signout')

 #pagination
    page = request.GET.get('page')
    paginatorCu = Paginator(current_queryset, 50)
    paginatorBi = Paginator(billed_queryset, 50)

    try:
        pagesCu = paginatorCu.page(page)
        pagesBi = paginatorBi.page(page)
    except PageNotAnInteger:
        pagesCu = paginatorCu.page(1)
        pagesBi = paginatorBi.page(1)
    except EmptyPage:
        pagesCu = paginatorCu.page(paginatorCu.num_pages)
        pagesBi = paginatorBi.page(paginatorBi.num_pages)

    pageCu_query = current_queryset.filter(id__in=[pageCu.id for pageCu in pagesCu])
    pageBi_query = billed_queryset.filter(id__in=[pageBi.id for pageBi in pagesBi])
    
    current = OrderStatusFormSet(queryset=pageCu_query, prefix='current')
    billed = OrderStatusFormSet(queryset=pageBi_query, prefix='billed')

    if request.method == 'POST':
        # for each order category, check to see if the form had been updated and save
        order_formset = OrderStatusFormSet(request.POST, prefix='current')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

        order_formset = OrderStatusFormSet(request.POST, prefix='billed')
        if order_formset.has_changed() and order_formset.is_valid():
            order_formset.save()

    return render(request,
        'store/sign_out_view.html',{
        'headers1':list(sort_headers1.headers()),
        'headers2':list(sort_headers2.headers()),
        'current': current,
        'billed': billed,
        'orders': orders,
        'days': days,
        'pagesCu': pagesCu,
        'pagesBi': pagesBi,
        })

@login_required
def sign_outs_remainder(request):

    user = request.user
    orders = Order.objects.all()
    bv = Bottles_Vials.objects.all()
    today = date.today()
    nextbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '25','%Y-%m-%d' ).date()
    lastbill = datetime.strptime(str(today.year) + '-' + str(today.month) + '-' + '24','%Y-%m-%d' ).date() + relativedelta.relativedelta(months=-1)    
    
    currentBottles = list(orders.prefetch_related('orderline_set').filter(orderline__inventory=1245).filter(date_created__range=[today, nextbill]).aggregate(
    Sum('orderline__qty')).values())[0]

    currentVials = list(orders.prefetch_related('orderline_set').filter(orderline__inventory=1263).filter(date_created__range=[today, nextbill]).aggregate(
    Sum('orderline__qty')).values())[0]

    inputBottles = Bottles_Vials.objects.get(item='1245')

    inputVials = Bottles_Vials.objects.get(item='1263')

    if request.method == "POST":
        formset = B_VFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request,
            'Amounts have been updated.')
            return HttpResponseRedirect('/signout/remainder')
        else:
            messages.error(request, 'There was a problem updating amounts.')
    else: formset = B_VFormSet()

    return render(request,
        'store/signout_leftovers.html',{
        'currentBottles': currentBottles,
        'currentVials': currentVials,
        'orders': orders,
        'formset': formset,
        'inputBottles': inputBottles,
        'inputVials': inputVials,
        })

# class SearchListView(ListView):
#     """
#     Display a Blog List page filtered by the search query.
#     """
#     model = Order
#     paginate_by = 10
#     template_name = 'store/search.html'

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_staff is False:
#             qs = Order.objects.preferred_order().filter(Q(submitter=user)|Q(requester=user))
#         else:
#             qs = Order.objects.all()

#         keywords = self.request.GET.get('q')
#         if keywords:
#             query = SearchQuery(keywords)
#             vector = SearchVector('submitter__last_name', 'submitter__first_name', 'requester__last_name', 'requester__first_name', 'department', 'date_created', 'date_billed', 'orderline__inventory__inventory_text', )
#             qs = qs.annotate(search=vector).filter(search=query)
#             qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-rank')

#         return qs

def search(request):

    ORDER_LIST_HEADERSCr = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Date Created', 'date_created'),
        ('Recurring', 'is_recurring'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )
    ORDER_LIST_HEADERSCo = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Date Completed', 'date_complete'),
        ('Recurring', 'is_recurring'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )

    ORDER_LIST_HEADERSB = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Date Billed', 'date_billed'),
        ('Recurring', 'is_recurring'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )
    ORDER_LIST_HEADERSKey = (
        ('Order ID', 'id'),
        ('Department to Bill', 'department__department_name'),
        ('Cost Center', 'department__number'),
        ('Requester', 'requester__last_name'),
        ('Recurring', 'is_recurring'),
        ('Location', 'location'),
        ('Status', 'status'),
        ('Order Total', 'order_total')
    )

    sort_headers1 = SortHeaders(request, ORDER_LIST_HEADERSCr)
    sort_headers2 = SortHeaders(request, ORDER_LIST_HEADERSCo)
    sort_headers3 = SortHeaders(request, ORDER_LIST_HEADERSB)
    sort_headers4 = SortHeaders(request, ORDER_LIST_HEADERSKey)

    user = request.user
    if user.is_staff is False:
        report = Order.objects.filter(Q(submitter=user)|Q(requester=user))
    else:
        report = Order.objects.get(id=441)

    if request.method == 'POST':
        form = OrderSearchForm(request.POST)
        if form.is_valid():
            if form.instance.search_date_from and form.instance.search_keyword:
                date_type = form.instance.date_type
                date_from = form.instance.search_date_from
                date_to = form.instance.search_date_to
                keyword = form.instance.search_keyword
                if date_type == 'Order Created':
                    reportCr = report.prefetch_related('orderline_set').filter(Q(submitter__icontains=keyword)|Q(requester__icontains=keyword)|Q(notes_order__icontains=keyword)|Q(
                    project_code__icontains=keyword)|Q(department__number__icontains=keyword)| Q(orderline__inventory__inventory_text__icontains=keyword)).filter(
                    date_created__range=[date_from, date_to])
                elif date_type == 'Order Completed':
                    reportCo = report.prefetch_related('orderline_set').filter(Q(submitter__icontains=keyword)|Q(requester__icontains=keyword)|Q(notes_order__icontains=keyword)|Q(
                    project_code__icontains=keyword)|Q(department__number__icontains=keyword)| Q(orderline__inventory__inventory_text__icontains=keyword)).filter(
                    date_complete__range=[date_from, date_to])
                else:
                    reportB = report.prefetch_related('orderline_set').filter(Q(submitter__icontains=keyword)|Q(requester__icontains=keyword)|Q(notes_order__icontains=keyword)|Q(
                    project_code__icontains=keyword)|Q(department__number__icontains=keyword)| Q(orderline__inventory__inventory_text__icontains=keyword)).filter(
                    date_billed__range=[date_from, date_to])
            elif form.instance.search_date_from:
                date_type = form.instance.date_type
                date_from = form.instance.search_date_from
                date_to = form.instance.search_date_to
                if date_type == 'Order Created':
                    reportCr = report.filter(date_created__range=[date_from, date_to])
                elif date_type == 'Order Completed':
                    reportCo = report.filter(date_complete__range=[date_from, date_to])
                else:
                    reportB = report.filter(date_billed__range=[date_from, date_to])
            elif form.instance.search_keyword:
                keyword = form.instance.search_keyword
                reportKey = report.prefetch_related('orderline_set').filter(Q(submitter__icontains=keyword)|Q(requester__icontains=keyword)|Q(notes_order__icontains=keyword)|
                Q(project_code__icontains=keyword)|Q(department__number__icontains=keyword)| Q(orderline__inventory__inventory_text__icontains=keyword))
            else:
               messages.error(request, "You didn't submit any dates or keywords to search")
        else:
            messages.error(request, "invalid form")
    else:
        form = OrderSearchForm()
    return render(request, 'store/search.html', {
        'user': user,
        'form': form,
        'reportCr': reportCr,
        'reportCo': reportCo,
        'reportB': reportB,
        'reportKey': reportKey,
        'headersCr': list(sort_headers1.headers()),
        'headersCo': list(sort_headers2.headers()),
        'headersB': list(sort_headers3.headers()),
        'headersKey': list(sort_headers4.headers()),
    })


def ajax(request):
    requester_test = request.GET.get('id', None)
    user = User.objects.get(id=requester_test)
    department = user.user_profile.department
    project = user.user_profile.hhmi_project_id 
    data = {'r_id': user.id, 'd_id':department.id, 'p_id':project, 'up_id':user.user_profile.id}
    data = simplejson.dumps(data)
    dataOne = simplejson.loads(data)
    return JsonResponse(dataOne)

@login_required(login_url='login')
def create_signout(request):

    order = Order()
    user = request.user
    u = user.id

    if u == 17380:
        loc = '2E.233'
        uname = 2
        q = Inventory.objects.filter(Q(id=1245) | Q(id=1263) | Q(id=1262))
    elif u == 17381:
        loc = '1E.390'
        uname = 1
        q = Inventory.objects.filter(Q(id=1267))
    elif u == 17382:
        loc = '3E.265'
        uname = 3
        q = Inventory.objects.filter(Q(id=1245) | Q(id=1263))
    else:
        loc = False
        uname = False
        q = Inventory.objects.all()
    

    if request.method == "POST":

        order_form = OrderForm(request.POST, request.FILES, prefix='order', instance=order, initial={
            'location': loc})
        orderlineformset = OrderLineInlineFormSet(
            request.POST, prefix='orderlines', instance=order,)
        for form in orderlineformset:
            form.fields['inventory'].queryset = q
        if order_form.is_valid() and orderlineformset.is_valid():
            order = order_form.save(commit=False)
            order.location = loc
            order.is_recurring = False
            order.status = 'Complete'
            order.notes_order = 'Signout'
            # order.submitter = order.requester
            order.save()
            orderlineformset.save()
            messages.success(request,
            'Thank you for signing out food!')
            return HttpResponseRedirect('/signout/new')
        else:
            messages.error(request, 'There was a problem saving your order. Please review the errors below.')
    else:
            order_form = OrderForm(prefix='order', instance=order,initial={
            'location': loc})
            orderlineformset = OrderLineInlineFormSet(
                prefix='orderlines', instance=order,)
            for form in orderlineformset:
                form.fields['inventory'].queryset = q

    return render(request, 'store/signout_create.html', {
        'order_form' : order_form,
        'formset': orderlineformset,
        'media_types': MEDIA_CHOICES,
        'loc': loc,
        'uname': uname,
        'user': user,
        'signout_lists': __build_signout_groups(),
        'q': q,
    })