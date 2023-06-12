# Generated by Django 4.2.2 on 2023-06-09 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="rol",
            name="usuarios",
            field=models.ManyToManyField(
                through="tasks.Usuario_Rol", to="tasks.usuario"
            ),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="cliente",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="usuarios",
                to="tasks.cliente",
            ),
        ),
        migrations.AlterField(
            model_name="usuario_rol",
            name="usuario",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="roles",
                to="tasks.usuario",
            ),
        ),
    ]