from ast import Mod
from dataclasses import fields
from email.policy import default
from turtle import RawTurtle
from core.models import Categoria, Editora, Autor, Livros, Compra, ItensCompra
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField
from rest_framework import serializers


class CategoriaSerializer(ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class EditoraSerializer(ModelSerializer):
    class Meta:
        model = Editora
        fields = '__all__'

class EditoraNestedSerializer(ModelSerializer):
    class Meta:
        model = Editora
        fields = ("nome",)

class AutorSerializer(ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class LivrosSerializer(ModelSerializer):
    class Meta:
        model = Livros
        fields = '__all__'

class LivrosDatailSerializer(ModelSerializer):
    categoria = CharField(source="categira.descricao")
    Editora = EditoraNestedSerializer()
    autores = SerializerMethodField()

    class Meta:
        model = Livros
        fields = '__all__'
        depth = 1

    def get_autores(self, instance):
        nomes_autores = []
        autores = instance .autores.get_queryset()
        for autor in autores:
            nomes_autores.append(autor.nome)
            return nomes_autores


class ItensCompraSerializer(ModelSerializer):
    class meta:
        model = ItensCompra
        fields = ("livro", "quantidade", "total")
        depth = 1

    def get_total(self, instance):
        return instance.quantidade * instance.livro.preco

class CompraSerializer(ModelSerializer):
    usuario = CharField(source="usuario.email")
    status = SerializerMethodField()
    itens = ItensCompraSerializer(many=True)
    
    class meta:
        model = Compra
        fields = ("id", "status", "usuario","itens","total")
        
    def get_status(self, instance):
        return instance.get_status.display()

class CriarEditarIntesCompraSerializer(ModelSerializer):
    class meta:
        model = ItensCompra
        fields = ('livro', 'quantidade')


    def validate(self, data):
        if data['quantaidade'] > data['livro'].quantidade:
            raise serializers.ValidationError({
                'quantidade': 'Quantidade solicitada não disponivel em estoque'
            })
        return data


class CriarEditarCompraSerializer(ModelSerializer):
    itens = ItensCompraSerializer(many=True)
    usuario = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class meta:
        model = Compra
        fields = ('usuario', 'itens')

        
    
    def Create(self, validated_data):
        itens = validated_data.pop('itens')
        compra = Compra.objects.create(**validated_data)
        for item in itens:
            ItensCompra.objects.create(compra=compra, **item)
        compra.save()
        return compra


    def update(self, instance, valideted_data):
        itens = valideted_data.pop('itens')
        if itens:
            instance.itens.all().delete()
            for item in itens:
                itens.objects.create(compra=instance, **item)
            instance.save()
        return instance