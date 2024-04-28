from django.contrib import admin
from .models import Movie, Category, Tag


admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'year', 'get_category')
    def get_category(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    get_category.short_description = 'Genres'

admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
