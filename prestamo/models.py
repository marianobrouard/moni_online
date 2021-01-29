from django.db import models


class Prestamo(models.Model):
    genero_choice = (
        ('0', 'MASCULINO'),
        ('1', 'FEMENINO'),
    )
    dni = models.IntegerField(primary_key=True,null=False,blank=False)
    nombre = models.CharField(max_length=100,null=False,blank=False)
    apellido = models.CharField(max_length=100,null=False,blank=False)
    genero = models.CharField(max_length=1, choices=genero_choice)
    email = models.EmailField(null=False,blank=False)
    monto_solicitado = models.DecimalField(max_digits=60, decimal_places=2)
    aprobado = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return str(self.dni) + '-' + self.nombre + '-' + self.apellido + '-' + str(self.monto_solicitado) + self.aprobado