from django.urls import path,re_path

from app.views import IndexView

urlpatterns = [
    path('', IndexView.as_view())

]