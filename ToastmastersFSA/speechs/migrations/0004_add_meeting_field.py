from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('speechs', '0003_alter_evaluationanswer_data'),
        ('meetings', '0004_alter_ressources_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluation',
            name='meeting',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                to='meetings.meeting',
                null=True  # Temporairement nullable
            ),
        ),
    ]