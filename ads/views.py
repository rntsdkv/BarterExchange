from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django_filters.views import FilterView

from .forms import AdForm, RegistrationForm
from .models import Ad, ExchangeProposal, StatusChoices, AdStatus


def index(request):
    income_proposals = []
    outcome_proposals = []
    user_ads = []

    if request.user.is_authenticated:
        user_ads = request.user.my_ads.filter(status=AdStatus.ACTIVE)

        outcome_proposals = ExchangeProposal.objects.filter(
            Q(ad_sender__in=user_ads) & Q(status=StatusChoices.PENDING)
        )
        income_proposals = ExchangeProposal.objects.filter(
            Q(ad_receiver__in=user_ads) & Q(status=StatusChoices.PENDING)
        )

    context = {
        'message': request.GET.get('message'),
        'color': request.GET.get('color'),
        'income_proposals': income_proposals,
        'outcome_proposals': outcome_proposals,
        'user_ads': user_ads
    }
    return render(request, 'index.html', context)


def new_ad_form(request):
    if not request.user.is_authenticated:
        return redirect('auth')

    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            print(form.cleaned_data)

            message = "Объявление успешно опубликовано"
            color = "green"
            return redirect(f'/?message={message}&color={color}')
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
            return redirect('auth')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def ad(request, id):
    ad = get_object_or_404(Ad, id=id)
    # todo: fix 404 page
    return render(request, 'ad.html', {'ad': ad})

def no_access(request):
    return render(request, 'no_access.html')

def ad_edit(request, id):
    ad = get_object_or_404(Ad, id=id)

    print(ad)

    if ad.user != request.user:
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

def ad_delete(request, id):
    ad = get_object_or_404(Ad, id=id)

    if request.method == 'POST':
        if ad.user != request.user:
            return redirect('no_access')

        ad.delete()

        message = "Объявление успешно удалено"
        color = "green"
        return redirect(f'/?message={message}&color={color}')

    message = "Что-то пошло не так..."
    color = "red"
    return redirect(f'/?message={message}&color={color}')


'''
def search(request):
    query = request.GET.get('query')
    page = request.GET.get('page')
    if page is None: page = 1

    if query:
        # todo: исправить нижний регистр
        results = Ad.objects.filter(
            Q(status=AdStatus.ACTIVE) &
            (Q(title__icontains=query) | Q(description__icontains=query))
        )
    else:
        results = Ad.objects.filter(status=AdStatus.ACTIVE)

    paginator = Paginator(results, 10)
    results_of_page = paginator.get_page(page)

    filter_form = FilterView()

    return render(request, 'search.html', {
        'query': query,
        'results': results,
        'results_of_page': results_of_page,
        'next_page': results_of_page.number + 1,
        'current_page': page,
        'previous_page': results_of_page.number - 1,
        'form': filter_form
    })
'''

def ad_exсhange(request, id):
    if not request.user.is_authenticated:
        return redirect('auth')

    ad = get_object_or_404(Ad, id=id)
    selected = request.GET.get('selected')

    if selected is None or not selected.isdigit():
        return render(request, "exchange.html", {'ad': ad})

    user_ad = get_object_or_404(Ad, id=int(selected))

    if request.method == 'POST':
        # todo: проверка что пользователь не один и тот же
        comment = request.POST.get("comment")
        print(user_ad, ad, comment)
        ExchangeProposal.objects.create(ad_sender=user_ad, ad_receiver=ad, comment=comment)

        message = "Вы отправили запрос на обмен"
        color = "green"
        return redirect(f'/?message={message}&color={color}')

    context = {
        'ad': ad,
        'user_ad': user_ad
    }
    return render(request, "exchange_selected.html", context)


def exchange(request, id):
    proposal = get_object_or_404(ExchangeProposal, id=id)
    ad_sender = proposal.ad_sender
    ad_receiver = proposal.ad_receiver

    context = {
        'proposal': proposal,
        'ad': ad_sender,
        'user_ad': ad_receiver
    }
    return render(request, "exchange_page.html", context)


def exchange_update(request, id):
    proposal = get_object_or_404(ExchangeProposal, id=id)
    if not request.user.is_authenticated:
        return redirect('auth')

    if request.method == 'POST' and proposal.status == StatusChoices.PENDING:
        action = request.GET.get('action')
        print(action)

        if action == 'reject':
            if request.user.id == proposal.ad_sender.user_id or request.user.id == proposal.ad_receiver.user_id:
                print('reject')
                proposal.reject()
            else:
                return redirect('no_access')
        elif action == 'accept':
            if request.user.id == proposal.ad_receiver.user_id:
                proposal.accept()
            else:
                return redirect('no_access')

    return redirect(f'/exchange/{id}/')
