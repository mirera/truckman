from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect


# landing page or home 
@login_required(login_url='login') 
def index_page(request): 
    context = {
        
    }
    return render(request, 'index.html', context)
