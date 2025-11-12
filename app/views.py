import math

from django.shortcuts import render
from django.views.generic import TemplateView

def index(request):
    print(request)


    return render(request, "app/index.html")

class IndexView(TemplateView):
    http_method_names = ['get']
    template_name = 'app/index.html'
    COUNT_FAKE_QUESTIONS = 30
    QUESTIONS_PER_PAGE = 4
    def get_fake_questions(self):
        return[{
            'id':i,
            'question_text': f'Fake question #{i}',
            'question_detail_text': 'Guys, i have troble with a moon park. Can\'t find th black-jack... ', 
        } for i in range(self.COUNT_FAKE_QUESTIONS)]
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        page = int(self.request.GET.get('page',1))
        context['page'] = page
        context['count_questions'] = self.COUNT_FAKE_QUESTIONS
        context['questions_per_page'] = self.QUESTIONS_PER_PAGE
        context['max_page'] = math.ceil(self.COUNT_FAKE_QUESTIONS / self.QUESTIONS_PER_PAGE)
        context['pages'] = [i for i in range(1,context['max_page'])]
        if page == 1:
            context['new_questions'] = self.get_fake_questions()[0:(page*self.QUESTIONS_PER_PAGE)]
        else:
            context['new_questions'] = self.get_fake_questions()[page*self.QUESTIONS_PER_PAGE:(page*self.QUESTIONS_PER_PAGE)+self.QUESTIONS_PER_PAGE]
        return context

    def dispatch(self, request, *args, **kwargs):
        print(request)
        return super(IndexView, self).dispatch(request, *args, **kwargs)
        

    
