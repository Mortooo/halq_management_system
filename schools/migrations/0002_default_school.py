from django.db import migrations


def create_default_school(apps, schema_editor):
    School = apps.get_model('schools', 'School')
    school, _ = School.objects.get_or_create(
        id=1,
        defaults={'name': 'الحلقات الافتراضية', 'address': '', 'tel': ''}
    )

    Teacher = apps.get_model('teachers', 'Teacher')
    Teacher.objects.filter(school__isnull=True).update(school=school)

    Halaqa = apps.get_model('halaqs', 'Halaqa')
    Halaqa.objects.filter(school__isnull=True).update(school=school)

    Grade = apps.get_model('students', 'Grade')
    Grade.objects.filter(school__isnull=True).update(school=school)

    Student = apps.get_model('students', 'Student')
    Student.objects.filter(school__isnull=True).update(school=school)


def create_user_profiles(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('schools', 'UserProfile')

    for user in User.objects.all():
        UserProfile.objects.get_or_create(
            user=user,
            defaults={'school_id': 1}
        )


def forward(apps, schema_editor):
    create_default_school(apps, schema_editor)
    create_user_profiles(apps, schema_editor)


def reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0001_initial'),
        ('teachers', '0004_teacher_school'),
        ('halaqs', '0004_halaqa_school'),
        ('students', '0005_grade_school_student_school'),
    ]

    operations = [
        migrations.RunPython(forward, reverse),
    ]
