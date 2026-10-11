from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="finance_categories",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_category_name_per_owner",
            )
        ]

    def __str__(self):
        return self.name


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        INCOME = "income", "Revenu"
        EXPENSE = "expense", "Dépense"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="finance_transactions",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices,
    )
    amount = models.DecimalField(
        max_digits=14,
        decimal_places=2,
    )
    description = models.CharField(max_length=255)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-transaction_date", "-id"]
        indexes = [
            models.Index(
                fields=["owner", "transaction_date"],
                name="transaction_owner_date_idx",
            ),
        ]

    def __str__(self):
        return f"{self.description} - {self.amount}"
