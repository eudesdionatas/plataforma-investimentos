from django import forms
from datetime import date
from .models import Operacao

class OperacaoForm(forms.ModelForm):
    is_renda_variavel = forms.BooleanField(required=False, label="Renda Variável", widget=forms.CheckboxInput(attrs={'id': 'id_is_renda_variavel'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['data'] = date.today()
        self.initial['is_renda_variavel'] = True

    def clean_preco_unitario(self):
        data = self.cleaned_data['preco_unitario']
        # Parse formatted currency
        import re
        data = re.sub(r'[^\d.,-]', '', data).replace(',', '.')
        try:
            return float(data)
        except ValueError:
            raise forms.ValidationError("Valor inválido para preço unitário")

    def clean_valor_total(self):
        data = self.cleaned_data['valor_total']
        # Parse formatted currency
        import re
        data = re.sub(r'[^\d.,-]', '', data).replace(',', '.')
        try:
            return float(data)
        except ValueError:
            raise forms.ValidationError("Valor inválido para valor total")

    class Meta:
        model = Operacao
        fields = ['nome_ativo', 'corretora', 'compra_venda', 'mercado', 'tipo', 'descricao', 'quantidade', 'preco_unitario', 'valor_total', 'moeda', 'data', 'observacao']
        widgets = {
            'nome_ativo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o Ticker', 'id': 'id_nome_ativo'}),
            'corretora': forms.Select(attrs={'class': 'form-select'}),
            'compra_venda': forms.Select(attrs={'class': 'form-select'}),
            'mercado': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_descricao'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_unitario': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_preco_unitario'}),
            'valor_total': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_valor_total'}),
            'moeda': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }