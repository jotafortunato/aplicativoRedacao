from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.utils import timezone

class Aluno(models.Model):
    id = models.AutoField(primary_key=True)
    matricula = models.CharField(max_length=50, blank=True, null=True)
    nome_aluno = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=8)
    dt_nasc = models.DateField()
    endereco = models.CharField(max_length=200)
    curso = models.CharField(max_length=100, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='aluno/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Antes de salvar, criptografa a senha se ela não estiver criptografada
        if not self.senha.startswith('pbkdf2_sha256$'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_aluno
    
    def check_password(self, raw_password):
        # Verifica se a senha fornecida corresponde à senha armazenada no banco de dados
        return check_password(raw_password, self.senha)

    class Meta:
        verbose_name_plural = "Alunos"


class Professor(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=8)
    dt_nasc = models.DateField()
    area_ensino = models.CharField(max_length=100, blank=True, null=True)
    endereco = models.CharField(max_length=200)
    ativo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Antes de salvar, criptografa a senha se ela não estiver criptografada
        if not self.senha.startswith('pbkdf2_sha256$'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    def check_password(self, raw_password):
        # Verifica se a senha fornecida corresponde à senha armazenada no banco de dados
        return check_password(raw_password, self.senha)
    

    class Meta:
        verbose_name_plural = "Professores"

class Redacoes(models.Model):
    id = models.AutoField(primary_key=True)
    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    texto_redacao = models.TextField()
    tema_redacao = models.CharField(max_length=200)
    data_envio = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Redacoes"

class Correcao(models.Model):
    id = models.AutoField(primary_key=True)
    id_redacao = models.ForeignKey(Redacoes, on_delete=models.CASCADE)
    id_prof = models.ForeignKey(Professor, on_delete=models.CASCADE)
    feedback = models.TextField()
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    data_correcao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Correcoes"

class HistRedacao(models.Model):
    id = models.AutoField(primary_key=True)
    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    id_redacao = models.ForeignKey(Redacoes, on_delete=models.CASCADE)
    data_acesso = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "HistRedacoes"


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=8)
    funcao = models.CharField(max_length=55)

    def save(self, *args, **kwargs):
        # Antes de salvar, criptografa a senha se ela não estiver criptografada
        if not self.senha.startswith('pbkdf2_sha256$'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
    
    def check_password(self, raw_password):
        # Verifica se a senha fornecida corresponde à senha armazenada no banco de dados
        return check_password(raw_password, self.senha)



class Usuarios(models.Model):
    id = models.AutoField(primary_key=True)
    id_aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    id_prof = models.ForeignKey(Professor, on_delete=models.CASCADE)
    id_admin = models.ForeignKey(Admin, on_delete=models.CASCADE)



import os
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

@receiver(pre_delete, sender=Aluno)
def delete_aluno_image(sender, instance, **kwargs):
    # Verifique se existe uma foto associada ao aluno
    if instance.foto:
        # Exclua o arquivo de imagem
        if os.path.isfile(instance.foto.path):
            os.remove(instance.foto.path)
