import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.utils import IntegrityError

from schools.models import School, UserProfile
from teachers.models import Teacher
from halaqs.models import Halaqa
from students.models import Student, Grade
from attendances.models import StudAttendance, TeachAttendance
from reports.models import WeekReport
from teachers.forms import TeacherForm
from students.forms import StudentForm, GradeForm
from halaqs.forms import HalaqaForm


class BaseTestCase(TestCase):
    """Base setup with multi-tenant fixtures."""

    def setUp(self):
        self.client = Client()

        # Create Schools
        self.school_a = School.objects.create(name="مدرسة النور", tel="0501111111", is_active=True)
        self.school_b = School.objects.create(name="مدرسة الفرقان", tel="0502222222", is_active=True)

        # Create School A Admin (Superuser)
        self.admin_user_a = User.objects.create_superuser(
            username="admin_a", email="admin_a@test.com", password="Password123!"
        )
        self.profile_a = UserProfile.objects.create(user=self.admin_user_a, school=self.school_a)

        # Create School B Admin (Superuser)
        self.admin_user_b = User.objects.create_superuser(
            username="admin_b", email="admin_b@test.com", password="Password123!"
        )
        self.profile_b = UserProfile.objects.create(user=self.admin_user_b, school=self.school_b)

        # Create Teacher in School A
        self.teacher_user_a = User.objects.create_user(
            username="teacher_a", email="teacher_a@test.com", password="Password123!", is_staff=True
        )
        self.teacher_a = Teacher.objects.create(
            name="فاطمة أحمد",
            tel="0503333333",
            email="teacher_a@test.com",
            user_name=self.teacher_user_a,
            school=self.school_a,
        )

        # Create Grade & Halaqa in School A
        self.grade_a = Grade.objects.create(name="المستوى الأول", school=self.school_a)
        self.halaqa_a = Halaqa.objects.create(
            name="حلقة البقرة", res_teacher=self.teacher_a, course="حفظ سورة البقرة", school=self.school_a
        )

        # Create Student in School A
        self.student_a = Student.objects.create(
            name="زيد علي",
            address="الرياض",
            tel="0504444444",
            date_birth=datetime.date(2015, 5, 10),
            halaqa=self.halaqa_a,
            grade=self.grade_a,
            school=self.school_a,
            status=True,
        )


class ModelIntegrityTests(BaseTestCase):
    """Test data integrity, constraints, and business properties."""

    def test_student_attendance_unique_constraint(self):
        """Ensure a student cannot have duplicate attendance records on the same day."""
        today = datetime.date.today()
        StudAttendance.objects.create(student=self.student_a, day=today, status=True)

        with self.assertRaises(IntegrityError):
            StudAttendance.objects.create(student=self.student_a, day=today, status=False)

    def test_teacher_attendance_unique_constraint(self):
        """Ensure a teacher cannot have duplicate attendance records on the same day."""
        today = datetime.date.today()
        TeachAttendance.objects.create(teacher=self.teacher_a, day=today, status=True)

        with self.assertRaises(IntegrityError):
            TeachAttendance.objects.create(teacher=self.teacher_a, day=today, status=False)

    def test_student_age_calculation(self):
        """Verify dynamic age calculation handles birthdays accurately."""
        birth = datetime.date.today().replace(year=datetime.date.today().year - 10)
        student = Student(date_birth=birth)
        self.assertEqual(student.age, 10)

    def test_halaqa_metrics_properties(self):
        """Verify Halaqa total_students and absent calculation."""
        self.assertEqual(self.halaqa_a.total_students, 1)
        StudAttendance.objects.create(student=self.student_a, day=datetime.date.today(), status=False)
        self.assertEqual(self.halaqa_a.total_absent_students, 1)


