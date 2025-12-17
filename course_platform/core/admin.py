from django.contrib import admin
from .models import Category, Course, Lesson, Profile, Comment, Contact

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_class')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profession')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor', 'category', 'date_created')
    list_filter = ('category', 'tutor', 'date_created')
    search_fields = ('title', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'position')
    list_filter = ('course',)
    ordering = ('course', 'position')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'created_at')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('created_at',)
