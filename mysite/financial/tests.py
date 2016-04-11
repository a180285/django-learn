#encoding:utf-8

from django.test import TestCase

# Create your tests here.
from .models import Account
from django.core.urlresolvers import reverse

class IndexViewTests(TestCase):
  def test_index_view(self):
    """
    If no questions exist, an appropriate message should be displayed.
    """
    response = self.client.get(reverse('financial:index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "账户管理")
    self.assertTemplateUsed(response, 'financial/index.html')

class AccountViewTests(TestCase):
  def check_template_used(self, response):
    template_name = 'financial/account.html'
    self.assertTemplateUsed(response, template_name)

  def test_with_no_account(self):
    response = self.client.get(reverse('financial:account'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['account_list'], [])
    self.check_template_used(response)

  def test_with_accounts(self):
    test_account_name = "test_account_name"
    test_account = Account.objects.create(name = test_account_name)
    response = self.client.get(reverse('financial:account'))
    self.assertEqual(response.status_code, 200)
    self.assertQuerysetEqual(response.context['account_list'], ['<Account: test_account_name>'])
    self.check_template_used(response)

# TODO: Add test for add_account
