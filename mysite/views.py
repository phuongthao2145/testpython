from sample_app.models import Company, Job
from django.shortcuts import redirect
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
class ParseExcel(APIView):
def post(self, request, format=None):
try:
excel_file = request.FILES[‘files’]
except MultiValueDictKeyError:
return redirect(<your_upload_file_failed_url>)
if (str(excel_file).split(‘.’)[-1] == “xls”):
data = xls_get(excel_file, column_limit=4)
elif (str(excel_file).split(‘.’)[-1] == “xlsx”):
data = xlsx_get(excel_file, column_limit=4)
else:
return redirect(<your_upload_file_fail_url>)
companies = data[“Company”]
jobs = data[“Job”]
if (len(companies) > 1): # We have company data
for company in companies:
if (len(company) > 0): # The row is not blank
# This is not header
if (company[0] != “No”):
# Fill ending columns with blank
if (len(company) < 4):
i = len(company)
while (i < 4):
company.append(“”)
i+=1
# Check if company exist
# Assume that company name is unique
name = company[1]
c = Company.objects.filter(name=name)
if ( c.count() == 0):
Company.objects.create(
name= company[1],
address= company[2],
kind= company[3]
)
for job in jobs:
if (len(job) > 0): # The row is not blank
if (job[0] != “No”): # This is not header
# Get company that own this job
comp_id = int(job[-1])]
name = companies[comp_id][1]
c = Company.objects.filter(name=name)
if (c.count() > 0): # Company exist
Job.objects.create(
company=c[0],
name= job[1],
salary= int(job[2])
)