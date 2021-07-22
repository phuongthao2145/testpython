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
from django.contrib.auth.decorators import permission_required
from slugify import slugify
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()


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
    users = Demo.objects.filter(patientcode=bn).first()
    fc = Demo.objects.filter(id=users.f_status_id).first()
    f = Demo.objects.filter(f_status=users.id).exclude(test_result=5)
    return render(request, 'demo/detail.html', {'id': users, 'users': f, 'fc': fc})


def upload(f):
    file = open('uploads/' + f.name, 'wb+')
    for chunk in f.chunks():
        file.write(chunk)


def index(request):
    users = Demo.objects.exclude(test_result=5).order_by('id')[::-1]
    p = ''
    return render(request, 'demo/test.html', {'users': users, 'p': p})


def view(request, f):
    if City.objects.filter(slug=f):
        test = City.objects.filter(slug=f).first()
        users = Demo.objects.filter(province=test.id).order_by('status')
        d1 = Demo.objects.filter(city=test.id, status=1)
        newf0 = 0
        for d in d1:
            if d.created_at.date() == datetime.today().date():
                newf0 += 1
        p = {'f0': Demo.objects.filter(city=test.id, status=1).exclude(test_result=5),
             'f1': Demo.objects.filter(city=test.id, status=2).exclude(test_result=5),
             'f2': Demo.objects.filter(city=test.id, status=3).exclude(test_result=5),
             'f3': Demo.objects.filter(city=test.id, status=4).exclude(test_result=5),
             'isolate': Demo.objects.filter(city=test.id, isolation_area=test.id),
             'isolatef1': Demo.objects.filter(city=test.id, isolation_area=test.id, status=2),
             'isolatef2': Demo.objects.filter(city=test.id, isolation_area=test.id, status=3),
             'title': test.cityname,
             'newf0': newf0,
             }
    elif District.objects.filter(slug=f):
        # get district
        district = District.objects.filter(slug=f).first()
        #get all province
        provinces = Province.objects.filter(district=district.id)

        p = list()
        for test in provinces:
            #users = Demo.objects.filter(province=test.id)
            d1 = Demo.objects.filter(province=test.id, status=1)
            newf0 = 0
            for d in d1:
                if d.created_at.date() == datetime.today().date():
                    newf0 += 1

            p.append({'f0': Demo.objects.filter(province=test.id, status=1).exclude(test_result=5),
                 'f1': Demo.objects.filter(province=test.id, status=2).exclude(test_result=5),
                 'f2': Demo.objects.filter(province=test.id, status=3).exclude(test_result=5),
                 'f3': Demo.objects.filter(province=test.id, status=4).exclude(test_result=5),
                 'isolate': Demo.objects.filter(province=test.id, isolation_area=test.id),
                 'isolatef1': Demo.objects.filter(province=test.id, isolation_area=test.id, status=2),
                 'isolatef2': Demo.objects.filter(province=test.id, isolation_area=test.id, status=3),
                 'newf0': newf0,
                 'title': test.proname,
                    'id': test.id,
                 })
        return render(request, 'demo/district.html', {'users': provinces, 'p': p})

    elif Province.objects.filter(slug=f):
        test = Province.objects.filter(slug=f).first()
        users = Demo.objects.filter(province=test.id).order_by('status')
        d1 = Demo.objects.filter(province=test.id, status=1)
        newf0 = 0
        for d in d1:
            if d.created_at.date() == datetime.today().date():
                newf0 += 1

        p = {'f0': Demo.objects.filter(province=test.id, status=1).exclude(test_result=5),
                 'f1': Demo.objects.filter(province=test.id, status=2).exclude(test_result=5),
                 'f2': Demo.objects.filter(province=test.id, status=3).exclude(test_result=5),
                 'f3': Demo.objects.filter(province=test.id, status=4).exclude(test_result=5),
                 'isolate': Demo.objects.filter(province=test.id, isolation_area=test.id),
                 'isolatef1': Demo.objects.filter(province=test.id, isolation_area=test.id, status=2),
                 'isolatef2': Demo.objects.filter(province=test.id, isolation_area=test.id, status=3),
                 'newf0': newf0,
                 'title': test.proname
                 }

    elif f[0] == "f" or f[0] == "F":
        test = Status.objects.filter(tag=f).first()
        users = Demo.objects.filter(status=test.id).exclude(test_result=5)
        p = ''
    elif f[0] == 'L':
        test = TestResult.objects.filter(tag=f).first()
        users = Demo.objects.filter(test_result=test.id)
        p = ''

    else:
        test = TestResult.objects.filter(tag=f).first()
        users = Demo.objects.filter(test_result=test.id).order_by('status')
        p = ''
    return render(request, 'demo/test.html', {'users': users, 'p': p})


