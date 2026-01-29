from django.contrib import admin
from telegram_django_bot.admin import TelegramUserAdmin as CustomUserAdmin
from .models import Category, Entity, User, Size, LostItem
from django.db.models import Count, Q


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_user_id', 'is_complete', 'description_preview')
    list_filter = ('is_complete',)

    def description_preview(self, obj):
        return (obj.description[:50] + '...') if obj.description and len(obj.description) > 50 else (obj.description or '-')

    description_preview.short_description = 'Descrição'


@admin.register(User)
class UserAdmin(CustomUserAdmin, admin.ModelAdmin):
    pass
