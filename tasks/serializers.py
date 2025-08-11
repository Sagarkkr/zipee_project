from rest_framework import serializers
from .models import Task
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user
    
class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        source="owner",
        queryset=User.objects.all(),
        write_only=True
    )
    class Meta:
        model = Task
        fields = ["id", "title", "description", "completed", "created_at", "updated_at", "owner", "owner_id"]
        read_only_fields = ["id", "created_at", "updated_at", "owner"]
