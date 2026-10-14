
from rest_framework import serializers


class AskQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(
        min_length=3,
        max_length=1000,
        trim_whitespace=True,
    )
