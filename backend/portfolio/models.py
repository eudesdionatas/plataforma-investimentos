from django.db import models


class ClasseAtivoChoices(models.TextChoices):
    RENDA_FIXA = "RENDA_FIXA", "Renda Fixa"
    RENDA_VARIAVEL = "RENDA_VARIAVEL", "Renda Variavel"


class TipoAtivoChoices(models.TextChoices):
    ACAO = "ACAO", "Ação"
    FII = "FII", "FII"
    STOCK = "STOCK", "Stock"
    REIT = "REIT", "REIT"
    ETF = "ETF", "ETF"
    TITULO_PUBLICO = "TITULO_PUBLICO", "Título Público"
    TITULO_PRIVADO = "TITULO_PRIVADO", "Título Privado"
    CDB = "CDB", "CDB"


class MercadoChoices(models.TextChoices):
    AVISTA = "AVISTA", "À vista"
    FRACIONARIO = "FRACIONARIO", "Fracionário"


class TipoOperacaoChoices(models.TextChoices):
    COMPRA = "COMPRA", "Compra"
    VENDA = "VENDA", "Venda"


class TamanhoAtivoChoices(models.TextChoices):
    SMALL = "SMALL", "Smallcap"
    MID = "MID", "Midcap"
    LARGE = "LARGE", "Largecap"


class Ativo(models.Model):
    classe = models.CharField(max_length=20, choices=ClasseAtivoChoices.choices)
    tipo = models.CharField(max_length=20, choices=TipoAtivoChoices.choices)
    nome = models.CharField(max_length=150)
    ticker = models.CharField(max_length=20, unique=True)
    aporte = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    custo = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    quantidade = models.DecimalField(max_digits=18, decimal_places=6, default=0)
    preco_medio_ajustado = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    tamanho = models.CharField(max_length=10, choices=TamanhoAtivoChoices.choices, blank=True)
    setor = models.CharField(max_length=100, blank=True)
    preco_medio = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    posicao_anterior = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_janeiro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_fevereiro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_marco = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_abril = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_maio = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_junho = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_julho = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_agosto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_setembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_outubro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_novembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    posicao_dezembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_anterior = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_janeiro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_fevereiro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_marco = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_abril = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_maio = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_junho = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_julho = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_agosto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_setembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_outubro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_novembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    valorizacao_dezembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_anterior = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_janeiro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_fevereiro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_marco = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_abril = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_maio = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_junho = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_julho = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_agosto = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_setembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_outubro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_novembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    lucro_dezembro = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    rentabilidade_anterior = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_janeiro = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_fevereiro = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_marco = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_abril = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_maio = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_junho = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_julho = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_agosto = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_setembro = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_outubro = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_novembro = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    rentabilidade_dezembro = models.DecimalField(max_digits=8, decimal_places=4, default=0)

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"

    def __str__(self):
        return f"{self.ticker} - {self.nome}"


class MoedaChoices(models.TextChoices):
    BRL = "BRL", "Real Brasileiro (BRL)"
    USD = "USD", "Dólar Americano (USD)"
    EUR = "EUR", "Euro (EUR)"
    GBP = "GBP", "Libra Esterlina (GBP)"
    JPY = "JPY", "Iene Japonês (JPY)"
    CAD = "CAD", "Dólar Canadense (CAD)"
    AUD = "AUD", "Dólar Australiano (AUD)"
    CHF = "CHF", "Franco Suíço (CHF)"
    CNY = "CNY", "Yuan Chinês (CNY)"
    SEK = "SEK", "Coroa Sueca (SEK)"
    ARS = "ARS", "Peso Argentino (ARS)"
    CLP = "CLP", "Peso Chileno (CLP)"
    MXN = "MXN", "Peso Mexicano (MXN)"
    PEN = "PEN", "Sol Peruano (PEN)"
    COP = "COP", "Peso Colombiano (COP)"
    UYU = "UYU", "Peso Uruguaio (UYU)"
    PYG = "PYG", "Guarani Paraguaio (PYG)"
    BOB = "BOB", "Boliviano (BOB)"
    VEF = "VEF", "Bolívar Venezuelano (VEF)"
    KRW = "KRW", "Won Sul-Coreano (KRW)"
    INR = "INR", "Rupia Indiana (INR)"
    RUB = "RUB", "Rublo Russo (RUB)"
    ZAR = "ZAR", "Rand Sul-Africano (ZAR)"
    TRY = "TRY", "Lira Turca (TRY)"
    SGD = "SGD", "Dólar de Singapura (SGD)"
    HKD = "HKD", "Dólar de Hong Kong (HKD)"
    NZD = "NZD", "Dólar Neozelandês (NZD)"
    NOK = "NOK", "Coroa Norueguesa (NOK)"
    DKK = "DKK", "Coroa Dinamarquesa (DKK)"
    PLN = "PLN", "Złoty Polonês (PLN)"
    CZK = "CZK", "Coroa Tcheca (CZK)"
    HUF = "HUF", "Forint Húngaro (HUF)"
    ILS = "ILS", "Shekel Israelense (ILS)"
    EGP = "EGP", "Libra Egípcia (EGP)"


