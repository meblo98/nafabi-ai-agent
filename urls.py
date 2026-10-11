
from django.urls import path

from .views import (
    CategoryListCreateView,
    TransactionListCreateView,
    TransactionSummaryView,
)

urlpatterns = [
    path("categories/", CategoryListCreateView.as_view(), name="category-list"),
    path("transactions/", TransactionListCreateView.as_view(), name="transaction-list"),
    path(
        "transactions/summary/",
        TransactionSummaryView.as_view(),
        name="transaction-summary",
    ),
]
