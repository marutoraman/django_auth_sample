from rest_framework import serializers
from ..models import UserFavoriteItemModel


class UserFavoriteItemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserFavoriteItemModel
        fields = ('id', 'user', 'item')