from django import forms
from .models import (
    Vehicle,
    Vehicle_Make,
    Vehicle_Model,
    Driver,
    Customer,
    Consignee,
    Trip,
    Shipper,
    Load,
    Service,
    Estimate,
    Invoice,
    Payment,
    Expense_Category,
    Expense,
    Reminder
)



#---------------------------------- Vehicle Make forms ------------------------------------------
class VehicleMakeForm(forms.ModelForm):
    class Meta:
        model = Vehicle_Make
        fields = '__all__'
        exclude =['company']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Mercedes'}),
            } 

#---------------------------------- Vehicle model forms ------------------------------------------
class VehicleModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        
        company = kwargs.pop('company')# Get the company from kwargs
        super(VehicleModelForm, self).__init__(*args, **kwargs)
        self.fields['make'].queryset = Vehicle_Make.objects.filter(company=company)
        
    class Meta:
        model = Vehicle_Model
        fields = '__all__'
        exclude =['company']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Mercedes'}),
                'make': forms.Select(attrs={'class': 'form-select js-select2', 'id':'vehicleMakeSelect2'}),
            } 

#---------------------------------- Vehicle forms -----------------------------------------------
class VehicleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
       # make = kwargs.pop('make')
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.fields['make'].queryset = Vehicle_Make.objects.filter(company=company)
        self.fields['model'].queryset = Vehicle_Model.objects.filter(company=company)

    class Meta:
        model = Vehicle
        fields = '__all__'
        exclude =['company']

        widgets = {
                'plate_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Registration number'}),
                'trailer_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Trailer number'}),
                'vin': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'1KZ-345678'}),
                'milage': forms.NumberInput(attrs={'class': 'form-control number-spinner','value': '0', 'placeholder':'345678'}),
                'make': forms.Select(attrs={'class': 'form-select js-select2', 'id':'vehicleMakeSelect'}),
                'model': forms.Select(attrs={'class': 'form-select js-select2', 'id':'vehicleModelSelect'}),
                'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'White'}),
                'milage_unit': forms.Select(attrs={'class': 'form-select js-select2'}),
                'condition': forms.Select(attrs={'class': 'form-select js-select2'}),
                'insurance_expiry': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'manufacture_year': forms.DateInput(attrs={'class': 'form-control  date-picker-range', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'purchase_year': forms.DateInput(attrs={'class': 'form-control  date-picker-range', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'notes': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'cf-default-textarea' ,'placeholder':'Notes...'}),
                'truck_image': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                'trailer_image': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                'truck_logbook': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                'trailer_logbook': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                'good_transit_licence': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            } 
        
#---------------------------------- Driver forms ------------------------------------------
class DriverForm(forms.ModelForm):

    def __init__(self, *args, **kwargs): 
        company = kwargs.pop('company')# Get the company from kwargs
        super(DriverForm, self).__init__(*args, **kwargs)
        self.fields['assigned_vehicle'].queryset = Vehicle.objects.filter(company=company, is_assigned_driver=False )

    class Meta:
        model = Driver
        fields = '__all__'
        exclude =['company']

        widgets = {
                #personal data
                'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'John '}),
                'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Moriasi'}),
                'id_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'34567800'}),
                'tel_home': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0700000000'}),
                'tel_roam': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0700000000'}),
                'date_hired': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'date_terminated': forms.DateInput(attrs={'class': 'form-control  date-picker-range', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'driver_photo': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                'id_img': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                #dl and passport
                'dl_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'34K5678'}),
                'dl_issuing_authority': forms.Select(attrs={'class': 'form-select js-select2'}),
                'dl_front_img': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                'dl_back_img': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                'passport_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'KZ345678'}),
                'passport_image': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
                #next of kin
                'emergency_contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Moriasi Ndoyo'}),
                'emergency_contact_person_rlshp': forms.Select(attrs={'class': 'form-select js-select2'}),
                'emergency_contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0700000000'}),
                'emergency_contact_two': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0700000000'}),
                #vehicle data
                'assigned_vehicle': forms.Select(attrs={'class': 'form-select js-select2'}),
            } 
        
