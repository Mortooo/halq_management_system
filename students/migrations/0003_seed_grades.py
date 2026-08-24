from django.db import migrations

GRADES = [
    'الصف الأول الابتدائي',
    'الصف الثاني الابتدائي',
    'الصف الثالث الابتدائي',
    'الصف الرابع الابتدائي',
    'الصف الخامس الابتدائي',
    'الصف السادس الابتدائي',
    'الصف الأول المتوسط',
    'الصف الثاني المتوسط',
    'الصف الثالث المتوسط',
    'الصف الأول الثانوي',
    'الصف الثاني الثانوي',
    'الصف الثالث الثانوي',
]


def seed_grades(apps, schema_editor):
    Grade = apps.get_model('students', 'Grade')
    for name in GRADES:
        Grade.objects.get_or_create(name=name)


def unseed_grades(apps, schema_editor):
    Grade = apps.get_model('students', 'Grade')
    Grade.objects.filter(name__in=GRADES, student__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_alter_student_halaqa'),
    ]

    operations = [
        migrations.RunPython(seed_grades, unseed_grades),
    ]
