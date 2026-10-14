
from django.urls import path

from .views import AskFinancialAssistantView

urlpatterns = [
    path("ask/", AskFinancialAssistantView.as_view(), name="ai-ask"),
]