#---------------------------------- Customer forms ------------------------------------------   
class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = '__all__'
        exclude =['company', 'customer_id', 'date_added']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'John Shippers'}),
                'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Moriasi Iteo'}),
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'034567800'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'info@company.com'}),
                'address_one': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ABC Road'}),
                'address_two': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ABC Road'}),
                'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'KENYA'}),
                'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'MOMBASA'}),
                'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder':'www.company.com'}),
                'credit_limit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'20'}),
                'payment_term': forms.Select(attrs={'class': 'form-select js-select2'}),
                'logo': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            }    

#---------------------------------- Consignee forms ------------------------------------------ 
class ConsigneeForm(forms.ModelForm):
    '''
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['assigned_vehicle'].queryset = Customer.objects.filter(company=company) 
    '''
    class Meta:
        model = Consignee
        fields = '__all__'
        exclude =['company', 'consignee_id', 'date_added']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'John Shippers'}),
                'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Moriasi Iteo'}),
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'034567800'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'info@company.com'}),
                'address_one': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ABC Road'}),
                'address_two': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ABC Road'}),
                'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'KENYA'}),
                'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'MOMBASA'}),
                'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder':'https://company.com'}),
                'logo': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            }    
        
#---------------------------------- Shipper forms ------------------------------------------ 
class ShipperForm(forms.ModelForm):
    '''
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['assigned_vehicle'].queryset = Customer.objects.filter(company=company) 
    '''
    class Meta:
        model = Shipper
        fields = '__all__'
        exclude =['company', 'shipper_id', 'date_added']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'John Shippers'}),
                'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Moriasi Iteo'}),
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'034567800'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'info@company.com'}),
                'address_one': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ABC Road'}),
                'address_two': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ABC Road'}),
                'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'KENYA'}),
                'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'MOMBASA'}),
                'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder':'https://company.com'}),
                'logo': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            }    

#---------------------------------- Load forms -----------------------------------------------

class LoadForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(LoadForm, self).__init__(*args, **kwargs)
        #self.fields['customer'].queryset = Customer.objects.filter(company=company) 
        self.fields['shipper'].queryset = Shipper.objects.filter(company=company) 
        self.fields['consignee'].queryset = Consignee.objects.filter(company=company) 
        self.fields['estimate'].queryset = Estimate.objects.filter(company=company, status='Accepted') 
    
    class Meta:
        model = Load
        fields = '__all__'
        exclude =['company', 'load_id', 'date_added']

        widgets = {
                #'customer': forms.Select(attrs={'class': 'form-select js-select2'}),
                'shipper': forms.Select(attrs={'class': 'form-select js-select2'}), 
                'consignee': forms.Select(attrs={'class': 'form-select js-select2'}),
                'estimate': forms.Select(attrs={'class': 'form-select js-select2', 'id':'estimate'}),
                #load details
                'weight': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'7800, weigh in Tons'}),
                'pickup_date': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'delivery_date': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'quantity_type':forms.Select(attrs={'class': 'form-select js-select2'}),
                'driver_instructions':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Fragile load, Drive with caution!'}),
                
                'legal_disclaimer': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Some legal dissclaimer...'}),
                'notes': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Some notes/description about the load..'})
            }    

#---------------------------------- Trip forms -----------------------------------------------
class TripForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(TripForm, self).__init__(*args, **kwargs)
        self.fields['load'].queryset = Load.objects.filter(company=company) 
        self.fields['vehicle'].queryset = Vehicle.objects.filter(company=company, is_assigned_driver=True)
    
    class Meta:
        model = Trip
        fields = '__all__'
        exclude =['company', 'trip_id', 'date_added']

        widgets = {
                'load': forms.Select(attrs={'class': 'form-select js-select2', 'id':'load'}),
                'vehicle': forms.Select(attrs={'class': 'form-select js-select2','id':'vehicle'}),
                'vehicle_odemeter': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'67800'}),
                'driver_milage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'67800'}),
                'driver_accesory_pay': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'67800'}),
                'driver_advance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'600'}), 
                'pick_up_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nairobi'}), 
                'drop_off_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Kampala'}),
                'distance': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'1000'}),
        }

