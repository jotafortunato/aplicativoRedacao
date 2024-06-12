from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
    path('cadastroAluno/', views.cadastro_aluno, name='cadastro_aluno'),
    path('loginAluno/', views.login_aluno, name='login_aluno'),
    path('homeAluno/', views.pag_aluno, name='pag_aluno'),
    path('logout/', views.logout_aluno, name='logout_aluno'),
    path('loginAdmin/', views.login_admin, name='login_admin'),
    path('gerenciamento/', views.pag_admin, name='pag_admin'),
    path('logout/', views.logout_admin, name='logout_admin'),
    path('cookies/', views.politica_cookies, name='cookies'),
    path('homeProf/', views.pag_prof, name='pag_prof'),
    path('loginProf/', views.login_prof, name='login_prof'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)