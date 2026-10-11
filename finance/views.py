from django.shortcuts import render

# Create your views here.

from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.db.models import DecimalField
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Transaction
from .serializers import CategorySerializer, TransactionSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(
            owner=self.request.user
        ).select_related("category")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionSummaryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(
            owner=request.user
        )

        money_field = DecimalField(
            max_digits=14,
            decimal_places=2,
        )

        totals = transactions.aggregate(
            income=Coalesce(
                Sum(
                    "amount",
                    filter=__import__(
                        "django.db.models", fromlist=["Q"]
                    ).Q(transaction_type="income"),
                ),
                0,
                output_field=money_field,
            ),
            expenses=Coalesce(
                Sum(
                    "amount",
                    filter=__import__(
                        "django.db.models", fromlist=["Q"]
                    ).Q(transaction_type="expense"),
                ),
                0,
                output_field=money_field,
            ),
        )

        income = totals["income"]
        expenses = totals["expenses"]

        return Response({
            "total_income": str(income),
            "total_expenses": str(expenses),
            "balance": str(income - expenses),
        })
