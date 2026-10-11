from django.test import TestCase

# Create your tests here.

from datetime import date
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from finance.models import Category, Transaction

User = get_user_model()


class TransactionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="test-password",
        )
        self.category = Category.objects.create(
            owner=self.user,
            name="Transport",
        )

    def test_create_expense(self):
        transaction = Transaction.objects.create(
            owner=self.user,
            category=self.category,
            transaction_type=Transaction.TransactionType.EXPENSE,
            amount=Decimal("1500.00"),
            description="Taxi",
            transaction_date=date(2026, 10, 11),
        )

        self.assertEqual(transaction.amount, Decimal("1500.00"))
        self.assertEqual(transaction.owner, self.user)

    def test_category_name_is_unique_per_owner(self):
        from django.db import IntegrityError, transaction

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Category.objects.create(
                    owner=self.user,
                    name="Transport",
                )
