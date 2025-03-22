from django.db import models

class Preparat(models.Model):
    nume = models.CharField(max_length=200)
    descriere = models.TextField()
    data_adaugare = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nume