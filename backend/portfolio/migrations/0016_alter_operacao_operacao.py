from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0015_rename_operacao_compra_venda_operacao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operacao",
            name="operacao",
            field=models.CharField(
                choices=[
                    ("SUBSCRICAO", "Subscrição"),
                    ("BONIFICACAO", "Bonificação"),
                    ("COMPRA", "Compra"),
                    ("VENDA", "Venda"),
                    ("IPO", "IPO"),
                    ("TAXAS", "Taxas"),
                    ("PROVENTOS_SOBRAS", "Proventos/Sobras"),
                    ("CASHOUT", "Cashout"),
                    ("AJUSTAR_QUANTIDADE", "Ajustar quantidade"),
                    ("AJUSTAR_PRECO_MEDIO", "Ajustar preço médio"),
                ],
                default="COMPRA",
                max_length=25,
                verbose_name="Operação",
            ),
        ),
    ]
