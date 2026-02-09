from django.db import models
from datetime import date
from cloudinary.models import CloudinaryField


class Beneficiario(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)

    documento_foto = CloudinaryField(
        "Documento",
        resource_type="auto",
        blank=True,
        null=True)

    recebe_beneficio = models.BooleanField(default=False)
    qual_beneficio = models.CharField(max_length=150, blank=True, null=True)

    documento_foto = models.ImageField(upload_to='documentos/', blank=True, null=True)

    total_cestas_ano = models.PositiveIntegerField(default=0)
    data_ultima_cesta = models.DateField(blank=True, null=True)

    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

    def pode_receber_cesta(self):
        hoje = date.today()

        # Limite anual
        if self.total_cestas_ano >= 3:
            return False, "Já recebeu 3 cestas neste ano."

        # Não pode receber no mês seguinte ao último
        if self.data_ultima_cesta:
            if self.data_ultima_cesta.year == hoje.year:
                if abs(hoje.month - self.data_ultima_cesta.month) <= 1:
                    return False, "Precisa aguardar o próximo mês."

        return True, "Pode receber cesta."

    def conceder_cesta(self):
        self.total_cestas_ano += 1
        self.data_ultima_cesta = date.today()
        self.save()


class Cesta(models.Model):
    beneficiario = models.ForeignKey(
        'Beneficiario',
        on_delete=models.CASCADE,
        related_name='cestas'
    )
    data_concessao = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Cesta - {self.beneficiario.nome}"
