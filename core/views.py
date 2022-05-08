from django.shortcuts import render
from .forms import UploadFileForm
import csv, io
from datetime import datetime


def index(request):
    return render(request, 'index.html')


def upload_file(request):
    if request.method == 'POST' and  request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            _handle_uploaded_file(request.FILES['file'])
        return render(request, 'index.html')


def _handle_uploaded_file(f):
    dataset = f.read().decode('UTF-8')
    io_string = io.StringIO(dataset)
    count = 0
    data_arquivo = None
    for row in csv.reader(io_string, delimiter=','):
        if count == 0:
            # Se for primeira linha, guardar data do arquivo
            data_arquivo = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')
            print('Primeira linha:', data_arquivo)
        else:

            data_linha = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')

            print('Data do arquivo:', data_arquivo)
            print('Data da linha', count ,':', data_linha)
            # Comparar se data da linha é igual data do arquivo
            # TODO - Melhorar comparação de datas escrota
            if not data_arquivo.day == data_linha.day or not data_arquivo.month == data_linha.month or not data_arquivo.year == data_linha.year:
                # abortar leitura de arquivo
                print('IGNORAR')
                break

            
        count += 1

'''
Banco origem - row[0]
Agência origem - row[1]
Conta origem - row[2]
Banco destino - row[3]
Agência destino - row[4]
Conta destino - row[5]
Valor da transação - row[6]
Data e hora da transação - row[7]
'''

'''
- Se o arquivo que foi feito upload estiver vazio, uma mensagem de erro deve ser exibida
para o usuário, indicando tal situação;

- Ler a primeira transação(primeira linha do arquivo csv) para determinar qual a data das 
transações desse arquivo em específico;

- Se alguma transação posterior estiver com outra data diferente, ela deve ser ignorada 
e não ser salva no banco de dados;

- A aplicação não deve "duplicar" transações de um determinado dia, ou seja, se o upload 
de transações de um determinado dia já tiver sido realizado anteriormente, uma mensagem de
 erro deve ser exibida ao usuário, indicando que as transações daquela data já foram realizadas;

- Todas as informações da transação são obrigatórias, ou seja, se alguma transação estiver 
com alguma informação faltando, ela também deve ser ignorada e nao ser salva no banco de dados.
'''
