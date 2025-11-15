from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('hot/', views.HotQuestionsView.as_view(), name='hot'),
    path('tag/<str:tag>/', views.TagQuestionsView.as_view(), name='tag'),
    path('question/<int:question_id>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('ask/', views.AskView.as_view(), name='ask'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('member/<str:username>/', views.MemberQuestionsView.as_view(), name='member'),
]