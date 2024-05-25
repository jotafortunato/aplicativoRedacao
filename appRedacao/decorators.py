# decorators.py

from django.shortcuts import redirect
from functools import wraps
from .models import Aluno, Professor, Admin



def user_is_active(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_type = request.session.get('user_type')
        user_id = request.session.get('user_id')

        if user_type == 'Aluno':
            try:
                user = Aluno.objects.get(id=user_id)
            except Aluno.DoesNotExist:
                return redirect('pag_aluno')
        elif user_type == 'Professor':
            try:
                user = Professor.objects.get(id=user_id)
            except Professor.DoesNotExist:
                return redirect('login_professor')
        else:
            return redirect('login_aluno')

        if not user.ativo:
            return redirect('home')  # Página que informa que o usuário está desativado

        return view_func(request, *args, **kwargs)
    return _wrapped_view

