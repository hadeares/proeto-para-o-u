from django.db import models
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.deletion import PROTECT


class Categoria(models.Model):
    descricao = models.CharField(max_length=255)

    def __str__(self):
        return self.descricao

class Editora(models.Model):
    nome = models.CharField(max_length=255)
    site = models.URLField()

    def __str__(self):
        return self.nome

class Autor(models.Model):
    class Meta:
        verbose_name_plural = "Autores" 

    nome = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome

class Livros(models.Model):
    class Meta:
        verbose_name_plural = "Livros" 
    titulo = models.CharField(max_length=255)
    ISBN = models.CharField(max_length=32)
    quantidade = models.IntegerField()
    preco = models.FloatField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="Livros")
    editora = models.ForeignKey(Editora, on_delete=models.PROTECT, related_name="Livros")
    autores = models.ManyToManyField(Autor, related_name="Livros")
    
    def __str__(self):
        return "%s (%s)" %(self.titulo , self.editora)

class Compra(models.Model):
    
    class StatusCompra(models.IntegerChoices):
        CARRINHO = 1, 'Carrinho'
        REALIZADO = 2, 'Realizado'
        PAGO = 3, 'Pago'
        Entregue = 4, 'Entregue'

    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="compras" )
    status = models.IntegerField(choices=StatusCompra.choices, default=StatusCompra.CARRINHO)

    @property 
    def total(self):
        queryset = self.itens.all().aggregate(
            total=models.Sum(F('quantidade') * F('livro__preco'))
        )

        return queryset["total"]


class ItensCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="itens")
    livro = models.ForeignKey(Livros, on_delete=models.PROTECT, related_name="+")
    quantidade = models.IntegerField()