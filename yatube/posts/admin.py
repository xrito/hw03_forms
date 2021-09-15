from django.contrib import admin

from .models import Group, Post


class PostAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',)
    list_editable = ('group',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


# class GroupAdmin(admin.ModelAdmin):
#     # prepopulated_fields = {"slug": ("title",)}


# При регистрации модели Post источником конфигурации для неё назначаем
# класс PostAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(Group)  # (Group, GroupAdmin)
