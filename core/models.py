from django.db import models
from django.utils import timezone
from datetime import timedelta


class Beneficiario(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20)
    endereco = models.CharField(max_length=200)

    recebe_beneficio = models.BooleanField(default=False)
    qual_beneficio = models.CharField(max_length=100, blank=True, null=True)

    documento_foto = models.FileField(
        upload_to='documentos/',
        blank=True,
        null=True
    )

    def pode_receber_cesta(self):
        ultima = self.cestas.order_by('-data').first()
        if ultima and timezone.now() - ultima.data < timedelta(days=30):
            return False, "Este beneficiário já recebeu cesta recentemente."
        return True, ""

    def conceder_cesta(self):
        Cesta.objects.create(beneficiario=self)

    def __str__(self):
        return self.nome


class Cesta(models.Model):
    beneficiario = models.ForeignKey(
        Beneficiario,
        related_name='cestas',
        on_delete=models.CASCADE
    )
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cesta - {self.beneficiario.nome}"
