
from rest_framework import serializers

from .models import Category, Transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "category",
            "category_name",
            "transaction_type",
            "amount",
            "description",
            "transaction_date",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "category_name"]

    def validate_category(self, category):
        request = self.context.get("request")

        if request and category.owner_id != request.user.id:
            raise serializers.ValidationError(
                "Cette catégorie ne vous appartient pas."
            )

        return category

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError(
                "Le montant doit être supérieur à zéro."
            )

        return amount
