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
    data = None
    for row in csv.reader(io_string, delimiter=','):
        # print(row)
        if count == 0:
            data = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')
            print('Primeira linha:', data)
        else:

            datetimex = datetime.strptime(row[7], '%Y-%m-%dT%H:%M:%S')

            print('Data do arquivo:', data)
            print('Data da linha', count ,':', datetimex)

            if not data.day == datetimex.day or not data.month == datetimex.month or not data.year == datetimex.year:
                print('IGNORAR')
        count += 1

        # print(row)
