from django.contrib import admin

from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")
    search_fields = ("name",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "description",
        "owner",
        "transaction_type",
        "amount",
        "transaction_date",
    )
    list_filter = ("transaction_type", "transaction_date")
    search_fields = ("description",)