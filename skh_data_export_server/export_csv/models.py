from django.db import models

# Create your models here.

class SensorReading(models.Model):

    
    day = models.IntegerField(blank=True, null=True)
    steps_taken = models.IntegerField(blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    medication_taken = models.BooleanField(default=False)


"""
 To convert to python scripts for bulk insert:
 
 For now inserting via command line:
 SensorReading.objects.bulk_create([SensorReading(day=1,steps_taken=2,heart_rate=3,medication_taken=True),
 SensorReading(day=2,steps_taken=2,heart_rate=3,medication_taken=True),
 SensorReading(day=3,steps_taken=2,heart_rate=3,medication_taken=True),
 SensorReading(day=4,steps_taken=2,heart_rate=3,medication_taken=True),
 SensorReading(day=5,steps_taken=2,heart_rate=3,medication_taken=True),
 SensorReading(day=6,steps_taken=2,heart_rate=3,medication_taken=True)]
)


"""