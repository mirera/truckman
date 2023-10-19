from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from django.http import JsonResponse


# landing page or home 
@login_required(login_url='login') 
def index_page(request): 
    context = {
        
    }
    return render(request, 'index.html', context)



def custom_404(request, exception):
    return render(request, 'error/404.html', status=404)


#storing user's current timezone to session


def set_timezone(request):
    if request.method == 'POST':
        user_timezone = request.POST.get('timezone')
        request.session['user_timezone'] = user_timezone
        request.session.save()
        return JsonResponse({'message': 'Timezone set successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


