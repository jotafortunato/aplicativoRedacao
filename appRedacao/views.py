from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import AlunoForm, AlunoLoginForm, RedacaoForm, AdminForm, AdminLoginForm, ProfessorForm, ProfessorLoginForm, DeleteForm
from django.contrib import messages
from .models import Aluno, Redacoes, Admin, Usuarios, Professor
from django.utils import timezone
from django.utils.timezone import activate





#INICIO
def index(request):
    return render(request, 'index.html')


#PAGINA DO ALUNO


def pag_aluno(request):
    if 'aluno_id' in request.session:
        aluno_id = request.session['aluno_id']
        aluno = Aluno.objects.get(id=aluno_id)
        if request.method == 'POST':
            activate('America/Sao_Paulo')
            tema_redacao = request.POST.get('tema_redacao')
            texto_redacao = request.POST.get('redacao')

            redacao = Redacoes(
                id_aluno_id=aluno_id,
                tema_redacao=tema_redacao,
                texto_redacao=texto_redacao,
                data_envio=timezone.now()
            )
            redacao.save()

            messages.success(request, 'Redação enviada com sucesso!')
            return redirect('pag_aluno')

        return render(request, 'pag_aluno.html', {'aluno': aluno})
    else:
        messages.error(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login_aluno')



#CADASTRO ALUNO

def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login_aluno')
    else:
        form = AlunoForm()
    return render(request, 'cadastro_aluno.html', {'form': form})




#LOGIN ALUNO

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
    


#FAZER LOGOUT ALUNO

def logout_aluno(request):
    # Encerra a sessão do usuário
    logout(request)
    # Exibe uma mensagem indicando que o usuário saiu
    messages.info(request, 'Você saiu. Até logo!')
    # Redireciona para a página de login
    return redirect('home')


#ENVIAR REDAÇÃO ALUNO

def enviar_redacao(request):
    if 'aluno_id' in request.session:  # Verifica se o aluno está autenticado
        if request.method == 'POST':
            texto_redacao = request.POST.get('texto_redacao', '')
            tema_redacao = request.POST.get('tema_redacao', '')  # Captura o tema da redação
            redacao = Redacoes.objects.create(
                id_aluno=request.user,
                texto_redacao=texto_redacao,
                tema_redacao=tema_redacao,
                data_envio=timezone.now()  # Salva a data de envio atual
            )
            redacao.save()
            return redirect('pagina_aluno')
        return render(request, 'formulario_redacao.html')
    else:
        messages.error(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login_aluno')










#CADASTRO ADMIN

def cadastro_admin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_admin')
    else:
        form = AdminForm()
    return render(request, 'cadastro_admin.html', {'form': form})


#LOGIN ADMIN

def login_admin(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            admin = Admin.objects.filter(email=email).first()
            if admin and admin.check_password(senha):
                # Login bem-sucedido, definindo o usuário na sessão manualmente
                request.session['admin_id'] = admin.id
                return redirect('pag_admin')  # Redireciona para a página inicial ou outra página após o login
            else:
                # Senha incorreta, exibir mensagem de erro
                form.add_error('senha', 'Senha incorreta. Por favor, tente novamente.')
    else:
        form = AdminLoginForm()
        
    error_messages = messages.get_messages(request)

    return render(request, 'login_admin.html', {'form': form, 'error_messages': error_messages})



#PAGINA DO ADMIN

from .forms import ProfessorForm, AdminForm  # Importe os formulários necessários


'''
def pag_admin(request):
    if 'admin_id' in request.session:
        admin_id = request.session['admin_id']
        admin = Admin.objects.get(id=admin_id)  # Obtenha o objeto Admin com base no ID da sessão

        user_found = None
        user_email = None

        if request.method == 'POST':
            formProfessor = ProfessorForm(request.POST)
            formAdmin = AdminForm(request.POST)
            formDelete = DeleteForm(request.POST)

            if formProfessor.is_valid():
                formProfessor.save()
                messages.success(request, 'Professor cadastrado com sucesso!')
                return redirect('pag_admin')  # Redirecione para evitar reenvio do formulário
            
            elif formAdmin.is_valid():
                formAdmin.save()
                messages.success(request, 'Admin cadastrado com sucesso!')
                return redirect('pag_admin')

            elif formDelete.is_valid():
                email = formDelete.cleaned_data['email']
                user_email = email
                
                if 'confirm_delete' in request.POST:
                    try:
                        user = Aluno.objects.get(email=email)
                        user.delete()
                        messages.success(request, 'Usuário excluído com sucesso!')
                        return redirect('pag_admin')
                    except Aluno.DoesNotExist:
                        try:
                            user = Professor.objects.get(email=email)
                            user.delete()
                            messages.success(request, 'Usuário excluído com sucesso!')
                            return redirect('pag_admin')
                        except Professor.DoesNotExist:
                            try:
                                user = Admin.objects.get(email=email)
                                user.delete()
                                messages.success(request, 'Usuário excluído com sucesso!')
                                return redirect('pag_admin')
                            except Admin.DoesNotExist:
                                messages.error(request, 'O usuário com o email fornecido não existe.')
                                return redirect('pag_admin')
                else:
                    try:
                        user = Aluno.objects.get(email=email)
                        user_found = user.nome_aluno
                    except Aluno.DoesNotExist:
                        try:
                            user = Professor.objects.get(email=email)
                            user_found = user.nome
                        except Professor.DoesNotExist:
                            try:
                                user = Admin.objects.get(email=email)
                                user_found = user.nome
                            except Admin.DoesNotExist:
                                user_found = None

            else:
                messages.error(request, 'Erro ao cadastrar. Verifique os dados e tente novamente.')
        else:
            formProfessor = ProfessorForm()
            formAdmin = AdminForm()
            formDelete = DeleteForm()

        return render(request, 'pag_admin.html', {
            'admin': admin,
            'formProfessor': formProfessor,
            'formAdmin': formAdmin,
            'formDelete': formDelete,
            'user_found': user_found,
            'user_email': user_email
        })
    else:
        messages.error(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login_admin')
    

    '''


def pag_admin(request):
    if 'admin_id' in request.session:
        admin_id = request.session['admin_id']
        admin = Admin.objects.get(id=admin_id)

        user_found = None
        user_found_email = None
        user_active = None

        if request.method == 'POST':
            formProfessor = ProfessorForm(request.POST)
            formAdmin = AdminForm(request.POST)
            formAluno = AlunoForm(request.POST)
            formDelete = DeleteForm(request.POST)

            if formProfessor.is_valid():
                formProfessor.save()
                messages.success(request, 'Professor cadastrado com sucesso!')
                return redirect('pag_admin')
            
            elif formAdmin.is_valid():
                formAdmin.save()
                messages.success(request, 'Admin cadastrado com sucesso!')
                return redirect('pag_admin')
            
            elif formAluno.is_valid():
                formAluno.save()
                messages.success(request, 'Aluno cadastrado com sucesso!')
                return redirect('pag_admin')

            elif formDelete.is_valid():
                email = formDelete.cleaned_data['email']
                user_found = None
                user_deleted = False
                user_deactivated = False
                user_activated = False
                
                try:
                    aluno = Aluno.objects.get(email=email)
                    user_found = aluno
                except Aluno.DoesNotExist:
                    try:
                        professor = Professor.objects.get(email=email)
                        user_found = professor
                    except Professor.DoesNotExist:
                        try:
                            admin = Admin.objects.get(email=email)
                            user_found = admin
                        except Admin.DoesNotExist:
                            user_found = None

                if user_found:
                    user_active = user_found.ativo if isinstance(user_found, (Aluno, Professor)) else None

                    if 'confirm_delete' in request.POST:
                        user_found.delete()
                        messages.success(request, 'Usuário excluído com sucesso!')
                        return redirect('pag_admin')
                    elif 'deactivate_user' in request.POST:
                        if isinstance(user_found, (Aluno, Professor)):
                            user_found.ativo = False
                            user_found.save()
                            messages.success(request, 'Usuário desativado com sucesso!')
                            return redirect('pag_admin')
                    elif 'activate_user' in request.POST:
                        if isinstance(user_found, (Aluno, Professor)):
                            user_found.ativo = True
                            user_found.save()
                            messages.success(request, 'Usuário ativado com sucesso!')
                            return redirect('pag_admin')
                else:
                    messages.error(request, 'O usuário com o email fornecido não existe.')

            else:
                messages.error(request, 'Erro ao cadastrar. Verifique os dados e tente novamente.')

        else:
            formProfessor = ProfessorForm()
            formAdmin = AdminForm()
            formAluno = AlunoForm()
            formDelete = DeleteForm()

        return render(request, 'pag_admin.html', {
            'admin': admin,
            'formProfessor': formProfessor,
            'formAdmin': formAdmin,
            'formAluno': formAluno,
            'formDelete': formDelete,
            'user_found': user_found,
            'user_active': user_active
        })
    else:
        messages.error(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login_admin')


    

















#FAZER LOGOUT ADMIN

def logout_admin(request):
    # Encerra a sessão do usuário
    logout(request)
    # Exibe uma mensagem indicando que o usuário saiu
    messages.info(request, 'Você saiu. Até logo!')
    # Redireciona para a página de login
    return redirect('home')

