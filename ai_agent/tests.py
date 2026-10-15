
from datetime import date
from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from finance.models import Category, Transaction
from .services import get_financial_context

User = get_user_model()


class AskFinancialAssistantTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            password="test-password-123",
        )
        self.other_user = User.objects.create_user(
            username="user2",
            password="test-password-456",
        )

        self.category = Category.objects.create(
            owner=self.user,
            name="Salaire",
        )
        self.other_category = Category.objects.create(
            owner=self.other_user,
            name="Transport",
        )

        Transaction.objects.create(
            owner=self.user,
            category=self.category,
            transaction_type="income",
            amount="200000.00",
            description="Salaire",
            transaction_date=date(2026, 10, 1),
        )

        Transaction.objects.create(
            owner=self.other_user,
            category=self.other_category,
            transaction_type="expense",
            amount="50000.00",
            description="Transport privé",
            transaction_date=date(2026, 10, 2),
        )

        self.url = "/api/ai-agent/ask/"

    def test_unauthenticated_user_is_rejected(self):
        response = self.client.post(
            self.url,
            {"question": "Quel est mon solde ?"},
            format="json",
        )

        self.assertIn(response.status_code, [401, 403])

    @patch("ai_agent.views.ask_financial_assistant")
    def test_authenticated_user_can_ask_question(self, mock_ask):
        mock_ask.return_value = "Vos revenus sont de 200000."

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            self.url,
            {"question": "Quels sont mes revenus ?"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["answer"],
            "Vos revenus sont de 200000.",
        )
        mock_ask.assert_called_once_with(
            user=self.user,
            question="Quels sont mes revenus ?",
        )

    @patch("ai_agent.views.ask_financial_assistant")
    def test_invalid_question_does_not_call_ai(self, mock_ask):
        self.client.force_authenticate(user=self.user)

        for question in ["", "x" * 1001]:
            with self.subTest(question_length=len(question)):
                response = self.client.post(
                    self.url,
                    {"question": question},
                    format="json",
                )

                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST,
                )

        mock_ask.assert_not_called()

    def test_financial_context_contains_only_own_transactions(self):
        context = get_financial_context(self.user)

        self.assertEqual(context["total_income"], "200000.00")
        self.assertEqual(context["total_expenses"], "0.00")
        self.assertEqual(context["balance"], "200000.00")

        descriptions = [
            transaction["description"]
            for transaction in context["recent_transactions"]
        ]

        self.assertIn("Salaire", descriptions)
        self.assertNotIn("Transport privé", descriptions)
