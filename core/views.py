from django.shortcuts import render
from .forms import UploadFileForm
import csv, io
from datetime import datetime
from .models import DayProcess, Transaction


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
    day_process = None
    for row in csv.reader(io_string, delimiter=','):
        transaction = None
        if count == 0:
            # Se for primeira linha, guardar data do arquivo
            data_arquivo = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')

            # Verificar no banco se já existe a transação desse dia 
            if len(DayProcess.objects.filter(date=data_arquivo)) > 0:
                print('Já existe um processamento para o dia: ', data_arquivo)
                break
            else:
                day_process = DayProcess.objects.create(date=data_arquivo)
                row_info = _validate_row(row, day_process)
                if None in row_info.values() or '' in row_info.values():
                        print('Algum valor nulo na linha, pulando registro: ', count)
                        continue
                transaction = _instantiate_transaction(row_info)
                if not transaction == None:
                    transaction.save()
        else:

            data_linha = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')

            # TODO - Melhorar comparação de datas escrota
            if data_arquivo.day == data_linha.day and data_arquivo.month == data_linha.month and data_arquivo.year == data_linha.year:

                row_info = _validate_row(row, day_process)

                if None in row_info.values() or '' in row_info.values():
                    print('Algum valor nulo na linha, pulando registro: ', count)
                    continue

                transaction = _instantiate_transaction(row_info)
                if not transaction == None:
                    transaction.save()
        count += 1

    
def _validate_row(row, day_process):
    row_info =  {
                'origin_bank': row[0],
                'origin_agency': row[1],
                'origin_account': row[2],
                'destiny_bank': row[3],
                'destiny_agency': row[4],
                'destiny_account': row[5],
                'transaction_value': row[6],
                'transaction_date_time': datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S'),
                'day_process': day_process
            }
    return row_info

def _instantiate_transaction(row_info):
    transaction = Transaction(
        origin_bank=row_info['origin_bank'],
        origin_agency=row_info['origin_agency'],
        origin_account=row_info['origin_account'],
        destiny_bank=row_info['destiny_bank'],
        destiny_agency=row_info['destiny_agency'],
        destiny_account=row_info['destiny_account'],
        transaction_value=float(row_info['transaction_value']),
        transaction_date_time=row_info['transaction_date_time'],
        day_process=row_info['day_process'],
    )
    return transaction
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
