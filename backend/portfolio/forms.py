from django import forms
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from .models import CorretoraChoices, Operacao, TipoAtivoChoices


TIPOS_BOLSA_VALORES = [
    (TipoAtivoChoices.ACAO, TipoAtivoChoices.ACAO.label),
    (TipoAtivoChoices.ACAO_EUA, TipoAtivoChoices.ACAO_EUA.label),
    (TipoAtivoChoices.BDR, TipoAtivoChoices.BDR.label),
    (TipoAtivoChoices.DESPESAS, TipoAtivoChoices.DESPESAS.label),
    (TipoAtivoChoices.DIREITO_SUBSCRICAO, TipoAtivoChoices.DIREITO_SUBSCRICAO.label),
    (TipoAtivoChoices.DOLAR_FUTURO, TipoAtivoChoices.DOLAR_FUTURO.label),
    (TipoAtivoChoices.ETF, TipoAtivoChoices.ETF.label),
    (TipoAtivoChoices.ETF_RENDA_FIXA, TipoAtivoChoices.ETF_RENDA_FIXA.label),
    (TipoAtivoChoices.ETF_USA, TipoAtivoChoices.ETF_USA.label),
    (TipoAtivoChoices.FI_AGRO, TipoAtivoChoices.FI_AGRO.label),
    (TipoAtivoChoices.FII, TipoAtivoChoices.FII.label),
    (TipoAtivoChoices.FUNDOS_ISENTOS, TipoAtivoChoices.FUNDOS_ISENTOS.label),
    (TipoAtivoChoices.FUTUROS_OUTROS, TipoAtivoChoices.FUTUROS_OUTROS.label),
    (TipoAtivoChoices.INDICE_FUTURO, TipoAtivoChoices.INDICE_FUTURO.label),
    (TipoAtivoChoices.JUROS_FUTUROS, TipoAtivoChoices.JUROS_FUTUROS.label),
    (TipoAtivoChoices.MUTUAL_FUNDS_USA, TipoAtivoChoices.MUTUAL_FUNDS_USA.label),
    (TipoAtivoChoices.OPCOES, TipoAtivoChoices.OPCOES.label),
    (TipoAtivoChoices.OPCOES_EUA, TipoAtivoChoices.OPCOES_EUA.label),
    (TipoAtivoChoices.OPCOES_FLEXIVEIS, TipoAtivoChoices.OPCOES_FLEXIVEIS.label),
    (TipoAtivoChoices.OURO_BOLSA, TipoAtivoChoices.OURO_BOLSA.label),
    (TipoAtivoChoices.REIT, TipoAtivoChoices.REIT.label),
    (TipoAtivoChoices.RENDA_FIXA_EUA, TipoAtivoChoices.RENDA_FIXA_EUA.label),
    (TipoAtivoChoices.TERMO, TipoAtivoChoices.TERMO.label),
]

TIPOS_RENDA_FIXA = [
    (TipoAtivoChoices.FUNDO, TipoAtivoChoices.FUNDO.label),
    (TipoAtivoChoices.TITULO_PUBLICO, TipoAtivoChoices.TITULO_PUBLICO.label),
    (TipoAtivoChoices.DEBENTURE, TipoAtivoChoices.DEBENTURE.label),
    (TipoAtivoChoices.CDB, TipoAtivoChoices.CDB.label),
    (TipoAtivoChoices.RDB, TipoAtivoChoices.RDB.label),
    (TipoAtivoChoices.LCI, TipoAtivoChoices.LCI.label),
    (TipoAtivoChoices.LCA, TipoAtivoChoices.LCA.label),
    (TipoAtivoChoices.CRI, TipoAtivoChoices.CRI.label),
    (TipoAtivoChoices.CRA, TipoAtivoChoices.CRA.label),
]

TIPOS_RENDA_VARIAVEL = [
    (TipoAtivoChoices.ACAO, TipoAtivoChoices.ACAO.label),
    (TipoAtivoChoices.FII, TipoAtivoChoices.FII.label),
    (TipoAtivoChoices.ETF, TipoAtivoChoices.ETF.label),
    (TipoAtivoChoices.FUNDO_ACOES, TipoAtivoChoices.FUNDO_ACOES.label),
    (TipoAtivoChoices.FUNDO_MULTIMERCADO, TipoAtivoChoices.FUNDO_MULTIMERCADO.label),
]

TIPOS_TODOS = TIPOS_BOLSA_VALORES + TIPOS_RENDA_VARIAVEL + TIPOS_RENDA_FIXA

ONDE_INVESTIR_CHOICES = [
    ("BOLSA_VALORES", "Bolsa de Valores (BR e EUA)"),
    ("TESOURO_DIRETO", "Tesouro Direto"),
    ("RENDA_FIXA", "Renda Fixa"),
    ("RENDA_FIXA_EUA", "Renda Fixa EUA"),
    ("FUNDOS_INVESTIMENTO", "Fundos de investimento"),
    ("CRIPTOMOEDA", "Criptomoeda"),
    ("CAIXA_CONTA_CORRENTE", "Caixa/Conta corrente"),
    ("OUTROS", "Outros"),
]

