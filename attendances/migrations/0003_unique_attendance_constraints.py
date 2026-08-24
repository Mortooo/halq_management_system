from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendances', '0002_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='studattendance',
            constraint=models.UniqueConstraint(fields=('student', 'day'), name='unique_student_day_attendance'),
        ),
        migrations.AddConstraint(
            model_name='teachattendance',
            constraint=models.UniqueConstraint(fields=('teacher', 'day'), name='unique_teacher_day_attendance'),
        ),
    ]