def savedb(request, filename):
    import xlrd
    file_extension = os.path.splitext(filename)
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
    for col in sheet:
        # col0:patientcode,#col1:name,#col2:status,#col3:f_status,#col4:phone,
        # #col5:addr,#col6:province,#col7:test_result,#col8:isolation_area
        # check if foreinkey is not exist
        # status
        if not Status.objects.filter(sname=col[2].value):
            # return HttpResponse("<h2>Vui lòng thêm giá trị: "+ col[2].value+" vào bảng status!</h2>")
            status = Status(sname=col[2].value.upper(), tag=slugify(col[2].value))
            status.save()
        # province
        if not Province.objects.filter(slug=slugify(col[6].value)):
            return HttpResponse("<h2>Vui lòng thêm giá trị: " + col[6].value + " vào bảng province!</h2>")

        # check if isolation_area is empty
        if not col[8].value:
            isolation_area = ''
        else:
            isolation_area = Province.objects.filter(slug=slugify(col[8].value)).first().id
        # check if f_status col is empty
        if not col[3].value:
            f_status = ''
        else:
            f_status = Demo.objects.filter(patientcode=col[3].value).first().id
        # check if result col is empty
        if not col[7].value:
            result_id = ''
        # test_result
        elif not TestResult.objects.filter(slug=slugify(col[7].value)):
            return HttpResponse("<h2>Vui lòng thêm giá trị: " + col[7].value + " vào bảng test_result!</h2>")
        else:
            result_id = TestResult.objects.filter(testname=col[7].value)[0].id

        # import demo to DB
        demo = Demo(patientcode=col[0].value,
                    name=col[1].value,
                    status_id=Status.objects.filter(sname=col[2].value)[0].id,
                    f_status_id=f_status,
                    phone=col[4].value,
                    address=col[5].value,
                    province_id=Province.objects.filter(slug=slugify(col[6].value))[0].id,
                    created_at=datetime.today(),
                    expiration=datetime.today() + timedelta(21),
                    test_result_id=result_id,
                    isolation_area_id=isolation_area,
                    )
        demo.save()
    os.remove("uploads/" + filename)
    return HttpResponseRedirect(reverse('demo:index'))


@permission_required('demo.updateStatusF0', raise_exception=True)
def updateStatusF0(request, id):
    f1 = Demo.objects.filter(f_status=id)
    for f2s in f1:
        f2 = Demo.objects.filter(f_status=f2s.id)
        for f3 in f2:
            p = Demo.objects.get(pk=f3.id)
            p.status = "F2"
            p.f_status_id = f2s.id
            p.save()

        p = Demo.objects.get(pk=f2s.id)
        p.status = "F1"
        p.f_status_id = id
        p.save()

    users = Demo.objects.get(pk=id)
    users.status = "F0"
    users.save()
    return HttpResponseRedirect(reverse('demo:index'))


@permission_required('demo.updateStatus', raise_exception=True)
def updateStatus(request, id):
    f1 = Demo.objects.filter(f_status=id)
    for f2s in f1:
        f2 = Demo.objects.filter(f_status=f2s.id)
        for f3 in f2:
            p = Demo.objects.get(pk=f3.id)
            p.testname = 5
            p.save()

        p = Demo.objects.get(pk=f2s.id)
        p.test_result_id = 5
        p.save()

    users = Demo.objects.get(pk=id)
    users.test_result_id = 5
    users.save()
    return HttpResponseRedirect(reverse('demo:index'))
