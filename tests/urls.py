from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),

    # path('', include(('telegram_bot.urls', 'base'), namespace='main')),

]