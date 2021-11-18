from rest_framework.views import APIView, set_rollback
from rest_framework.response import Response
from rest_framework import status

from my_app.models import UserFavoriteItemModel, ItemModel
from my_app.serializers.user_favorite_item import UserFavoriteItemSerializer 
from django.contrib.auth import get_user_model


class UserFavoriteItemAPIView(APIView):
    
    def get(self, request):
        '''
        データ取得
        '''
        # ログインユーザーでフィルター
        seliarizer = UserFavoriteItemSerializer(UserFavoriteItemModel.objects.filter(user=request.user), many=True)
        return Response(seliarizer.data)
    
    
    def post(self, request):
        '''
        データ登録
        '''
        item = ItemModel.objects.filter(id=request.data.get("item_id")).first()
        if not item:
            return Response({"detail": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)
        results = UserFavoriteItemModel.objects.get_or_create(
                user = request.user, 
                item = item
            )
        seliarizer = UserFavoriteItemSerializer(results[0])
        return Response(seliarizer.data)
    
