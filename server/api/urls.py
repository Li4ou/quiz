from api import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('quiz', views.QuizViewSet, basename='test')


from django.urls import path
urlpatterns = [
    path('quiz/', views.QuizViewSet.as_view()),
    path('quiz/questions/<int:pk>', views.QuestionsView.as_view()),
    path('result/', views.ResultsAPIView.as_view()),
    path('nagrady/', views.NagradyAPIView.as_view())
]
#
