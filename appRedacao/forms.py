from django import forms 
from .models import Aluno
from django.contrib.auth.hashers import check_password

class AlunoForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Aluno
        fields = ['matricula', 'nome_aluno', 'email', 'senha', 'dt_nasc', 'endereco', 'curso']
        error_messages = {
            'email': {
            'unique': "Já existe um aluno com este e-mail.",
        }
        }




class AlunoLoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'placeholder': 'Digite seu e-mail'}))
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))

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
