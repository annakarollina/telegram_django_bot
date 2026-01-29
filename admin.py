from django.contrib import admin

from .models import TelegramUser, TeleDeepLink, ActionLog, Trigger, UserTrigger, BotMenuElem, BotMenuElemAttrText
from .admin_utils import CustomRelatedOnlyDropdownFilter, DefaultOverrideAdminWidgetsForm


class TelegramUserAdmin(admin.ModelAdmin):
    """Base admin para modelos que herdam de TelegramUser. Não registra TelegramUser (é abstrato)."""
    list_display = ('id', 'first_name', 'last_name', 'username', 'telegram_username', 'is_active', 'date_joined')
    search_fields = ('first_name', 'last_name', 'username', 'telegram_username')
    list_filter = ('is_active', 'date_joined')


@admin.register(TeleDeepLink)
class TeleDeepLinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'link', 'count_users')
    search_fields = ('title', 'link')

    def get_queryset(self, request):
        qs = super(TeleDeepLinkAdmin, self).get_queryset(request)
        return qs.annotate(
            c_users=Count('users')
        )

    def count_users(self, inst):
        return inst.c_users

    count_users.admin_order_field = 'c_users'

    def count_activated(self, inst):
        return inst.ca_users

    count_activated.admin_order_field = 'ca_users'



class BotMenuElemAdminForm(DefaultOverrideAdminWidgetsForm):
    list_json_fields = ['buttons_db', 'callbacks_db', ]


@admin.register(BotMenuElem)
class BotMenuElemAdmin(admin.ModelAdmin):
    list_display = ('id', 'message', 'is_visable', 'callbacks_db')
    search_fields = ('command', 'callbacks_db', 'message', 'buttons_db',)
    list_filter = ('is_visable', 'empty_block')
    form = BotMenuElemAdminForm


@admin.register(BotMenuElemAttrText)
class BotMenuElemAttrTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'dttm_added', 'language_code', 'default_text', 'translated_text')
    search_fields = ('default_text', 'translated_text')
    list_filter = ('language_code', 'bot_menu_elem')


class TriggerAdminForm(DefaultOverrideAdminWidgetsForm):
    json_fields = ['condition_db',]


@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'min_duration', 'priority', 'botmenuelem_id')
    search_fields = ('name', 'condition_db')
    form = TriggerAdminForm


@admin.register(UserTrigger)
class UserTriggerAdmin(admin.ModelAdmin):
    list_display = ('id', 'dttm_added', 'trigger_id', 'user_id', 'is_sent')
    list_filter = ('trigger', 'is_sent')
