import os
from typing import List
from datetime import date 
import importlib

from django.contrib.auth.models import User 
from django.db.models import JSONField,IntegerField,CharField,ForeignKey,Model,BooleanField
from django.db.models import ManyToManyField,OneToOneField,CASCADE,DateField,TextField
from django.core.validators import MinValueValidator,MaxValueValidator

from annoying.fields import AutoOneToOneField

from cartographer.services import getQuarter,quarterRange,today
from lib.onlyoneactive import OnlyOneActive

class WaiverText(OnlyOneActive,Model):
    content = TextField(default="ENTER A WAIVER TEXT HERE",null=False)
    def __str__(self):
        return self.content[:50]+"..."


class Country(Model):
    class Meta:
        verbose_name_plural = "countries"

    gwno = IntegerField(null = False,primary_key=True)
    name = CharField(max_length = 150, null = False)
    iso2c = CharField(max_length=2,null = True)
    active = BooleanField(default=False)

    shape = JSONField(null = False)
    simpleshape = JSONField(null=False)

    def __str__(self):
        return f"{self.gwno} - {self.name}"

class Profile(Model):
    meta = JSONField(default = dict, null = True, blank = True)
    user = AutoOneToOneField(User,on_delete=CASCADE)
    countries = ManyToManyField(Country,related_name="assignees")

    waiver = BooleanField(default = False)

    last_mailed = DateField(default = None, null = True, blank = True)
    unsubscribed = BooleanField(default = False)

    def __str__(self):
        return f"profile of {self.user.username}" # pylint: disable=no-member

class ProjectDescription(OnlyOneActive,Model):
    title = CharField(max_length = 128)
    description = TextField()
    long_description = TextField()

    def __str__(self):
        return "Project description"

class Answer(Model):
    """
    A model that does two things:
    
        Firstly, it handles the date attribute similarly to auto_now_add,
        except that the attribute is overrideable. This is important for
        testing, since I really need to simulate answers given some time ago.

        Secondly, it allows you to define mutex-models, which means that
        only instances from a given model in the mutex can exist from 
        the same author, for the same project, in the given quarter.

        This means that you won't get situations where there are both non-answers
        and shapes, for instance.

    """
    class Meta:
        abstract = True

    date = DateField(null=False)
    author = ForeignKey(User,on_delete=CASCADE,null=False)
    country = ForeignKey(Country,on_delete=CASCADE,null=False)

    mutex: List[Model] = []

    @property
    def quarter(self):
        return getQuarter(self.date)

    @property
    def year(self):
        return self.date.year

    def save(self,*args,**kwargs):
        if self.pk is None and self.date is None:
            self.date = today() 

        s,e = quarterRange(self.date)
        for model in self.mutex:
            if type(model) is str:
                module,model = os.path.splitext(model)
                model = model[1:]
                model = getattr(importlib.import_module(module),model)
            else:
                pass
            others = model.objects.filter(
                    author=self.author,
                    country=self.country,
                    date__gte=s,date__lte=e)
            others.delete()

        super().save(*args,**kwargs)

class Shape(Answer):
    mutex=["api.models.NonAnswer"]

    #Name collision
    country = ForeignKey(Country,related_name="Shapes",on_delete=CASCADE,null=False)

    shape =  JSONField(null = False, blank = False)
    values = JSONField(default = dict, blank = True)

    null_prediction = BooleanField(default = False, blank=True)

    def __str__(self):
        return f"Shape {self.quarter}/{self.year}@{self.country.name}"

    def save(self,*args,**kwargs):
        s,e = quarterRange(self.date)
        nas = NonAnswer.objects.filter(
                author=self.author,
                country=self.country,
                date__gte=s,
                date__lte=e
                )

        if nas:
            nas.delete()

        super().save(*args,**kwargs)

class NonAnswer(Answer):
    mutex=["api.models.Shape"]

    def __str__(self):
        return f"Nonanswer {self.quarter}/{self.year}@{self.country.name}"

class Feedback(Model):
    author = ForeignKey(User,on_delete=CASCADE,null=False)
    message = TextField()
    stars = IntegerField(default=3,
            validators = [
                MinValueValidator(1),
                MaxValueValidator(5),
                ])

