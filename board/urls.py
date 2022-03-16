from django.urls import path
from board.views import BoardView

urlpatterns = [
    path('posting/', BoardView.as_view()),
]