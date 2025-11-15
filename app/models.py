from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count

class DefaultModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

class UserManager(DjangoUserManager):
    def best_members(self):
        """Лучшие пользователи по количеству вопросов и ответов"""
        return self.annotate(
            total_contributions=Count('question') + Count('answer')
        ).order_by('-total_contributions')[:10]

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class TagManager(models.Manager):
    def popular_tags(self):
        """Популярные теги по количеству вопросов"""
        return self.annotate(
            question_count=Count('question')
        ).order_by('-question_count')[:10]

class Tag(DefaultModel):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
    
    title = models.CharField(max_length=200, verbose_name="Название тега")
    
    objects = TagManager()

    def __str__(self):
        return self.title

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.filter(is_active=True).order_by('-created_at')
    
    def hot_questions(self):
        return self.filter(is_active=True).order_by('-rating')
    
    def by_tag(self, tag_name):
        return self.filter(is_active=True, tags__title=tag_name)

class Question(DefaultModel):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
    
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    detailed = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")
    rating = models.IntegerField(default=0)
    votes_count = models.IntegerField(default=0)
    answers_count = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super(Question, self).save(*args, **kwargs)

class Answer(DefaultModel):
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()
    rating = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Ответ на вопрос: {self.question.title}"

class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'question']
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'

class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    value = models.SmallIntegerField(validators=[MinValueValidator(-1), MaxValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'answer']
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'