class CorretoraChoices(models.TextChoices):
    XP = "XP", "XP Investimentos"
    RICO = "RICO", "Rico Investimentos"
    CLEAR = "CLEAR", "Clear Corretora"
    MODALMAIS = "MODALMAIS", "Modalmais"
    TORO = "TORO", "Toro Investimentos"
    EASYNVEST = "EASYNVEST", "Easynvest"
    GUIDE = "GUIDE", "Guide Investimentos"
    ORAMA = "ORAMA", "Órama"
    SANTANDER = "SANTANDER", "Santander Corretora"
    BRADESCO = "BRADESCO", "Bradesco Corretora"
    ITAU = "ITAU", "Itaú Corretora"
    BTG = "BTG", "BTG Pactual"
    BB = "BB", "Banco do Brasil"
    CAIXA = "CAIXA", "Caixa Econômica Federal"
    SAFRA = "SAFRA", "Safra Corretora"
    AVENUE = "AVENUE", "Avenue Securities"
    FIDELITY = "FIDELITY", "Fidelity Investments"
    SCHWAB = "SCHWAB", "Charles Schwab"
    TDAMERITRADE = "TDAMERITRADE", "TD Ameritrade"
    ETRADE = "ETRADE", "E*TRADE"
    VANGUARD = "VANGUARD", "Vanguard"
    MERRILL = "MERRILL", "Merrill Lynch"
    WELLSFARGO = "WELLSFARGO", "Wells Fargo"
    JPMORGAN = "JPMORGAN", "JPMorgan Chase"
    GOLDMAN = "GOLDMAN", "Goldman Sachs"
    MORGAN = "MORGAN", "Morgan Stanley"
    CREDIT = "CREDIT", "Credit Suisse"


class Operacao(models.Model):
    nome_ativo = models.CharField(max_length=150, verbose_name="Nome do Ativo", blank=True, default="")
    corretora = models.CharField(max_length=20, choices=CorretoraChoices.choices, default=CorretoraChoices.XP)
    compra_venda = models.CharField(max_length=10, choices=TipoOperacaoChoices.choices, default=TipoOperacaoChoices.COMPRA, verbose_name="Negociação")
    mercado = models.CharField(max_length=20, choices=MercadoChoices.choices, default=MercadoChoices.AVISTA)
    tipo = models.CharField(max_length=20, choices=TipoAtivoChoices.choices, default=TipoAtivoChoices.ACAO)
    quantidade = models.DecimalField(max_digits=18, decimal_places=6)
    preco_unitario = models.DecimalField(max_digits=14, decimal_places=6, verbose_name="Preço unitário")
    valor_total = models.DecimalField(max_digits=14, decimal_places=2)
    moeda = models.CharField(max_length=3, choices=MoedaChoices.choices, default='BRL', verbose_name='Moeda')
    data = models.DateField()
    observacao = models.TextField(blank=True)

    class Meta:
        verbose_name = "Operacao"
        verbose_name_plural = "Operacoes"
        ordering = ["-data", "-id"]

    def __str__(self):
        return f"{self.compra_venda} - {self.ticker} - {self.data}"


class Provento(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.PROTECT, related_name="proventos")
    tipo = models.CharField(max_length=20, choices=TipoAtivoChoices.choices)
    data_com = models.DateField()
    data_pagamento = models.DateField()
    quantidade = models.DecimalField(max_digits=18, decimal_places=6)
    valor_unitario = models.DecimalField(max_digits=14, decimal_places=6)
    total = models.DecimalField(max_digits=14, decimal_places=2)
    preco_medio = models.DecimalField(max_digits=14, decimal_places=6, default=0)
    yoc = models.DecimalField(max_digits=8, decimal_places=4, default=0, verbose_name="YoC")
    liquido = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    ano = models.PositiveIntegerField()
    mes = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = "Provento"
        verbose_name_plural = "Proventos"
        ordering = ["-data_pagamento", "-id"]

    def __str__(self):
        return f"{self.ativo.ticker} - {self.data_pagamento}"
