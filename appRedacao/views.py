from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import AlunoForm, AlunoLoginForm
from django.contrib import messages
from .models import Aluno, Professor
from django.contrib import auth


def index(request):
    return render(request, 'index.html')


def pag_aluno(request):
    return render(request, 'pag_aluno.html')

def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_aluno')
    else:
        form = AlunoForm()
    return render(request, 'cadastro_aluno.html', {'form': form})


'''
def login_aluno(request):
    if request.method == 'POST':
        form = AlunoLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            aluno = Aluno.objects.get(email=email)
            login(request, aluno)
            return redirect('pag_aluno')
    else:
        form = AlunoLoginForm()
    return render(request, 'login_aluno.html', {'form': form})

    
'''



def login_aluno(request):
    if request.method == 'POST':
        form = AlunoLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            aluno = authenticate(request, email=email, password=senha)
            return redirect('pag_aluno')
            #if aluno is not None:
             #   login(request, aluno)
              #   return redirect('pag_aluno')  # Redireciona para a página do aluno após o login
        # Se as credenciais não forem válidas ou a autenticação falhar, exibe uma mensagem de erro
        messages.error(request, 'Credenciais inválidas. Por favor, tente novamente.')
        
    else:
        form = AlunoLoginForm()
    return render(request, 'login_aluno.html', {'form': form})








def logout_aluno(request):
    # Encerra a sessão do usuário
    logout(request)
    # Exibe uma mensagem indicando que o usuário saiu
    messages.info(request, 'Você saiu. Até logo!')
    # Redireciona para a página de login
    return redirect('home')
