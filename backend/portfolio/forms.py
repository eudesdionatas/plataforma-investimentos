from django import forms
from datetime import date
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from .models import Operacao

class OperacaoForm(forms.ModelForm):
    is_renda_variavel = forms.BooleanField(required=False, label="Renda Variável", widget=forms.CheckboxInput(attrs={'id': 'id_is_renda_variavel'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['data'] = date.today()
        self.initial['is_renda_variavel'] = True

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
        fields = ['nome_ativo', 'corretora', 'compra_venda', 'mercado', 'tipo', 'quantidade', 'preco_unitario', 'valor_total', 'moeda', 'data', 'observacao']
        labels = {
            'observacao': 'Observação',
        }
        widgets = {
            'nome_ativo': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nome_ativo'}),
            'corretora': forms.Select(attrs={'class': 'form-select'}),
            'compra_venda': forms.Select(attrs={'class': 'form-select'}),
            'mercado': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_unitario': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_preco_unitario'}),
            'valor_total': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_valor_total'}),
            'moeda': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }