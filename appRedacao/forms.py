from django import forms 
from .models import Aluno, Redacoes, Professor, Admin, Correcao, TemaRedacao
from django.contrib.auth.hashers import check_password


#FORMULÁRIO CRIAÇÃO ALUNO

class AlunoForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha (8 caracteres)'}),
        label='Senha'
    )

    class Meta:
        model = Aluno
        fields = ['nome_aluno', 'email', 'senha', 'dt_nasc', 'endereco', 'foto']
        widgets = {
            'nome_aluno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha (max 8 caracteres)'}),
            'dt_nasc': forms.DateInput(attrs={'class': 'form-control', 'placeholder': '(DD/MM/AAAA)'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome_aluno': 'Nome Completo',
            'email': 'E-mail',
            'dt_nasc': 'Data de Nascimento',
            'endereco': 'Endereço',
            'foto': 'Foto de Perfil',
        }

        error_messages = {
            'email': {
                'unique': "Já existe um aluno com este e-mail.",
            }
        }


#FORMULÁRIO CRIAÇÃO PROFESSOR

class ProfessorForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha (8 caracteres)'}),
        label='Senha'
    )

    class Meta:
        model = Professor
        fields = ['nome', 'email', 'senha', 'dt_nasc', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha (max 8 caracteres)'}),
            'dt_nasc': forms.DateInput(attrs={'class': 'form-control', 'placeholder': '(DD/MM/AAAA)'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'dt_nasc': 'Data de Nascimento',
            'endereco': 'Endereço',
        }
        error_messages = {
            'email': {
            'unique': "Já existe um professor com este e-mail.",
        }
        }

#FORMULÁRIO CRIAÇÃO ADMIN

class AdminForm(forms.ModelForm):
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha (8 caracteres)'}),
        label='Senha'
    )

    class Meta:
        model = Admin
        fields = ['nome', 'email', 'senha', 'funcao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
            'funcao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Função'}),
        }
        labels = {
            'nome': 'Nome Completo',
            'email': 'E-mail',
            'funcao': 'Função',
        }
        error_messages = {
            'email': {
            'unique': "Já existe um usuário com este e-mail.",
        }
        }



#FORMULÁRIO DE LOGIN ALUNO

class AlunoLoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'}))
    senha = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        senha = cleaned_data.get('senha')

        if email and senha:
            # Verifica se o aluno com o email fornecido existe no banco de dados
            aluno = Aluno.objects.filter(email=email).first()
            if aluno:
                # Verifica se a senha fornecida corresponde à senha criptografada no banco de dados
                if not check_password(senha, aluno.senha):
                    raise forms.ValidationError('Senha incorreta. Por favor, tente novamente.')
            else:
                raise forms.ValidationError('Aluno não encontrado. Por favor, verifique suas credenciais.')
        return cleaned_data
    



#FORMULÁRIO DE LOGIN PROFESSOR

class ProfessorLoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'}))
    senha = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        senha = cleaned_data.get('senha')

        if email and senha:
            # Verifica se o professor com o email fornecido existe no banco de dados
            professor = Professor.objects.filter(email=email).first()
            if professor:
                # Verifica se a senha fornecida corresponde à senha criptografada no banco de dados
                if not check_password(senha, professor.senha):
                    raise forms.ValidationError('Senha incorreta. Por favor, tente novamente.')
            else:
                raise forms.ValidationError('Professor não encontrado. Por favor, verifique suas credenciais.')
        return cleaned_data
    


#FORMULÁRIO DE LOGIN ADMIN

class AdminLoginForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'}))
    senha = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        senha = cleaned_data.get('senha')

        if email and senha:
            # Verifica se o admin com o email fornecido existe no banco de dados
            admin = Admin.objects.filter(email=email).first()
            if admin:
                # Verifica se a senha fornecida corresponde à senha criptografada no banco de dados
                if not check_password(senha, admin.senha):
                    raise forms.ValidationError('Senha incorreta. Por favor, tente novamente.')
            else:
                raise forms.ValidationError('Admin não encontrado. Por favor, verifique suas credenciais.')
        return cleaned_data
    











#FORMULÁRIO DE ENVIO DA REDAÇÃO

class RedacaoForm(forms.ModelForm):
    class Meta:
        model = Redacoes
        fields = ['tema_redacao', 'arquivo_redacao']
        widgets = {
            'tema_redacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tema da Redação'}),
            'arquivo_redacao': forms.FileInput(attrs={'class': 'form-control'}),
        }




class TemaForm(forms.ModelForm):
    class Meta:
        model = TemaRedacao
        fields = ['tema_redacao']
        widgets = {
            'tema_redacao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira o tema desejado'}),
        }






class DeleteForm(forms.Form):
    email = forms.EmailField(label='Email do usuário', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email do usuário'}))




class CorrecaoForm(forms.ModelForm):
    class Meta:
        model = Correcao
        fields = ['feedback', 'nota']
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nota': forms.NumberInput(attrs={'class': 'form-control'})
        }