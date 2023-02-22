from django.contrib import admin

from .models import CD


class CDAdmin(admin.ModelAdmin):
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("title", "date", "artist", "genre",) 
    # добавляем интерфейс для поиска по тексту постов
    list_filter = ("date", "genre",)
    # это свойство сработает для всех колонок: где пусто - там будет эта строка
    empty_value_display = "-пусто-"

# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin
admin.site.register(CD, CDAdmin)
