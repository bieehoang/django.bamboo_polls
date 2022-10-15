from django.urls import path
from . import views
# Create url for app
app_name = 'polls'
urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /polls/3
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'),
    #ex: /polls/3/results/
    path('<int:pk>/results/', views.ResultView.as_view(), name='results'),
    #ex: /polls/3/vote
    path('<int:question_id>/vote/', views.vote, name='vote'),
]