ONDE_INVESTIR_RENDA_VARIAVEL = {"BOLSA_VALORES", "FUNDOS_INVESTIMENTO"}
ONDE_INVESTIR_RENDA_FIXA = {"TESOURO_DIRETO", "RENDA_FIXA", "RENDA_FIXA_EUA"}

class OperacaoForm(forms.ModelForm):
    onde_investir = forms.ChoiceField(
        required=True,
        label="Onde investir",
        choices=ONDE_INVESTIR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_onde_investir'}),
    )
    corretora = forms.CharField(
        required=True,
        label="Corretora",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'id': 'id_corretora',
                'list': 'lista_corretoras',
                'autocomplete': 'off',
                'placeholder': 'Selecione da lista ou digite uma corretora',
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['data'] = date.today()
        self.initial['onde_investir'] = "BOLSA_VALORES"
        self.corretora_sugestoes = [choice.label for choice in CorretoraChoices]
        self._corretora_por_nome = {
            choice.label.casefold(): choice.value for choice in CorretoraChoices
        }
        self._corretora_por_codigo = {
            choice.value.casefold(): choice.value for choice in CorretoraChoices
        }

        corretora_inicial = self.initial.get('corretora')
        if corretora_inicial:
            corretora_normalizada = self._corretora_por_codigo.get(str(corretora_inicial).casefold())
            if corretora_normalizada:
                self.initial['corretora'] = CorretoraChoices(corretora_normalizada).label

        self.fields['operacao'].label = 'Operação'
        self.fields['tipo'].label = 'Tipo de Ativo'

        if self.is_bound:
            onde_investir = self.data.get('onde_investir', 'BOLSA_VALORES')
        else:
            onde_investir = self.initial.get('onde_investir', 'BOLSA_VALORES')

        if onde_investir == "BOLSA_VALORES":
            self.fields['tipo'].choices = TIPOS_BOLSA_VALORES
        elif onde_investir in ONDE_INVESTIR_RENDA_VARIAVEL:
            self.fields['tipo'].choices = TIPOS_RENDA_VARIAVEL
        elif onde_investir in ONDE_INVESTIR_RENDA_FIXA:
            self.fields['tipo'].choices = TIPOS_RENDA_FIXA
        else:
            self.fields['tipo'].choices = TIPOS_TODOS

    def clean_preco_unitario(self):
        return self._parse_money(self.cleaned_data['preco_unitario'], "preço unitário")

    def clean_valor_total(self):
        return self._parse_money(self.cleaned_data['valor_total'], "valor total")

    def clean_corretora(self):
        corretora = (self.cleaned_data.get('corretora') or "").strip()
        if not corretora:
            raise forms.ValidationError("Informe a corretora.")

        corretora_por_codigo = self._corretora_por_codigo.get(corretora.casefold())
        if corretora_por_codigo:
            return corretora_por_codigo

        corretora_por_nome = self._corretora_por_nome.get(corretora.casefold())
        if corretora_por_nome:
            return corretora_por_nome

        return corretora

    def clean(self):
        cleaned_data = super().clean()
        quantidade = cleaned_data.get('quantidade')
        valor_total = cleaned_data.get('valor_total')

        if quantidade in (None, 0) or valor_total is None:
            return cleaned_data

        try:
            quantidade_decimal = Decimal(str(quantidade))
            if quantidade_decimal == 0:
                return cleaned_data

            valor_total_decimal = Decimal(str(valor_total))
            cleaned_data['preco_unitario'] = (valor_total_decimal / quantidade_decimal).quantize(
                Decimal('0.000001'), rounding=ROUND_HALF_UP
            )
        except (InvalidOperation, ZeroDivisionError):
            pass

        return cleaned_data

    def _parse_money(self, data, field_name):
        import re
        cleaned = re.sub(r'[^\d.,]', '', str(data)).strip()
        if not cleaned:
            return 0.0
        last_dot = cleaned.rfind('.')
        last_comma = cleaned.rfind(',')
        if last_dot > last_comma:
            # ponto é separador decimal (ex: 1,234.56)
            cleaned = cleaned.replace(',', '')
        elif last_comma > last_dot:
            # vírgula é separador decimal (ex: 1.234,56)
            cleaned = cleaned.replace('.', '').replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            raise forms.ValidationError(f"Valor inválido para {field_name}")

    class Meta:
        model = Operacao
        fields = ['nome_ativo', 'corretora', 'operacao', 'mercado', 'tipo', 'quantidade', 'preco_unitario', 'valor_total', 'moeda', 'data', 'observacao']
        labels = {
            'observacao': 'Observação',
        }
        widgets = {
            'nome_ativo': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nome_ativo'}),
            'operacao': forms.Select(attrs={'class': 'form-select'}),
            'mercado': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_unitario': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_preco_unitario'}),
            'valor_total': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_valor_total'}),
            'moeda': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }