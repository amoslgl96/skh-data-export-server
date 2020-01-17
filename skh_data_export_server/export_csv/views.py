import csv

from django.shortcuts import render, HttpResponse
from django.core.mail import EmailMessage
from .models import SensorReading

# Create your views here.
def hello_world(request):
    return render(request, 'hello_world.html', {})


def export_csv(request):

    sensor_readings = SensorReading.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sensor-readings.csv"'

    writer = csv.writer(response, delimiter=',')
    writer.writerow(['day','steps_taken','heart_rate','medication_taken'])

    for reading_obj in sensor_readings:
        writer.writerow([reading_obj.day,reading_obj.steps_taken,reading_obj.heart_rate,reading_obj.medication_taken])
    
    return response