class FormValidationTests(BaseTestCase):
    """Verify name validation uses exact matching rather than substring collisions."""

    def test_teacher_similar_name_allowed(self):
        """A teacher named 'فاطمة' can be added even if 'فاطمة أحمد' exists."""
        form_data = {
            'name': 'فاطمة',
            'tel': '0512345678',
            'email': 'fatima_new@test.com',
            'address': 'الرياض',
            'username': 'fatima_new',
            'password': 'Password123!',
        }
        form = TeacherForm(data=form_data, school=self.school_a)
        self.assertTrue(form.is_valid(), form.errors)

    def test_teacher_exact_duplicate_name_rejected(self):
        """A teacher with the exact same name within the school is rejected."""
        form_data = {
            'name': 'فاطمة أحمد',
            'tel': '0512345678',
            'email': 'fatima_dup@test.com',
            'address': 'الرياض',
            'username': 'fatima_dup',
            'password': 'Password123!',
        }
        form = TeacherForm(data=form_data, school=self.school_a)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_student_similar_name_allowed(self):
        """A student named 'زيد' can be added even if 'زيد علي' exists."""
        form_data = {
            'name': 'زيد',
            'tel': '0599999999',
            'address': 'مكة',
            'date_birth': datetime.date(2016, 1, 1),
            'halaqa': self.halaqa_a.id,
            'grade': self.grade_a.id,
            'status': True,
        }
        form = StudentForm(data=form_data, school=self.school_a)
        self.assertTrue(form.is_valid(), form.errors)

    def test_register_school_duplicate_name_rejected(self):
        """RegisterSchoolForm rejects school name if it already exists."""
        from schools.views import RegisterSchoolForm
        form_data = {
            'school_name': 'مدرسة النور',  # already exists in setUp
            'school_address': 'الرياض',
            'school_tel': '0501111111',
            'username': 'new_unique_admin',
            'email': 'unique_email@test.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
        }
        form = RegisterSchoolForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('school_name', form.errors)

    def test_teacher_create_view_with_non_default_school_id(self):
        """Ensure TeacherCreate view succeeds when creating teacher in school B without FK error."""
        self.client.login(username="admin_b", password="Password123!")
        url = reverse("administration:add_teacher")
        post_data = {
            'name': 'مريم عبد الله',
            'tel': '0598765432',
            'email': 'maryam@test.com',
            'address': 'جدة',
            'username': 'maryam_teacher',
            'password': 'Password123!',
        }
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)
        teacher = Teacher.objects.filter(name='مريم عبد الله').first()
        self.assertIsNotNone(teacher)
        self.assertEqual(teacher.school, self.school_b)
    def test_login_redirect_for_school_admin(self):
        """School superuser with UserProfile is redirected to administration:dashboard on login."""
        from core.adapter import MyAccountAdapter
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post('/accounts/login/')
        request.user = self.admin_user_a
        adapter = MyAccountAdapter()
        redirect_url = adapter.get_login_redirect_url(request)
        self.assertEqual(redirect_url, reverse('administration:dashboard'))

    def test_login_redirect_for_global_admin(self):
        """Global superuser without UserProfile is redirected to schools:school_list on login."""
        from core.adapter import MyAccountAdapter
        from django.test import RequestFactory
        global_admin = User.objects.create_superuser(
            username="global_admin", email="global@test.com", password="Password123!"
        )
        factory = RequestFactory()
        request = factory.post('/accounts/login/')
        request.user = global_admin
        adapter = MyAccountAdapter()
        redirect_url = adapter.get_login_redirect_url(request)
        self.assertEqual(redirect_url, reverse('schools:school_list'))


class MultiTenancyAndSecurityTests(BaseTestCase):
    """Audit role-based permissions and multi-tenant isolation."""

    def test_unauthenticated_access_redirects(self):
        """Verify unauthorized users are redirected to login."""
        url = reverse("administration:dashboard")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_teacher_cannot_access_superadmin_dashboard(self):
        """Verify staff teachers cannot access the superadmin dashboard."""
        self.client.login(username="teacher_a", password="Password123!")
        url = reverse("administration:dashboard")
        response = self.client.get(url)
        self.assertIn(response.status_code, [302, 404])

    def test_school_admin_isolation(self):
        """Verify Admin A cannot see or manage students from School B."""
        student_b = Student.objects.create(
            name="عمر خالد",
            address="جدة",
            tel="0505555555",
            date_birth=datetime.date(2014, 1, 1),
            school=self.school_b,
            status=True,
        )

        self.client.login(username="admin_a", password="Password123!")
        response = self.client.get(reverse("students:students_manage"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.student_a.name)
        self.assertNotContains(response, student_b.name)


class AttendanceAndReportingWorkflowTests(BaseTestCase):
    """Integration tests for batch attendance and weekly reports."""

    def test_batch_student_attendance_submission(self):
        """Test submitting daily attendance form as teacher."""
        self.client.login(username="teacher_a", password="Password123!")
        url = reverse("attendances:student_attendance", kwargs={"pk": self.teacher_user_a.pk})

        post_data = {
            "student_id": [self.student_a.id],
            f"status_{self.student_a.id}": "True",
            f"notes_{self.student_a.id}": "حاضر في الموعد",
        }
        response = self.client.post(url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        record = StudAttendance.objects.filter(student=self.student_a, day=datetime.date.today()).first()
        self.assertIsNotNone(record)
        self.assertTrue(record.status)
        self.assertEqual(record.notes, "حاضر في الموعد")

    def test_weekly_report_submission_and_redirect(self):
        """Test submitting weekly report redirects via PRG pattern."""
        self.client.login(username="teacher_a", password="Password123!")
        url = reverse("reports:weekly_report")

        post_data = {
            "halaqa": self.halaqa_a.id,
            "progress": "تم حفظ الوجه الأول والثاني",
            "plan_status": "on_track",
        }
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("reports:weekly_report"))

        report = WeekReport.objects.filter(halaqa=self.halaqa_a).first()
        self.assertIsNotNone(report)
        self.assertEqual(report.compare_plan, "on_track")
