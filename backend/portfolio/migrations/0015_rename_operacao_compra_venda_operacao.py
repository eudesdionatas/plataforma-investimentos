from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0014_remove_operacao_descricao_alter_ativo_tipo_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="operacao",
            old_name="compra_venda",
            new_name="operacao",
        ),
        migrations.AlterField(
            model_name="operacao",
            name="operacao",
            field=models.CharField(
                choices=[("COMPRA", "Compra"), ("VENDA", "Venda")],
                default="COMPRA",
                max_length=10,
                verbose_name="Operação",
            ),
        ),
    ]