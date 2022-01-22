from django.db import models
from django.db.models.deletion import PROTECT
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    class Meta:
        abstract = True
        app_label = 'status'


class User(AbstractUser):
    DESIGNATION = [
        ("Level 1", "Level 1"),
        ("Level 2", "Level 2"),
        ("Level 3", "Level 3")
    ]
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    designation = models.CharField(max_length=10, choices=DESIGNATION)

    def __str__(self):
        return self.name


class Project(BaseModel):
    is_removed = models.BooleanField()
    name = models.CharField(max_length=250)
    client_name = models.CharField(max_length=200)
    client_id = models.CharField(max_length=5)
    assigned_to = models.ForeignKey(User, on_delete=PROTECT)
    is_live = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)


class ProgressOfProject(BaseModel):
    is_removed = models.BooleanField()
    project = models.ForeignKey(Project, on_delete=PROTECT)
    drawing = models.CharField(max_length=100)
    progress = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    image = models.ImageField(upload_to='media/')

    def __str__(self):
        return self.project.name + " - " + self.drawing