#---------------------------------- Service forms -----------------------------------------------
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        exclude =['company']

        widgets = {
                'name':forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Glass Transport'}),
                'unit_type': forms.Select(attrs={'class': 'form-select js-select2'}),
                'unit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'600'}),
                'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'2000'}),
                'tax': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'16 for 16%'}),
                
                'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Transport of fragile glasses'}), 
        }

#---------------------------------- Estimate forms -----------------------------------------------
class EstimateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(EstimateForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.filter(company=company) 
    
    class Meta:
        model = Estimate
        fields = '__all__'
        exclude =['company', 'estimate_id', 'date_added']

        widgets = {
                'customer': forms.Select(attrs={'class': 'form-select js-select2', 'id':'customerSelect'}),
                'item': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Steel Coils'}),
                'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Some descriptions.'}),
                #'sub_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'7800'}),
                #'tax': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'7800'}),
                #'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'10'}),
                #'total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'10'}),
                'valid_till': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Note some terms/remarks here.'}),
                'status': forms.Select(attrs={'class': 'form-select js-select2'}), #for updating estimate.
            }    

#---------------------------------- Invoice forms -----------------------------------------------

class InvoiceForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(company=company) 
        self.fields['trip'].queryset = Trip.objects.filter(company=company) 
    
    class Meta:
        model = Invoice
        fields = '__all__'
        exclude =['company',  'invoice_id', 'date_added']

        widgets = {
                'trip': forms.Select(attrs={'class': 'form-select js-select2', 'id':'trip'}),
                'service': forms.Select(attrs={'class': 'form-select js-select2'}),
                'sub_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'7800'}),
                'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'10'}),
                'total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'10'}),
                'valid_till': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'invoice_date': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'due_date': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Add payment details here'})
            }    

#---------------------------------- Payment forms -----------------------------------------------

class PaymentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].queryset = Invoice.objects.filter(company=company) 
    
    class Meta:
        model = Payment
        fields = '__all__'
        exclude =['company']

        widgets = {
                'transaction_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'REHU456WER'}),
                'invoice': forms.Select(attrs={'class': 'form-select js-select2'}),
                'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'7800'}),
                'paid_on': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'payment_method': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'ETF'}),
                'remark': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Some remarks'}),
            }    

#---------------------------------- Expense Category forms --------------------------------------

class ExpenseCategoryForm(forms.ModelForm):
    
    
    class Meta:
        model = Expense_Category
        fields = '__all__'
        exclude =['company']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Fines'}),
            }    

#---------------------------------- Expense  forms -----------------------------------------------

class ExpenseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(ExpenseForm, self).__init__(*args, **kwargs)
        self.fields['expense_category'].queryset = Expense_Category.objects.filter(company=company) 
        self.fields['trip'].queryset = Trip.objects.filter(company=company) 
    
    class Meta:
        model = Expense
        fields = '__all__'
        exclude =['company', 'expense_id' ]

        widgets = {
                'expense_category': forms.Select(attrs={'class': 'form-select js-select2', 'id':'expenseCategorySelect'}),
                'trip': forms.Select(attrs={'class': 'form-select js-select2'}),
                'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'7800'}),
                'date_paid': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'paid_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'REHU456WER'}),
                'receipt': forms.FileInput(attrs={'class': 'form-file-input', 'id': 'customFile'}),
            }    

#---------------------------------- Reminder forms -----------------------------------------------
class ReminderForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')# Get the company from kwargs
        super(ReminderForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(company=company) 
    
    class Meta:
        model = Reminder
        fields = '__all__'
        exclude =['company']

        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Oil Change'}),
                'vehicle': forms.Select(attrs={'class': 'form-select js-select2'}),
                'frequency': forms.Select(attrs={'class': 'form-select js-select2'}),
                'status': forms.Select(attrs={'class': 'form-select js-select2'}),
                'last_date': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                'next_date': forms.DateInput(attrs={'class': 'form-control  date-picker', 'data-date-format':'yyyy-mm-dd', 'placeholder':'yyyy-mm-dd'}),
                
            }    

#---------------------------------- Reminder forms --------------------------------------



