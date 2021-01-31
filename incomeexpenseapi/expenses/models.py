from django.db import models
from authentication.models import  User

# Create your models here.



class Expense(models.Model):

    CATEGORIES = [
    ('ONLINE_SERVICES', 'ONLINE_SERVICES'), 
    ('TRAVEL', 'TRAVEL'),
    ('FOOD', 'FOOD'),
    ('TRANSPORT', 'TRANSPORT'),
    ('RENT', 'RENT'),
    ('OTHERS', 'OTHERS')
]

    category = models.CharField(max_length=255, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    date_created = models.DateField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name, self.date