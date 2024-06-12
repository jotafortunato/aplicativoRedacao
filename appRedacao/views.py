from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import AlunoForm, AlunoLoginForm, RedacaoForm, AdminForm, AdminLoginForm, ProfessorForm, ProfessorLoginForm, DeleteForm, CorrecaoForm, TemaForm
from django.contrib import messages
from .models import Aluno, Redacoes, Admin, Usuarios, Professor, TemaRedacao, Correcao
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
            redacao_form = RedacaoForm(request.POST, request.FILES)
            if redacao_form.is_valid():
                redacao = redacao_form.save(commit=False)
                redacao.id_aluno = aluno
                redacao.data_envio = timezone.now()
                redacao.save()
                messages.success(request, 'Redação enviada com sucesso!')
                return redirect('pag_aluno')
            else:
                messages.error(request, 'Erro ao enviar a redação. Verifique os dados e tente novamente.')

        correcoes = Correcao.objects.filter(id_aluno=aluno).order_by('-data_correcao')
        return render(request, 'pag_aluno.html', {
            'aluno': aluno,
            'correcoes': correcoes,
            'redacao_form': RedacaoForm(),
            'temas': TemaRedacao.objects.all()
        })
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
            if aluno:
                if aluno.check_password(senha):
                    if aluno.ativo:
                        # Login bem-sucedido, definindo o usuário na sessão manualmente
                        request.session['aluno_id'] = aluno.id
                        return redirect('pag_aluno')  # Redireciona para a página inicial ou outra página após o login
                    else:
                        # Usuário inativo, exibir mensagem de aviso
                        messages.error(request, 'Sua conta está inativa. Por favor, entre em contato com o suporte.')
                else:
                    # Senha incorreta, exibir mensagem de erro
                    form.add_error('senha', 'Senha incorreta. Por favor, tente novamente.')
            else:
                # Usuário não encontrado, exibir mensagem de erro
                form.add_error('email', 'Não há conta associada a este e-mail.')
    else:
        form = AlunoLoginForm()
        
    return render(request, 'login_aluno.html', {'form': form})
    


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

def pag_admin(request):
    if 'admin_id' in request.session:
        admin_id = request.session['admin_id']
        admin = Admin.objects.get(id=admin_id)

        user_found = None
        user_active = None

        if request.method == 'POST':
            formProfessor = ProfessorForm(request.POST)
            formAdmin = AdminForm(request.POST)
            formAluno = AlunoForm(request.POST, request.FILES)
            formDelete = DeleteForm(request.POST)
            formTema = TemaForm(request.POST)

            if 'formTema' in request.POST:
                if formTema.is_valid():
                    formTema.save()
                    messages.success(request, 'Tema cadastrado com sucesso!')
                    return redirect('pag_admin')

            elif 'edit_tema' in request.POST:
                tema_id = request.POST.get('tema_id')
                tema_redacao = request.POST.get('tema_redacao')
                try:
                    tema = TemaRedacao.objects.get(id=tema_id)
                    tema.tema_redacao = tema_redacao
                    tema.save()
                    messages.success(request, 'Tema atualizado com sucesso!')
                except TemaRedacao.DoesNotExist:
                    messages.error(request, 'Tema não encontrado.')

            elif 'delete_tema' in request.POST:
                tema_id = request.POST.get('tema_id')
                try:
                    tema = TemaRedacao.objects.get(id=tema_id)
                    tema.delete()
                    messages.success(request, 'Tema excluído com sucesso!')
                except TemaRedacao.DoesNotExist:
                    messages.error(request, 'Tema não encontrado.')

            elif formProfessor.is_valid():
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
                user_active = None

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
            formTema = TemaForm()

        # Obter todos os temas do banco de dados
        temas = TemaRedacao.objects.all()

        return render(request, 'pag_admin.html', {
            'admin': admin,
            'formProfessor': formProfessor,
            'formAdmin': formAdmin,
            'formAluno': formAluno,
            'formDelete': formDelete,
            'formTema': formTema,
            'user_found': user_found,
            'user_active': user_active,
            'temas': temas  # Adicionar a lista de temas ao contexto
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

    


def politica_cookies(request):
    return render(request, 'politica-cookies.html')





#LOGIN PROFESSOR

def login_prof(request):
    if request.method == 'POST':
        form = ProfessorLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            professor = Professor.objects.filter(email=email).first()
            if professor:
                if professor.check_password(senha):
                    if professor.ativo:
                        request.session['professor_id'] = professor.id
                        return redirect('pag_prof')
                    else:
                        messages.error(request, 'Sua conta está inativa. Por favor, entre em contato com o suporte.')
                else:
                    form.add_error('senha', 'Senha incorreta. Por favor, tente novamente.')
            else:
                form.add_error('email', 'Não há conta associada a este e-mail.')
    else:
        form = ProfessorLoginForm()
        
    return render(request, 'login_prof.html', {'form': form})




#PAGINA PROFESSOR

def pag_prof(request):
    if 'professor_id' in request.session:
        professor_id = request.session['professor_id']
        try:
            professor = Professor.objects.get(id=professor_id)
            
            if request.method == 'POST':
                form = CorrecaoForm(request.POST)
                if form.is_valid():
                    correcao = form.save(commit=False)
                    correcao.id_prof = professor
                    correcao.id_redacao_id = request.POST.get('id_redacao')
                    correcao.id_aluno_id = Redacoes.objects.get(id=correcao.id_redacao_id).id_aluno_id
                    correcao.save()
                    messages.success(request, 'Correção enviada com sucesso!')
                    return redirect('pag_prof')
                else:
                    messages.error(request, 'Erro ao enviar a correção. Verifique os dados e tente novamente.')

            # Filtrar redações que ainda não foram corrigidas
            redacoes = Redacoes.objects.filter(correcao__isnull=True)
            context = {
                'professor': professor,
                'redacoes': redacoes,
                'correcao_form': CorrecaoForm()
            }
            return render(request, 'pag_prof.html', context)
        except Professor.DoesNotExist:
            messages.error(request, 'Professor não encontrado.')
            return redirect('login_prof')
    else:
        messages.error(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login_prof')
    



def corrigir_redacao(request, redacao_id):
    if 'professor_id' not in request.session:
        messages.error(request, 'Você precisa fazer login para acessar esta página.')
        return redirect('login_prof')

    professor_id = request.session['professor_id']
    professor = get_object_or_404(Professor, id=professor_id)
    redacao = get_object_or_404(Redacoes, id=redacao_id)

    if request.method == 'POST':
        form = CorrecaoForm(request.POST)
        if form.is_valid():
            correcao = form.save(commit=False)
            correcao.redacao = redacao
            correcao.professor = professor
            correcao.save()
            messages.success(request, 'Redação corrigida com sucesso!')
            return redirect('pag_prof')
    else:
        form = CorrecaoForm()

    context = {
        'redacao': redacao,
        'form': form
    }
    return render(request, 'corrigir_redacao.html', context)
    
