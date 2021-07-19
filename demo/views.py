from django.shortcuts import render
from django.http import HttpResponse
import openpyxl
from pathlib import Path
import os
from django.urls import reverse
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from demo.models import *
import django
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.contrib.auth.decorators import permission_required


@permission_required('demo.uploadfile', login_url='auth/login/')

def fileUploaderView(request):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                upload(request.FILES['file'])
                return HttpResponseRedirect('savedb/' + request.FILES['file'].name)
            else:
                return HttpResponse("<h2>File uploaded not successful!</h2>")
        form = UploadFileForm()
        return render(request, 'demo/index.html', {'form': form})



def search(request):

    p = Demo.objects.filter(patientcode__contains=request.GET['q'])
    return render(request, 'demo/test.html', {'users': p})


def detail(request, bn):
    f0 = 0
    f1 = 0
    f2 = 0
    id = Demo.objects.filter(patientcode=bn)
    if id[0].status == 'f0':
        p = Demo.objects.filter(f0=id[0].id)
        f0 = Demo.objects.filter(f0=id[0].id, status='f0').count()
        f1 = Demo.objects.filter(f0=id[0].id, status='f1').count()
        f2 = Demo.objects.filter(f0=id[0].id, status='f2').count()
    elif id[0].status == 'f1':
        p = Demo.objects.filter(f1=id[0].id)
        f1 = Demo.objects.filter(f1=id[0].id, status='f1').count()
        f2 = Demo.objects.filter(f1=id[0].id, status='f2').count()
    else:
        p = Demo.objects.filter(f2=id[0].id)
    return render(request, 'demo/detail.html', {'users': p, 'id': id[0], 'f0': f0, 'f1': f1, 'f2': f2})


def upload(f):
    file = open('uploads/' + f.name, 'wb+')
    for chunk in f.chunks():
        file.write(chunk)


def index(request):
    users = Demo.objects.order_by('id')[::-1]
    f0 = Demo.objects.filter(status='f0').count()
    f1 = Demo.objects.filter(status='f1').count()
    f2 = Demo.objects.filter(status='f2').count()
    paginator = Paginator(users, 5)
    pageNumber = request.GET.get('page')
    try:
        users = paginator.page(pageNumber)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'demo/test.html', {'users': users, 'f0': f0, 'f1': f1, 'f2': f2})


def view(request, f):
    users = Demo.objects.filter(status=f)
    paginator = Paginator(users, 5)
    pageNumber = request.GET.get('page')
    try:
        users = paginator.page(pageNumber)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'demo/test.html', {'users': users})


def savedb(request, filename):
    import xlrd
    from django.shortcuts import get_object_or_404
    file_extension = os.path.splitext(filename)
    print(filename)
    if file_extension[1] == '.xlsx':
        xlsx_file = Path('uploads', filename)
        wb_obj = openpyxl.load_workbook(xlsx_file)
        # Read the active sheet:
        sheet = wb_obj.active
    elif file_extension[1] == '.xls':
        xlsx_file = Path('uploads', filename)
        wb = xlrd.open_workbook(xlsx_file)
        sheet = wb.sheet_by_index(0)
    else:
        return HttpResponse("<h2>File not supported!</h2>" + file_extension[1])
    for row in sheet:
        if not row[3].value:
            ff0 = 0
        else:
            ff00 = Demo.objects.filter(patientcode=row[3].value)
            ff0 = ff00[0].id

        if not row[4].value:
            ff1 = 0
        else:
            ff00 = Demo.objects.filter(patientcode=row[4].value)
            ff1 = ff00[0].id

        if not row[5].value:
            ff2 = 0
        else:
            ff00 = Demo.objects.filter(patientcode=row[5].value)
            ff2 = ff00[0].id

        cell = Demo(patientcode=row[0].value,
                    name=row[1].value,
                    status=row[2].value,
                    f0_id=ff0,
                    f1_id=ff1,
                    f2_id=ff2,
                    phone=row[6].value,
                    address=row[7].value,
                    )
        cell.save()
    return HttpResponseRedirect(reverse('demo:index'))
