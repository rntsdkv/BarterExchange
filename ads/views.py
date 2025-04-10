from django.shortcuts import render, redirect
from .forms import AdForm, RegistrationForm


def index(request):
    if request.user.is_authenticated:
        print(request.user.my_ads.all())
    return render(request, 'index.html')


def ad_form(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user_id = request.user.id
            ad.save()
            print(form.cleaned_data)

            context = {'ad_success': True}
            return render(request, 'index.html', context)
        else:
            print(form.errors)
            form = AdForm()

            context = {'form': form,
                       'success': False}
        return render(request, 'ad.html', context)
    elif request.method == 'GET':
        context = {'form': AdForm(),
                   'success': True}
        return render(request, 'ad.html', context)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def success_new_ad(request):
    return render(request, 'success_new_ad.html')