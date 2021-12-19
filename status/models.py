from django.core import validators
from django.db import models
from django.db.models.deletion import CASCADE, PROTECT
from django.core.validators import MaxValueValidator


class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = 'status'


class Staff(BaseModel):
    is_removed = models.BooleanField()
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    # designation = ?

    def __str__(self):
        return self.name


class Project(BaseModel):
    is_removed = models.BooleanField()
    name = models.CharField(max_length=250)
    client_name = models.CharField(max_length=200)
    client_id = models.CharField(max_length=5)
    assigned_to = models.ForeignKey(Staff, on_delete=PROTECT)
    is_live = models.BooleanField()

    def __str__(self):
        return self.name


class ProgressOfProject(BaseModel):
    project = models.ForeignKey(Project, on_delete=PROTECT)
    drawing = models.CharField(max_length=100)
    progress = models.PositiveIntegerField(validators=[MaxValueValidator(100)])

    def __str__(self):
        return self.project.name + " - " + self.drawing
