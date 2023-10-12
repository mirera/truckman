from django.utils import timezone
from datetime import timedelta
from trip.models import Estimate, Invoice, LoadingList, LoadingListItem
from django.shortcuts import get_object_or_404

'''
This function is called when an estimate has been accepted
by the customer. You can also use it to re-generate an 
invoice for a given estimate.
'''
def generate_invoice(estimate): 
        #estimate = Estimate.objects.get(id=estimate.id)
        due_date = timezone.now().date() + timedelta(days=30)
        #create instance of a invoice
        invoice = Invoice.objects.create(
            company=estimate.company,
            estimate = estimate,
            route = estimate.route,
            item = estimate.item,
            trucks = estimate.trucks,
            rate = estimate.rate,
            description = estimate.description,
            sub_total = estimate.sub_total,
            discount = estimate.discount,
            tax = estimate.tax,
            total = estimate.total,
            balance = estimate.total,
            invoice_date = timezone.now().date(),
            due_date = due_date,
            note = estimate.company.invoice_payment_details,
        )
        return invoice  #should return a path to the pdf of the invoice
#--ends

'''
This function is called when an estimate has been accepted
by the customer. It creates a loading list 
'''
def generate_loading_list(estimate):
        estimate = get_object_or_404(Estimate, id=estimate.id)

        #create instance of a loading list
        loading_list = LoadingList.objects.create(
            company=estimate.company,
            estimate = estimate,    
        )

        #create instance of a loading list item
        loading_list_item = []
          
        loading_list_item = LoadingListItem.objects.create(
            company=estimate.company,
            loading_list = loading_list,   
            vehicle = vehicle 
        )


        for item_data in loading_list_items:
            LoadingListItem.objects.create(loading_list=loading_list, **item_data)
#--ends




