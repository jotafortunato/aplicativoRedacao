from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from appRedacao.models import Aluno, Professor

class Command(BaseCommand):
    help = 'Criptografa todas as senhas existentes na tabela Aluno'

    def handle(self, *args, **options):
        alunos = Aluno.objects.all()
        for aluno in alunos:
            aluno.senha = make_password(aluno.senha)
            aluno.save()
        self.stdout.write(self.style.SUCCESS('Todas as senhas foram criptografadas com sucesso!'))

