from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from app.models import User, Question, Answer, Tag, QuestionLike, AnswerLike

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'answers_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'tags')
    search_fields = ('title', 'detailed')
    filter_horizontal = ('tags',)

    class AnswerInline(admin.TabularInline):
        model = Answer
        extra = 0
        fields = ('author', 'answer_text', 'rating', 'is_correct', 'is_active')
    
    inlines = (AnswerInline,)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'rating', 'is_correct', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_correct', 'created_at')
    search_fields = ('answer_text',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'value', 'created_at')
    list_filter = ('value', 'created_at')

@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer', 'value', 'created_at')
    list_filter = ('value', 'created_at')