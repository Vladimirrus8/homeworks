from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Проверяем, что есть хотя бы один основной раздел
        main_count = 0
        for form in self.forms:
            if form.cleaned_data.get('DELETE'):
                continue

            if form.cleaned_data.get('is_main'):
                main_count += 1

        if main_count == 0:
            raise ValidationError('Укажите основной раздел')

        if main_count > 1:
            raise ValidationError('Основным может быть только один раздел')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1
    verbose_name = 'Раздел'
    verbose_name_plural = 'Разделы'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_at']
    list_filter = ['published_at']
    search_fields = ['title', 'text']
    inlines = [ScopeInline]
    save_on_top = True


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']