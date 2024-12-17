
from django.db.models import Model,BooleanField

class OnlyOneActive(Model):
    active = BooleanField(default=False,help_text="Is this model active? Only one model should be active.")

    class Meta:
        abstract = True

    def save(self,*args,**kwargs):
        if self.active:
            qs = type(self).objects.all().filter(active=True)

            if self.pk:
                qs.exclude(pk = self.pk)

            qs.update(active=False)
        super().save(*args,**kwargs)
