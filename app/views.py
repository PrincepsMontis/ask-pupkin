import math
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.db.models import Count

from app.models import Question, Tag, Answer, User

def paginate(objects_list, request, per_page=20):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return page_obj

class IndexView(TemplateView):
    template_name = 'app/index.html'
    QUESTIONS_PER_PAGE = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        new_questions = Question.objects.new_questions()
        page_obj = paginate(new_questions, self.request, self.QUESTIONS_PER_PAGE)
        
        context.update({
            'new_questions': page_obj,
            'pages': range(1, page_obj.paginator.num_pages + 1),
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
            'page_obj': page_obj,
        })
        return context

class HotQuestionsView(TemplateView):
    template_name = 'app/hot_questions.html'
    QUESTIONS_PER_PAGE = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        hot_questions = Question.objects.hot_questions()
        page_obj = paginate(hot_questions, self.request, self.QUESTIONS_PER_PAGE)
        
        context.update({
            'questions': page_obj,
            'pages': range(1, page_obj.paginator.num_pages + 1),
            'page_obj': page_obj,
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
        })
        return context

class TagQuestionsView(TemplateView):
    template_name = 'app/tag_questions.html'
    QUESTIONS_PER_PAGE = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs.get('tag')
        
        tag = get_object_or_404(Tag, title=tag_name)
        questions = Question.objects.by_tag(tag_name)
        page_obj = paginate(questions, self.request, self.QUESTIONS_PER_PAGE)
        
        context.update({
            'tag': tag_name,
            'questions': page_obj,
            'pages': range(1, page_obj.paginator.num_pages + 1),
            'page_obj': page_obj,
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
        })
        return context

class QuestionDetailView(TemplateView):
    template_name = 'app/question.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs.get('question_id')
        
        question = get_object_or_404(Question, id=question_id)
        answers = question.answers.all()
        
        context.update({
            'question': question,
            'answers': answers,
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
        })
        return context

class LoginView(TemplateView):
    template_name = 'app/login.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
        })
        return context

class SignupView(TemplateView):
    template_name = 'app/signup.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
        })
        return context

class AskView(TemplateView):
    template_name = 'app/ask.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
        })
        return context

class SettingsView(TemplateView):
    template_name = 'app/settings.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
        })
        return context
class MemberQuestionsView(TemplateView):
    template_name = 'app/member_questions.html'
    QUESTIONS_PER_PAGE = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        

        member = get_object_or_404(User, username=username)
        

        member_questions = Question.objects.filter(author=member, is_active=True)
        page_obj = paginate(member_questions, self.request, self.QUESTIONS_PER_PAGE)
        
        context.update({
            'member': member,
            'questions': page_obj,
            'pages': range(1, page_obj.paginator.num_pages + 1),
            'page_obj': page_obj,
            'tags': Tag.objects.popular_tags(),
            'best_members': User.objects.best_members(),
        })
        return context