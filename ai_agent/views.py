
import logging

from openai import OpenAI, APIError, APITimeoutError, RateLimitError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AskQuestionSerializer
from .services import ask_financial_assistant

logger = logging.getLogger(__name__)


class AskFinancialAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AskQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            answer = ask_financial_assistant(
                user=request.user,
                question=serializer.validated_data["question"],
            )
            return Response({"answer": answer})

        except (APITimeoutError, RateLimitError, APIError):
            logger.exception("AI provider request failed")
            return Response(
                {"error": "The AI service is temporarily unavailable."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except RuntimeError:
            logger.exception("AI assistant configuration error")
            return Response(
                {"error": "The AI assistant is not configured."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
