from cloudinary_storage.storage import MediaCloudinaryStorage
from django.db import models
from django.utils import timezone
from datetime import date


class Beneficiario(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)

    recebe_beneficio = models.BooleanField(default=False)
    qual_beneficio = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    documento_foto = models.ImageField(
        upload_to='documentos/',
        blank=True,
        null=True
    )

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    def pode_receber_cesta(self):
        hoje = date.today()

        # total de cestas no ano atual
        total_ano = self.cestas.filter(
            data_concessao__year=hoje.year
        ).count()

        if total_ano >= 3:
            return False, "Já recebeu 3 cestas neste ano."

        # última cesta concedida
        ultima = self.cestas.order_by('-data_concessao').first()

        if ultima and ultima.data_concessao.month == hoje.month:
            return False, "Já recebeu cesta este mês."

        return True, "Pode receber cesta."

    def conceder_cesta(self):
        Cesta.objects.create(beneficiario=self)


class Cesta(models.Model):
    beneficiario = models.ForeignKey(
        Beneficiario,
        on_delete=models.CASCADE,
        related_name='cestas'
    )
    data_concessao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cesta - {self.beneficiario.nome} ({self.data_concessao})"
