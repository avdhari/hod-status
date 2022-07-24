from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import PROTECT
from django.utils.text import slugify
from django.core.validators import MaxValueValidator
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
    phone = models.CharField(max_length=10, blank=True)
    designation = models.CharField(max_length=10, choices=DESIGNATION, blank=True)

    def __str__(self):
        return self.name


class Project(BaseModel):
    STATUS_TYPE = [
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('done', 'Done!')
    ]
    is_removed = models.BooleanField(default=False)
    name = models.CharField(max_length=250)
    client_name = models.CharField(max_length=200)
    client_id = models.CharField(max_length=5)
    assigned_to = models.ForeignKey(User, on_delete=PROTECT)
    status = models.CharField(max_length=25, choices=STATUS_TYPE)
    slug = models.SlugField(blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField()

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)

    def get_remaining_days(self):
        today = date.today()
        delta = self.deadline - today
        btn_color = ''
        if delta.days > 2:
            btn_color = '#00B74A'
        elif delta.days == 2:
            btn_color = '#FFA900'
        else:
            btn_color = '#F93154'
        return btn_color


class ProgressOfProject(BaseModel):
    is_removed = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=PROTECT)
    drawing = models.CharField(max_length=100)
    progress = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    image = models.ImageField(null=True, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project.name + " - " + self.drawing
