from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = ["id", "username", "movie", "rating", "comment", "created_at", "updated_at"]
        read_only_fields = ["movie"]

    def validate_rating(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Rating must be between 1 and 10.")
        return value
