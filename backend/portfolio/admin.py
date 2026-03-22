from django.contrib import admin

from .models import Ativo, Operacao, Provento


@admin.register(Ativo)
class AtivoAdmin(admin.ModelAdmin):
    list_display = ("ticker", "nome", "classe", "tipo", "quantidade", "preco_medio")
    search_fields = ("ticker", "nome", "setor")
    list_filter = ("classe", "tipo", "tamanho")


@admin.register(Operacao)
class OperacaoAdmin(admin.ModelAdmin):
    list_display = ("data", "nome_ativo", "operacao", "mercado", "quantidade", "valor_total")
    search_fields = ("nome_ativo", "corretora")
    list_filter = ("operacao", "mercado", "tipo", "moeda")


@admin.register(Provento)
class ProventoAdmin(admin.ModelAdmin):
    list_display = ("ativo", "tipo", "data_com", "data_pagamento", "total", "liquido")
    search_fields = ("ativo__ticker", "ativo__nome")
    list_filter = ("tipo", "ano", "mes")
