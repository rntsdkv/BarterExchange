from django.shortcuts import render, redirect
from .forms import AdForm, RegistrationForm


def index(request):
    ad_success = request.GET.get('ad_success')
    if request.user.is_authenticated:
        print(request.user.my_ads.all())
    return render(request, 'index.html', {'ad_success': ad_success})


def new_ad_form(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user_id = request.user.id
            ad.save()
            print(form.cleaned_data)

            ad_success = True
            return redirect(f'/?ad_success={ad_success}')
        else:
            print(form.errors)
            form = AdForm()

            context = {'form': form,
                       'success': False}
        return render(request, 'new_ad.html', context)
    elif request.method == 'GET':
        context = {'form': AdForm(),
                   'success': True}
        return render(request, 'new_ad.html', context)


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