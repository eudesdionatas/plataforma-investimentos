from django import forms
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from .models import Operacao, TipoAtivoChoices


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

TIPOS_TODOS = TIPOS_RENDA_VARIAVEL + TIPOS_RENDA_FIXA

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['data'] = date.today()
        self.initial['onde_investir'] = "BOLSA_VALORES"

        self.fields['operacao'].label = 'Operação'
        self.fields['tipo'].label = 'Tipo de Ativo'

        if self.is_bound:
            onde_investir = self.data.get('onde_investir', 'BOLSA_VALORES')
        else:
            onde_investir = self.initial.get('onde_investir', 'BOLSA_VALORES')

        if onde_investir in ONDE_INVESTIR_RENDA_VARIAVEL:
            self.fields['tipo'].choices = TIPOS_RENDA_VARIAVEL
        elif onde_investir in ONDE_INVESTIR_RENDA_FIXA:
            self.fields['tipo'].choices = TIPOS_RENDA_FIXA
        else:
            self.fields['tipo'].choices = TIPOS_TODOS

    def clean_preco_unitario(self):
        return self._parse_money(self.cleaned_data['preco_unitario'], "preço unitário")

    def clean_valor_total(self):
        return self._parse_money(self.cleaned_data['valor_total'], "valor total")

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
            'corretora': forms.Select(attrs={'class': 'form-select'}),
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