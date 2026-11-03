from rest_framework import serializers
from restaurant.models import Dish, Category


class DishSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Dish
        fields = ["id", "name", "description", "price", "available", "category", "category_name"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]