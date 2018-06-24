from datetime import datetime
import csv
from django.http import HttpResponse

from django.shortcuts import render
from django_filters import rest_framework
from rest_framework import viewsets, filters

from searchapp.models import User, ApiReport
from searchapp.serializers import UserSerializer




class UserViewSet(viewsets.ModelViewSet):
    """
    Search API endpoint that allows users to be viewed or edited.
    Allows to search Users based on email, date_joined.
    Allows to filter users based on username, email.
    """
    
    serializer_class = UserSerializer
    filter_backends = (rest_framework.DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('email', 'date_joined')
    filter_fields = ('username', 'email')

    def get_queryset(self):
        search_param = self.request.GET.get('search', None)
        if search_param:
            report_obj = ApiReport.objects.create(search_keyword=search_param, 
                api_call_date=datetime.now())
            report_obj.save
        queryset = User.objects.all().order_by('-date_joined')
        return queryset


def generate_report(request):
    """ Generates report with Users count, 
        Search API call count based on day, month, year.
    """
    if request.method == 'POST':
        report_date = request.POST.get('report_date', None)
        report_name = request.POST.get('report_name', 'sample')
        if report_date:
            date_list = report_date.split('-')
            header_list = ['Name', 'Day', 'Month', 'Year']
            user_list = ['User Count', ]
            search_call_list = ['Search API call count', ]
            user_day_count = User.objects.filter(date_joined__day=date_list[0]).count()
            user_month_count = User.objects.filter(date_joined__month=date_list[1]).count()
            user_year_count = User.objects.filter(date_joined__year=date_list[2]).count()
            user_list.extend([user_day_count, user_month_count, user_year_count])
            search_day_count = ApiReport.objects.filter(api_call_date__day=date_list[0]).count()
            search_month_count = ApiReport.objects.filter(api_call_date__month=date_list[1]).count()
            search_year_count = ApiReport.objects.filter(api_call_date__year=date_list[2]).count()
            search_call_list.extend([search_day_count, search_month_count, search_year_count])
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="%s.csv"'%(report_name)
            writer = csv.writer(response)
            writer.writerow(header_list)
            writer.writerow(user_list)
            writer.writerow(search_call_list)
            return response
    return render(request, 'report.html')