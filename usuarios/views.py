from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rolepermissions.decorators import has_permission_decorator
from .models import Users
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages

@has_permission_decorator('cadastrar_vendedor')
def cadastrar_vendedor(request):
    if request.method == "GET":
        vendedores = Users.objects.filter(cargo="V")
        return render(request, 'castastrar_vendedor.html', {'vendedores': vendedores})
    
    if request.method == 'POST':
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        user = Users.objects.filter(email=email)
        
        if user.exists():
            messages.add_message(request, messages.WARNING, 'E-mail já cadastrado!')
            return redirect('/auth/cadastrar_vendedor')
        
        if len(nome.strip()) == 0 or len(sobrenome.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'Favor preencher os campos corretamente!')
            return redirect('/auth/cadastrar_vendedor')
        
        if len(email.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'Favor preencher o campo e-mail!')
            return redirect('/auth/cadastrar_vendedor')
        
        if len(senha) <= 8:
            messages.add_message(request, messages.WARNING, 'Sua senha deve conter mais de 8 caracteres!')
            return redirect('/auth/cadastrar_vendedor')
            
        
        user = Users.objects.create_user(username=email, email=email, password=senha, first_name=nome, last_name=sobrenome, cargo="V")
        messages.add_message(request, messages.SUCCESS, 'Usuário cadastrado com sucesso!')
        return redirect('/auth/cadastrar_vendedor')
    
def login(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect( '/')

        return render(request, 'login.html')
    
    elif request.method == "POST":
        login = request.POST.get('email')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(username=login, password=senha)
        
        if not user:
            messages.add_message(request, messages.ERROR, 'E-mail ou senha incorrétos!')
            return redirect('/auth/login')
        
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Seja bem-vindo(a)!')
        return redirect('/auth/cadastrar_vendedor')
    
def sair(request):
    request.session.flush()
    messages.add_message(request, messages.INFO, 'Logout realizado com sucesso!')
    return redirect(reverse('login'))

@has_permission_decorator('cadastrar_vendedor')
def excluir_usuario(request, id):
    vendedor = get_object_or_404(Users, id=id)
    vendedor.delete()
    messages.add_message(request, messages.SUCCESS, 'Vendedor excluido com sucesso!')
    return redirect(reverse('cadastrar_vendedor'))

def handler404(request, exception):
    return render(request, 'not_found.html')
    