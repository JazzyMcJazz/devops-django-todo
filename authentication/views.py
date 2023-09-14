from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

def register(request):
    form = UserCreationForm()

    # if request.method == 'POST':
    #     return

    context = { 'form': form }
    return render(request, 'authentication/register.html', context)
    
