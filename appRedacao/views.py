from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import AlunoForm, AlunoLoginForm
from django.contrib import messages
from .models import Aluno, Professor
from django.contrib import auth


def index(request):
    return render(request, 'index.html')


'''def pag_aluno(request):
    return render(request, 'pag_aluno.html')
    '''

def pag_aluno(request):
    if 'aluno_id' in request.session:
        return render(request, 'pag_aluno.html')
    else:
        messages.error(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login_aluno')

def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_aluno')
    else:
        form = AlunoForm()
    return render(request, 'cadastro_aluno.html', {'form': form})


# NAO REDIRECIONA, ACHO QUE ELE NAO RECONHECE A CLASSE PERSONALIZADA QUANDO USA AUTHENTICATE
# SÓ REDIRECIONA SE COMENTAR O ULTIMO IF 

def login_aluno(request):
    if request.method == 'POST':
        form = AlunoLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            aluno = Aluno.objects.filter(email=email).first()
            if aluno and aluno.check_password(senha):
                # Login bem-sucedido, definindo o usuário na sessão manualmente
                request.session['aluno_id'] = aluno.id
                return redirect('pag_aluno')  # Redireciona para a página inicial ou outra página após o login
            else:
                # Senha incorreta, exibir mensagem de erro
                form.add_error('senha', 'Senha incorreta. Por favor, tente novamente.')
    else:
        form = AlunoLoginForm()
        
    error_messages = messages.get_messages(request)

    return render(request, 'login_aluno.html', {'form': form, 'error_messages': error_messages})
    






def logout_aluno(request):
    # Encerra a sessão do usuário
    logout(request)
    # Exibe uma mensagem indicando que o usuário saiu
    messages.info(request, 'Você saiu. Até logo!')
    # Redireciona para a página de login
    return redirect('home')
