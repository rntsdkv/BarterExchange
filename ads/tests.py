from unittest import mock
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse, path
from ads.models import Ad, AdCategory, AdCondition, ExchangeProposal, StatusChoices, AdStatus
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ad/<int:id>/edit/', views.ad_edit, name='ad_edit'),
    path('ad/<int:id>/delete/', views.ad_delete, name='ad_delete'),
    path('ad/<int:id>/exchange/', views.ad_exсhange, name='ad_exchange'),
    path('exchange/<int:id>/update', views.exchange_update, name='exchange_update'),
]

class AdViewTest(TestCase):
    def setUp(self):
        self.ad = Ad.objects.create(
            title="Test Ad",
            description="Test description",
            user=User.objects.create(username="testuser"),
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )

    def test_ad_view_returns_200(self):
        response = self.client.get(reverse('ad', args=[self.ad.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Ad")
        self.assertContains(response, "Test description")
        self.assertContains(response, "testuser")
        self.assertContains(response, "testcategory")
        self.assertContains(response, "new")

    def test_ad_view_returns_404_for_invalid_id(self):
        response = self.client.get(reverse('ad', args=[999]))
        self.assertEqual(response.status_code, 404)

class AdCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.category = AdCategory.objects.create(title="testcategory")
        self.condition = AdCondition.NEW
        self.url = reverse("new_ad")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth'))

    def test_new_ad_get_request_renders_form(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_new_ad_post_invalid_data(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertEqual(Ad.objects.count(), 0)

    # @mock.patch('django.middleware.csrf.get_token')
    # def test_new_ad_post_valid_data_creates_ad(self, mock_get_token):
    #     mock_get_token.return_value = 'dummy_csrf_token'
    #     self.client.login(username="testuser", password="testpassword")
    #     image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
    #
    #     form_data = {
    #         'title': 'Test Ad',
    #         'description': 'Test description',
    #         'image': image,
    #         'category': self.category.id,
    #         'condition': "new"
    #     }
    #
    #     response = self.client.post(
    #         self.url,
    #         form_data,
    #         follow=True,
    #         content_type='multipart/form-data'
    #     )
    #
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(Ad.objects.count(), 1)
    #     self.assertEqual(Ad.objects.first().title, 'Test Ad')

class AdEditTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        self.ad = Ad.objects.create(
            title="Test Ad",
            description="Test description",
            user=self.user,
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.url = reverse('ad_edit', args=[self.ad.id])

    def test_ad_edit_get_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('auth'))

    def test_ad_edit_if_not_exists(self):
        response = self.client.get(reverse('ad_edit', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_ad_edit_post_if_user_dont_have_ad(self):
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(self.url, data={
            'title': 'Test Ad 2',
            'description': 'Test description',
            'category': AdCategory.objects.create(title="testcategory").id,
            'condition': "new"
        })
        self.assertEqual(Ad.objects.first().title, "Test Ad")
        self.assertEqual(response.status_code, 302)

    def test_ad_edit_post_invalid_data(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, data={
            'title': 'Test Ad',
            'description': '',
            'category': AdCategory.objects.create(title="testcategory").id,
            'condition': "new"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')

    def test_ad_edit_post_returns_302(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url, data={
            'title': 'Test Ad 2',
            'description': 'Test description 2',
            'category': AdCategory.objects.create(title="testcategory").id,
            'condition': "used"
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('ad', args=[self.ad.id]))

class AdDeleteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        self.ad = Ad.objects.create(
            title="Test Ad",
            description="Test description",
            user=self.user,
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.url = reverse('ad_delete', args=[self.ad.id])

    def test_ad_delete_get_returns_302(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 1)

    def test_ad_edit_if_not_exists(self):
        response = self.client.get(reverse('ad_edit', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('auth'))

    def test_ad_delete_if_user_dont_have_ad(self):
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(self.url)
        self.assertEqual(Ad.objects.count(), 1)
        self.assertRedirects(response, reverse('no_access'))

    def test_ad_delete_returns_302(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.url)
        self.assertEqual(Ad.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

class AdSearchTest(TestCase):
    def setUp(self):
        self.ad1 = Ad.objects.create(
            title="Test Ad 1",
            description="Test description",
            user=User.objects.create_user(username="testuser1", password="testpassword1"),
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.ad2 = Ad.objects.create(
            title="Test Ad 2",
            description="Test description",
            user=User.objects.create_user(username="testuser2", password="testpassword2"),
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.ad3 = Ad.objects.create(
            title="Test Ad 3",
            description="Test description",
            user=User.objects.create_user(username="testuser3", password="testpassword3"),
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )

    def test_ad_search_none_query_returns_all(self):
        response = self.client.get(reverse('search'))
        self.assertContains(response, 'Test Ad 1')
        response = self.client.get(f'{reverse("search")}?page=2')
        self.assertContains(response, 'Test Ad 2')
        response = self.client.get(f'{reverse("search")}?page=3')
        self.assertContains(response, 'Test Ad 3')

    def test_ad_search_first_ad(self):
        response = self.client.get(f'{reverse("search")}?search=Ad 1')
        self.assertContains(response, 'Test Ad 1')
        self.assertContains(response, 'Страница 1 из 1')

    def test_ad_search_not_exists(self):
        response = self.client.get(f'{reverse("search")}?search=A1')
        self.assertContains(response, 'Нет объявлений')


class ProposalCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        self.ad1 = Ad.objects.create(
            title="Test Ad User 1",
            description="Test description",
            user=self.user,
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.ad2 = Ad.objects.create(
            title="Test Ad User 2",
            description="Test description",
            user=self.user2,
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.ad3 = Ad.objects.create(
            title="Test Ad 2 User 1",
            description="Test description",
            user=self.user,
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.url = reverse('ad_exchange', args=[self.ad1.id])

    def test_proposal_create_get_returns_302(self):
        response = self.client.get(f'{self.url}?selected={self.ad2.id}')
        self.assertEqual(response.status_code, 302)

    def test_proposal_create_if_user_is_not_authorized(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('auth'))

    def test_proposal_create_ad_is_not_exists(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(f'{reverse("ad_exchange", args=[999])}?selected=1')
        self.assertEqual(ExchangeProposal.objects.count(), 0)
        self.assertEqual(response.status_code, 404)

    def test_proposal_create_selected_ad_is_not_exists(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(f'{self.url}?selected=999')
        self.assertEqual(ExchangeProposal.objects.count(), 0)
        self.assertEqual(response.status_code, 404)

    def test_proposal_create_selected_ad_is_not_digit(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(f'{self.url}?selected=test')
        self.assertEqual(ExchangeProposal.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_proposal_create_if_user_dont_have_access(self):
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(f'{self.url}?selected=3')
        self.assertEqual(ExchangeProposal.objects.count(), 0)
        self.assertRedirects(response, reverse('no_access'))

    def test_proposal_create_if_user_exchanges_himself(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(f'{self.url}?selected=3')
        self.assertEqual(ExchangeProposal.objects.count(), 0)
        self.assertEqual(response.status_code, 302)

    def test_proposal_create_if_proposal_exists(self):
        ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='test comment'
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(f'{self.url}?selected=2')
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_proposal_create_returns_302(self):
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(f'{self.url}?selected=2&comment=test')
        self.assertEqual(ExchangeProposal.objects.count(), 1)
        self.assertEqual(response.status_code, 302)

class ProposalUpdateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.user2 = User.objects.create_user(username="testuser2", password="testpassword2")
        self.user3 = User.objects.create_user(username="testuser3", password="testpassword3")
        self.ad1 = Ad.objects.create(
            title="Test Ad User 1",
            description="Test description",
            user=self.user,
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.ad2 = Ad.objects.create(
            title="Test Ad User 2",
            description="Test description",
            user=self.user2,
            image="test image",
            category=AdCategory.objects.create(title="testcategory"),
            condition=AdCondition.NEW
        )
        self.proposal = ExchangeProposal.objects.create(
            ad_sender=self.ad1,
            ad_receiver=self.ad2,
            comment='test comment'
        )
        self.url = reverse('exchange_update', args=[self.proposal.id])

    def test_proposal_update_get_returns_302(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_proposal_update_if_not_exists(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(f'{reverse("exchange_update", args=[999])}?action=reject')
        self.assertEqual(response.status_code, 404)

    def test_proposal_update_if_user_is_not_authorized(self):
        response = self.client.post(f'{self.url}?action=reject')
        self.assertRedirects(response, reverse('auth'))

    def test_proposal_update_if_proposal_not_pending(self):
        self.client.login(username="testuser", password="testpassword")
        self.proposal.status = StatusChoices.REJECTED
        response = self.client.post(f'{self.url}?action=accept')
        self.assertEqual(self.proposal.status, StatusChoices.REJECTED)
        self.assertEqual(response.status_code, 302)

    def test_proposal_update_if_ads_not_active(self):
        self.client.login(username="testuser", password="testpassword")
        self.ad1.status = AdStatus.EXCHANGED
        self.ad1.save()
        response = self.client.post(f'{self.url}?action=accept')
        self.assertRedirects(response, reverse('no_access'))

    def test_proposal_update_if_user_have_no_access(self):
        self.client.login(username="testuser3", password="testpassword3")
        self.proposal.status = StatusChoices.PENDING
        self.ad1.status = AdStatus.ACTIVE
        response = self.client.post(f'{self.url}?action=accept')
        self.assertEqual(self.proposal.status, StatusChoices.PENDING)
        self.assertRedirects(response, reverse('no_access'))

    def test_proposal_update_user_created_proposal(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(f'{self.url}?action=accept')
        self.assertEqual(self.proposal.status, StatusChoices.PENDING)
        self.assertRedirects(response, reverse('no_access'))

    def test_proposal_update_valid_returns_302(self):
        self.client.login(username="testuser2", password="testpassword2")
        response = self.client.post(f'{self.url}?action=accept')
        self.proposal.refresh_from_db()
        self.ad1.refresh_from_db()
        self.ad2.refresh_from_db()
        self.assertEqual(self.proposal.status, StatusChoices.ACCEPTED)
        self.assertEqual(self.ad1.status, AdStatus.EXCHANGED)
        self.assertEqual(self.ad2.status, AdStatus.EXCHANGED)
        self.assertEqual(response.status_code, 302)