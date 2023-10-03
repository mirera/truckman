from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect


# landing page or home 
@login_required(login_url='login') 
def index_page(request): 
    context = {
        
    }
    return render(request, 'index.html', context)



def custom_404(request, exception):
    return render(request, 'error/404.html', status=404)

