from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('cadastroAluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('loginAluno/', views.login_aluno, name='login_aluno'),
    path('homeAluno/', views.pag_aluno, name='pag_aluno'),
    path('logout/', views.logout_aluno, name='logout_aluno'),

]