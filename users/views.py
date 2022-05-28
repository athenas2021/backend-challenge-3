from django.shortcuts import render
from .forms import UserCreationForm
from .models import UserManager, User
from django.core.mail import send_mail

def users(request):
    all_users = list(User.objects.all().order_by('id').values())
    data = {
        'all_users': all_users
    }
    return render(request, 'users.html', data)


def create_user(request):
    if request.method == 'POST':
        if not request.POST['username'] is None and not request.POST['email'] is None:
            try:
                # Gera senha
                import random
                passw = str(random.randint(100000, 999999))
                user = User(
                    username = request.POST['username'],
                    email = request.POST['email'],
                    password = passw
                    )
                user.save()
                # Manda e-mail com senha
                send_mail(
                    'Nova conta',
                    'Sua senha: {passw}.'.format(passw=passw),
                    'suport@alurachallenge.com',
                    [request.POST['email']],
                    fail_silently=False,
                )
            except Exception as e:
                print('Não gravou usuário', e)
        return render(request, 'users.html')


def edit_user(request):
    if request.method == 'POST':
        if not request.POST['username'] is None and not request.POST['email'] is None:
            user = User.objects.get(pk=int(request.POST['submit']))
            user.user_name = request.POST['username']
            user.email = request.POST['email']
            user.save()
            return render(request, 'users.html')

def user(request):
    if request.method == 'POST':

        data = {
            'type': 'include'
        }
    if request.method == 'POST':    
        if 'edit' in request.POST:
            user = User.objects.get(pk=int(request.POST['edit']))
            data = {
                'type': 'edit',
                'user_id': request.POST['edit'],
                'user_name': user.get_username(),
                'user_email': user.email
            }

    
    return render(request, 'user.html', data)


'''
- Apenas 2 informações serão necessárias no cadastro: Nome e Email, sendo ambas obrigatórias
- A aplicação deve gerar uma senha aleatória para o usuário, composta de 6 números;
- A senha deverá ser enviada para o email do usuário sendo cadastrado;
- A senha não deve ser armazenada no banco de dados em texto aberto, devendo ser salvo um hash dela, 
gerado pelo algoritmo BCrypt;
- A aplicação não deve permitir o cadastro de um usuário com o email de outro usuário já cadastrado, 
devendo exibir uma mensagem de erro caso essa situação ocorra;
- A aplicação deve ter um usuário padrão previamente cadastrado, com nome: Admin, email: admin@email.com.br e senha: 123999;
- O usuário padrão não pode ser editado e nem excluído da aplicação, tampouco deve ser exibido na lista de usuários cadastrados;
- Qualquer usuário tem permissão para listar, cadastrar, alterar e excluir outros usuários;
- Um usuário não pode excluir ele próprio da aplicação.
'''