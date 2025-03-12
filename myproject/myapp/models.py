from django.db import models

class Student(models.Model):
    studentID = models.IntegerField(primary_key=True)
    studentName = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    presentDate = models.DateField()

    class Meta:
        db_table = 'students'

    def __str__(self):
        return self.studentName
