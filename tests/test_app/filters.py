"""Filtros customizados para o MessageHandler do bot."""
from telegram.ext.filters import UpdateFilter

from .models import LostItem


class PendingLostItemFilter(UpdateFilter):
    """Permite apenas updates de usuários que têm um LostItem com is_complete=False."""

    def filter(self, update):
        if not update.effective_message or not getattr(update.effective_message, "text", None):
            return False
        if not update.effective_user:
            return False
        return LostItem.objects.filter(
            telegram_user_id=update.effective_user.id,
            is_complete=False,
        ).exists()
