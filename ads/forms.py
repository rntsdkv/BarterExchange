from django import forms
from django.contrib.auth import user_logged_in
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.template.context_processors import request
from django_filters.views import FilterView
import django_filters
from ads.models import Ad, AdCategory, AdStatus, AdCondition, StatusChoices, ExchangeProposal


class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image', 'category', 'condition']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'image': 'Фото',
            'category': 'Категория',
            'condition': 'Состояние'
        }

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Пароль'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label='Повторите пароль'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': 'Никнейм',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Никнейм',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class CustomLoginView(LoginView):
    template_name = 'auth.html'
    authentication_form = CustomLoginForm
    redirect_authenticated_user = True

class AdFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_search',
        label='Поиск'
    )
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=AdCategory.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категории'
    )
    condition = django_filters.ChoiceFilter(
        choices=AdCondition.choices,
        label='Состояние'
    )

    class Meta:
        model = Ad
        fields = []
        # fields = ['category', 'condition']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            title__icontains=value
        ) | queryset.filter(
            description__icontains=value
        )

class AdFilterView(FilterView):
    model = Ad
    filterset_class = AdFilter
    template_name = 'search.html'
    context_object_name = 'ads'
    paginate_by = 1

    def get_queryset(self):
        return Ad.objects.filter(status=AdStatus.ACTIVE)

class ProposalFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(
        method='filter_sender_search',
        label='Поиск по отправителю'
    )
    receiver = django_filters.CharFilter(
        method='filter_receiver_search',
        label='Поиск по получателю'
    )
    status = django_filters.ChoiceFilter(
        choices=StatusChoices.choices,
        label='Статус'
    )

    class Meta:
        model = ExchangeProposal
        fields = []

    def filter_sender_search(self, queryset, name, value):
        return queryset.filter(
            ad_sender__user__username__icontains=value
        )

    def filter_receiver_search(self, queryset, name, value):
        return queryset.filter(
            ad_receiver__user__username__icontains=value
        )

class ProposalFilterView(FilterView):
    model = ExchangeProposal
    filterset_class = ProposalFilter
    template_name = 'index.html'
    context_object_name = 'proposals'