from rest_framework import serializers
from apps.main.models import Feedback, Product, ProductImage


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "name",
            "phone",
            "product_name",
            "link",
        ]


class ProductSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField("get_link")
    manufacturer_name = serializers.SerializerMethodField("get_manufacturer_name")
    collection_name = serializers.SerializerMethodField("get_collection_name")
    category = serializers.SerializerMethodField("get_category_name")

    def get_link(self, product):
        request = self.context.get("request")
        return request.build_absolute_uri(product.get_absolute_url())

    def get_manufacturer_name(self, product):
        return product.manufacturer.name

    def get_category_name(self, product):
        return product.category.name

    def get_collection_name(self, product):
        if product.collection:
            return product.collection.name
        else:
            return None

    class Meta:
        model = Product
        fields = [
            "name",
            "manufacturer_name",
            "collection_name",
            "mainImage",
            "category",
            "link",
            "slug",
        ]


class ImageSerializer(serializers.ModelSerializer):
    def get_link(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url)

    class Meta:
        model = ProductImage
        fields = [
            "image",
        ]
