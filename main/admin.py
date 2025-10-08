from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline
from unfold.admin import TabularInline
from unfold.contrib.filters.admin import ChoicesDropdownFilter
from unfold.contrib.filters.admin import MultipleRelatedDropdownFilter
from unfold.contrib.filters.admin import RangeNumericFilter
from unfold.contrib.filters.admin import RelatedDropdownFilter
from unfold.contrib.filters.admin import BooleanRadioFilter
from unfold.decorators import display

from .forms import ProductForm
from .models import Address
from .models import Category
from .models import Collection
from .models import Feedback
from .models import Manufacturer
from .models import Phone
from .models import Product
from .models import ProductImage
from .models import Specs


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = [
        "display_header",
        "is_staff",
        "is_active",
        "is_superuser",
        "date_joined",
        "last_login",
    ]
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = ["last_login", "date_joined"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    ("first_name", "last_name"),
                    "email",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    search_fields = ["first_name", "last_name", "email", "username"]
    list_filter = ["is_active", "is_staff", "is_superuser"]

    @display(description=_("User"), header=True)
    def display_header(self, instance: User):
        return instance.get_full_name() or f"@{instance.username}", instance.email


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


class ImageInline(StackedInline):
    model = ProductImage
    extra = 0
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = "Предпросмотр обложки"
    image_preview.allow_tags = True


class SpecsInline(TabularInline):
    model = Specs
    extra = 0
    tab = True


@admin.register(Manufacturer)
class ManufacturerAdmin(ModelAdmin):
    readonly_fields = ("slug",)


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    pass


@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    fields = (
        "name",
        "phone",
        "product",
        "date",
    )
    readonly_fields = ("phone", "product")

    list_display = (
        "display_header",
        "link",
        "date",
    )

    @display(description=_("Заголовок"), header=True)
    def display_header(self, instance: Feedback):
        return [
            instance.name,
            instance.phone,
        ]


@admin.register(Phone)
class PhoneAdmin(ModelAdmin):
    list_display = ("phone",)
    list_display_links = ("phone",)


@admin.register(Collection)
class CollectionAdmin(ModelAdmin):
    list_display = ("name", "slug", "manufacturer")
    list_display_links = ("name",)
    search_fields = (
        "name",
        "manufacturer",
    )
    list_filter = ("manufacturer__name",)
    readonly_fields = ("slug",)
    filter_horizontal = ("category",)


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name", "slug", "number", "isCabinet")
    list_display_links = ("name",)
    list_editable = ("number", "isCabinet")
    readonly_fields = ("slug",)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    form = ProductForm
    search_fields = (
        "name",
    )
    list_editable = ("rating", "isOnSale", "price")
    list_filter = (
        ("manufacturer", RelatedDropdownFilter),
        ("category", MultipleRelatedDropdownFilter),
        ("collection", MultipleRelatedDropdownFilter),
        ("isOnSale", ChoicesDropdownFilter),
        ("rating", RangeNumericFilter),
    )
    filter_horizontal = ("collectionCategory",)
    readonly_fields = (
        "id",
        "slug",
        "date",
    )

    inlines = [ImageInline, SpecsInline]

    list_display = (
        "display_header",
        "manufacturer",
        "category",
        "isOnSale",
        "price",
        "rating",
    )

    list_filter_sheet = False
    list_filter_submit = True

    @display(description=_("Название"), header=True)
    def display_header(self, instance: Product):
        return [
            instance.name,
            instance.collection,
            None,
            {
                "path": instance.mainImage.url,
            },
        ]

    def save_related(self, request, form, formsets, change):
        try:
            super().save_related(request, form, formsets, change)
        except ValidationError as e:
            # Перехватываем ошибку валидации и показываем её в интерфейсе
            self.message_user(request, f"Ошибка: {e.message}", level=messages.ERROR)
