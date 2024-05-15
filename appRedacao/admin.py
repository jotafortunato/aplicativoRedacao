from django.contrib import admin
from .models import Aluno, Professor, Redacoes, HistRedacao, Correcao
# Register your models here.

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Redacoes)
admin.site.register(HistRedacao)
admin.site.register(Correcao)