from rest_framework import serializers
from django.contrib.auth import get_user_model
from savings.models import UserSaving, Recommendation
from articles.models import Question

User = get_user_model()

class UserWithSavingSerializer(serializers.ModelSerializer):
    usersaving_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)


class UserwithQuestionSerializer(serializers.ModelSerializer):
    question_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id',)