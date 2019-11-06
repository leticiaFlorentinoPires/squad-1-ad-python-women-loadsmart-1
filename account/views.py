from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from account.forms import SignUpForm


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        #TODO
        #não tem jeito do form ficar valido... 
        #em todos os casos recebo o mesmo erro: The two password fields didn't match.
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # TODO 
            # esse redirect tá com erro.. algum problema no fluxo
            # return redirect('/events')
        else:
            context = {
                'form': form,
                'error': form.error_messages,
            }
            return render(request, 'registration/signup.html', context=context)
    else:
        return render(request, 'registration/signup.html', {'form': form})
