import math
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import TemplateView

def paginate(objects_list, request, per_page=10):
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
    COUNT_FAKE_QUESTIONS = 30
    QUESTIONS_PER_PAGE = 4
    
    def get_fake_questions(self):
        return [{
            'id': i,
            'question_text': f'Fake question #{i}',
            'question_detail_text': 'Guys, i have trouble with a moon park. Can\'t find the black-jack...',
        } for i in range(1, self.COUNT_FAKE_QUESTIONS + 1)]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.get_fake_questions()
        page_obj = paginate(questions, self.request, self.QUESTIONS_PER_PAGE)
        page = int(self.request.GET.get('page', 1))
        context['page'] = page
        context['count_questions'] = self.COUNT_FAKE_QUESTIONS
        context['questions_per_page'] = self.QUESTIONS_PER_PAGE
        context['max_page'] = math.ceil(self.COUNT_FAKE_QUESTIONS / self.QUESTIONS_PER_PAGE)
        context['pages'] = [i for i in range(1, context['max_page'] + 1)]
        
        if page == 1:
            context['new_questions'] = questions[0:(page * self.QUESTIONS_PER_PAGE)]
        else:
            start_index = (page - 1) * self.QUESTIONS_PER_PAGE
            end_index = start_index + self.QUESTIONS_PER_PAGE
            context['new_questions'] = questions[start_index:end_index]
        
        return context

class HotQuestionsView(TemplateView):
    template_name = 'app/hot_questions.html'
    COUNT_FAKE_QUESTIONS = 25
    QUESTIONS_PER_PAGE = 4
    
    def get_fake_questions(self):
        return [{
            'id': i,
            'question_text': f'Hot question #{i}',
            'question_detail_text': 'This is a popular question with many votes...',
        } for i in range(1, self.COUNT_FAKE_QUESTIONS + 1)]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = self.get_fake_questions()
        
        page = int(self.request.GET.get('page', 1))
        context['page'] = page
        context['count_questions'] = self.COUNT_FAKE_QUESTIONS
        context['questions_per_page'] = self.QUESTIONS_PER_PAGE
        context['max_page'] = math.ceil(self.COUNT_FAKE_QUESTIONS / self.QUESTIONS_PER_PAGE)
        context['pages'] = [i for i in range(1, context['max_page'] + 1)]
        
        if page == 1:
            context['questions'] = questions[0:(page * self.QUESTIONS_PER_PAGE)]
        else:
            start_index = (page - 1) * self.QUESTIONS_PER_PAGE
            end_index = start_index + self.QUESTIONS_PER_PAGE
            context['questions'] = questions[start_index:end_index]
        
        return context

class TagQuestionsView(TemplateView):
    template_name = 'app/tag_questions.html'
    QUESTIONS_PER_PAGE = 4
    
    def get_fake_questions(self, tag):
        return [{
            'id': i,
            'question_text': f'Question about {tag} #{i}',
            'question_detail_text': f'This question is related to {tag} tag...',
        } for i in range(1, 16)]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = self.kwargs.get('tag', '')
        questions = self.get_fake_questions(tag)
        
        page = int(self.request.GET.get('page', 1))
        context['tag'] = tag
        context['count_questions'] = len(questions)
        context['questions_per_page'] = self.QUESTIONS_PER_PAGE
        context['max_page'] = math.ceil(len(questions) / self.QUESTIONS_PER_PAGE)
        context['pages'] = [i for i in range(1, context['max_page'] + 1)]
        
        if page == 1:
            context['questions'] = questions[0:(page * self.QUESTIONS_PER_PAGE)]
        else:
            start_index = (page - 1) * self.QUESTIONS_PER_PAGE
            end_index = start_index + self.QUESTIONS_PER_PAGE
            context['questions'] = questions[start_index:end_index]
        
        return context

class QuestionDetailView(TemplateView):
    template_name = 'app/question.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = self.kwargs.get('question_id')
        
        question = {
            'id': question_id,
            'title': 'How to build a moon park?',
            'text': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Suscipit magni cum quos deserunt neque, ea dolorum natus facilis magnam inventore sequi beatae, nam velit exercitationem quisquam illo laboriosam veniam doloremque! Lorem ipsum dolor sit amet consectetur adipisicing elit.',
        }
        
        answers = [{
            'id': i,
            'text': f'This is answer #{i} to the question.',
            'is_correct': i == 1,
        } for i in range(1, 4)]
        
        context.update({
            'question': question,
            'answers': answers,
        })
        return context

class LoginView(TemplateView):
    template_name = 'app/login.html'

class SignupView(TemplateView):
    template_name = 'app/signup.html'

class AskView(TemplateView):
    template_name = 'app/ask.html'

class SettingsView(TemplateView):
    template_name = 'app/settings.html'