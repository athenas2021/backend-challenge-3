from django.shortcuts import render
from .forms import UserCreationForm
from .models import UserManager, User


def users(request):
    all_users = list(User.objects.all().values())
    data = {
        'all_users': all_users
    }
    return render(request, 'users.html', data)


def create_user(request):
    if request.method == 'POST':
        if not request.POST['username'] is None and not request.POST['email'] is None:
            try:
                print('teste1')
                user = User(
                    username = request.POST['username'],
                    email = request.POST['email'],
                    password = '123456'
                    )
                user.save()
                print('teste2')
                
                
            except:
                print('Não gravou usuário')
        return render(request, 'users.html')

def user(request):
    return render(request, 'user.html')


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