from django.db import models
from django.contrib.auth import get_user_model
import ulid

class ItemModel(models.Model):
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True, editable=False)
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    
    class Meta:
        db_table = "item"


class UserFavoriteItemModel(models.Model):
    id = models.CharField(max_length=32, default=ulid.new, primary_key=True, editable=False)
    item = models.ForeignKey(ItemModel, db_column="item_id", on_delete=models.CASCADE, null=False, blank=False)
    user = models.ForeignKey(get_user_model(), db_column="user_id", on_delete=models.CASCADE, null=False, blank=False)
    
    class Meta:
        db_table = "user_favorite_item"