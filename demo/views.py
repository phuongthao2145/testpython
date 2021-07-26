from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import permission_required
from django.db.models import Sum, Count
from django.shortcuts import redirect
from pathlib import Path
from .forms import UploadFileForm
from demo.models import *
from slugify import slugify
from datetime import datetime, timedelta
from .config import *
import openpyxl
import os
import django
from django.http import JsonResponse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

date = datetime.today()


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
    f = Demo.objects.filter(f_status=users.id).exclude(test_result=OLDF)
    return render(request, 'demo/detail.html', {'id': users, 'users': f, 'fc': fc})


def upload(f):
    file = open('uploads/' + f.name, 'wb+')
    for chunk in f.chunks():
        file.write(chunk)


def index(request):
    users = Demo.objects.exclude(test_result=OLDF).order_by('id')[::-1]
    p = ''
    return render(request, 'demo/test.html', {'users': users, 'p': p})


def city(request, f):
    # get 1 city by slug
    city = City.objects.filter(slug=f).first()
    # get all district id by city id
    districts_id = District.objects.filter(city_id=city.id).values_list('id', flat=True)
    districts = District.objects.filter(city_id=city.id)
    # get all province in all district
    provinces_id = Province.objects.filter(district__in=districts_id).values_list('id', flat=True)
    demo = Demo.objects.filter(province__in=provinces_id).exclude(test_result=OLDF)
    data = {'f0': demo.filter(status=F0).count(),
            'f1': demo.filter(status=F1).count(),
            'f2': demo.filter(status=F2).count(),
            'f3': demo.filter(status=F3).count(),
            'isolation': demo.filter(isolation_area__in=provinces_id).count(),
            'isolationf1': demo.filter(isolation_area__in=provinces_id, status=F1).count(),
            'isolationf2': demo.filter(isolation_area__in=provinces_id, status=F2).count(),
            'newf': demo.filter(created_at__year=date.year, created_at__month=date.month,
                                created_at__day=date.day).count(),
            'oldf': Demo.objects.filter(province__in=provinces_id, test_result=OLDF).count(),
            'title': city.cityname
            }
    return render(request, 'demo/city.html', {'data': data, 'total': districts})


def district(request, f):
    # get district
    district = District.objects.filter(slug=f).first()
    # get all id province belongs to a district
    province_ids = Province.objects.filter(district=district.id).values_list('id', flat=True)
    # get all trong provinces
    users = Demo.objects.filter(province_id__in=province_ids).exclude(test_result=OLDF)
    if users:
        total = {'f0': users.filter(status=F0).count(),
                 'f1': users.filter(status=F2).count(),
                 'f2': users.filter(status=F2).count(),
                 'f3': users.filter(status=F3).count(),
                 'isolation': users.filter(isolation_area__in=province_ids).count(),
                 'isolationf1': users.filter(isolation_area__in=province_ids, status=F1).count(),
                 'isolationf2': users.filter(isolation_area__in=province_ids, status=F2).count(),
                 'newf': users.filter(province_id__in=province_ids, created_at__year=date.year,
                                      created_at__month=date.month,
                                      created_at__day=date.day).count(),
                 'title': district.disname
                 }
    else:
        total = ''
    queryset = Province.objects.filter(district=district.id)
    detail = []
    for i in queryset:
        users = Demo.objects.filter(province=i.id).exclude(test_result=OLDF)
        detail.append({'f0': users.filter(status=F0).count(),
                       'f1': users.filter(status=F1).count(),
                       'f2': users.filter(status=F2).count(),
                       'f3': users.filter(status=F3).count(),
                       'isolation': users.filter(isolation_area=i.id).count(),
                       'isolationf1': users.filter(isolation_area=i.id, status=F1).count(),
                       'isolationf2': users.filter(isolation_area=i.id, status=F2).count(),
                       'newf': users.filter(province_id=i.id, created_at__year=date.year, created_at__month=date.month,
                                            created_at__day=date.day).count(),
                       'extra': i,
                       })
    # for chart
    labels = []
    combo = [['Name', 'Số ca dương tính', 'Số ca nhiễm mới']]
    for entry in queryset:
        labels.append(entry.proname)
        d = Demo.objects.filter(created_at__year=date.year, created_at__month=date.month,
                                created_at__day=date.day, province=entry.id).annotate(Count('created_at'))
        d1 = Demo.objects.filter(status=F0, province=entry.id).annotate(Count('status'))
        pp = [entry.proname, d1.count(), d.count()]
        combo.append(pp)
    return render(request, 'demo/district.html',
                  {'total': total, 'detail': detail, 'combo': combo})


def province(request, f):
    test = Province.objects.filter(slug=f).first()
    users = Demo.objects.filter(province=test.id).exclude(test_result=OLDF).order_by('status')
    data = {'f0': users.filter(status=F0).exclude(test_result=OLDF).count(),
            'f1': users.filter(status=F1).exclude(test_result=OLDF).count(),
            'f2': users.filter(status=F2).exclude(test_result=OLDF).count(),
            'f3': users.filter(status=F3).exclude(test_result=OLDF).count(),
            'isolation': users.filter(isolation_area=test.id).exclude(test_result=OLDF).count(),
            'isolationf1': users.filter(isolation_area=test.id, status=F1).exclude(test_result=OLDF).count(),
            'isolationf2': users.filter(isolation_area=test.id, status=F3).exclude(test_result=OLDF).count(),
            'newf': users.filter(created_at__year=date.year, created_at__month=date.month,
                                 created_at__day=date.day).count(),
            'title': test.proname
            }
    return render(request, 'demo/test.html', {'users': users, 'data': data})


def view(request, f):
    if f=="h":
        users = Demo.objects.filter(test_result=OLDF).order_by('updated_at')[::-1]
    else:
        test = Status.objects.filter(tag=f).first()
        users = Demo.objects.filter(status=test.id).exclude(test_result=OLDF).order_by('updated_at')[::-1]
    return render(request, 'demo/test.html', {'users': users, 'data': ''})


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
            return HttpResponse("<h2>Vui lòng thêm giá trị: " + col[2].value + " vào bảng status!</h2>")
            # status = Status(sname=col[2].value.upper(), tag=slugify(col[2].value))
            # status.save()
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
   #update F1
    f1 = Demo.objects.filter(id=id).first()
    Demo.objects.filter(id=id).update(status=F0)
    #update F2
    Demo.objects.filter(f_status=id).update(status=F1)
   # update F3
    f2s = Demo.objects.filter(f_status=id).values_list('id', flat=True)
    Demo.objects.filter(f_status__in=f2s).update(status=F2)
    return HttpResponseRedirect(reverse('demo:detail',args=[f1.patientcode]))


@permission_required('demo.updateStatus', raise_exception=True)
def updateStatus(request, id):
    f1 = Demo.objects.filter(id=id).first()
    # update F1
    Demo.objects.filter(id=id).update(test_result=OLDF)
    # update F2
    Demo.objects.filter(f_status=id).update(test_result=OLDF)
    # update F3
    f2s = Demo.objects.filter(f_status=id).values_list('id', flat=True)
    Demo.objects.filter(f_status__in=f2s).update(test_result=OLDF)
    return HttpResponseRedirect(reverse('demo:detail',args=[f1.patientcode]))
