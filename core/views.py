from django.shortcuts import render
from .forms import UploadFileForm
import csv, io

def index(request):
    return render(request, 'index.html')


def upload_file(request):
   
    if request.method == 'POST' and  request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
        return render(request, 'index.html')

def handle_uploaded_file(f):
    dataset = f.read().decode('UTF-8')
    io_string = io.StringIO(dataset)
    for row in csv.reader(io_string, delimiter=','):
        print(row)
