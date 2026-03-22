from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0016_alter_operacao_operacao"),
    ]

    operations = [
        migrations.AlterField(
            model_name="operacao",
            name="corretora",
            field=models.CharField(default="XP", max_length=20),
        ),
    ]
