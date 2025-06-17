from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:id>/<slug>/', views.question, name="question"),
    path('random-question', views.randomQuestion, name="randomQuestion"),
    path('search', views.search, name="search"),
    path('changelog', views.changelog, name="changelog"),
    path('stats', views.stats),
    path('infiniteScroll', views.infiniteScroll, name="infiniteScroll"),
    path('postQuestion', views.postQuestion, name="postQuestion"),
    path('postComment/<int:id>', views.postComment, name="postComment"),
]
