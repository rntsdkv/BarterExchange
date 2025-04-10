from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .forms import AdForm, RegistrationForm
from .models import Ad


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


def ad(request, id):
    ad = get_object_or_404(Ad, id=id)
    return render(request, 'ad.html', {'ad': ad})


def no_access(request):
    return render(request, 'no_access.html')

def ad_edit(request, id):
    ad = get_object_or_404(Ad, id=id)

    print(ad)

    if ad.user_id != request.user.id:
        return redirect('no_access')

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ad', id=id)
        else:
            form = AdForm(instance=ad)
    else:
        form = AdForm(instance=ad)

    return render(request, 'ad_edit.html', {'form': form, 'ad': ad})