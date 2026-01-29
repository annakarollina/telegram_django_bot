import os
import uuid

from django.conf import settings
from django.utils.translation import gettext as _

from telegram_django_bot.utils import handler_decor
from telegram_django_bot.telegram_lib_redefinition import (
    InlineKeyboardMarkupDJ as inlinemark,
    InlineKeyboardButtonDJ as inlinebutt
)

from .models import LostItem


@handler_decor()
def handle_lost_item_photo(bot, update, user):
    """Recebe uma foto, baixa, cria LostItem com is_complete=False e pede a descrição."""
    photo = update.message.photo[-1]
    file = bot.get_file(photo.file_id)
    upload_dir = os.path.join(settings.MEDIA_ROOT, "lost_items")
    os.makedirs(upload_dir, exist_ok=True)
    ext = "jpg"
    filename = f"{uuid.uuid4().hex}.{ext}"
    local_path = os.path.join(upload_dir, filename)
    file.download(local_path)
    relative_path = os.path.join("lost_items", filename)
    LostItem.objects.create(
        image=relative_path,
        telegram_user_id=user.id,
        description="",
        is_complete=False,
    )
    return bot.send_message(
        user.id,
        _("Envie a descrição do item."),
    )


@handler_decor()
def handle_lost_item_description(bot, update, user):
    """Se o usuário tem LostItem pendente, salva o texto como descrição e marca is_complete=True."""
    pending = LostItem.objects.filter(
        telegram_user_id=user.id,
        is_complete=False,
    ).order_by("-id").first()
    if not pending:
        return None
    pending.description = update.message.text
    pending.is_complete = True
    pending.save()
    return bot.send_message(
        user.id,
        _("Item registrado com sucesso."),
    )


@handler_decor()
def me(bot, update, user):
    return bot.send_message(
        user.id,
        f"{user}",
        reply_markup=inlinemark([[
            inlinebutt(text=_('create category'), callback_data='cat/cr'),
            inlinebutt(text=_('create entity'), callback_data='ent/cr'),
            inlinebutt(text=_('user'), callback_data='us/se')
        ]])
    )


