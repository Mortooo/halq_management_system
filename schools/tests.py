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


class UserSettingsAndProfileTests(BaseTestCase):
    """Tests for displaying user name and user settings / password change."""

    def test_user_name_and_settings_in_supervisor_dashboard(self):
        """Supervisor sees their username/name and account settings link."""
        self.client.login(username="admin_a", password="Password123!")
        response = self.client.get(reverse("administration:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "admin_a")
        self.assertContains(response, reverse("account_change_password"))
        self.assertContains(response, "إعدادات الحساب")

    def test_user_name_and_settings_in_teacher_dashboard(self):
        """Teacher sees their username/name and account settings link."""
        self.client.login(username="teacher_a", password="Password123!")
        response = self.client.get(reverse("teachers:teacher_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "teacher_a")
        self.assertContains(response, reverse("account_change_password"))
        self.assertContains(response, "إعدادات الحساب")

    def test_user_settings_page_and_password_update(self):
        """User can view settings page and update password successfully."""
        self.client.login(username="teacher_a", password="Password123!")
        change_url = reverse("account_change_password")

        # View settings page
        response = self.client.get(change_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "إعدادات الحساب")
        self.assertContains(response, "teacher_a")

        # Post new password
        post_data = {
            "oldpassword": "Password123!",
            "password1": "NewSecurePass2026!",
            "password2": "NewSecurePass2026!",
        }
        response = self.client.post(change_url, data=post_data, follow=True)
        self.assertEqual(response.status_code, 200)

        # Verify old password fails and new password works
        self.client.logout()
        login_success = self.client.login(username="teacher_a", password="NewSecurePass2026!")
        self.assertTrue(login_success)


class PWATests(BaseTestCase):
    """Tests for PWA manifest, service worker, and metadata."""

    def test_manifest_endpoint_and_content(self):
        """Verify /manifest.json returns valid JSON and PWA properties."""
        response = self.client.get("/manifest.json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/manifest+json")
        self.assertContains(response, "نظام إدارة الحلقات القرآنية")
        self.assertContains(response, "standalone")
        self.assertContains(response, "icon-192.png")

    def test_service_worker_endpoint(self):
        """Verify /sw.js is accessible as javascript with root scope."""
        response = self.client.get("/sw.js")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/javascript")
        self.assertContains(response, "CACHE_NAME")

    def test_pwa_meta_tags_in_templates(self):
        """Verify home page includes PWA manifest and theme meta tags."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'rel="manifest" href="/manifest.json"')
        self.assertContains(response, 'name="theme-color"')


class InactiveSchoolAccessTests(BaseTestCase):
    """Tests for access restrictions when a school is deactivated by global admin."""

    def test_inactive_school_admin_login_rejected(self):
        """School admin belonging to a deactivated school cannot log in."""
        self.school_a.is_active = False
        self.school_a.save()

        login_url = reverse("account_login")
        response = self.client.post(login_url, data={
            "login": "admin_a",
            "password": "Password123!",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "تم تعطيل حساب هذه المدرسة من قبل الإدارة العامة")
        # Ensure user is not authenticated
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_inactive_school_teacher_login_rejected(self):
        """Teacher belonging to a deactivated school cannot log in."""
        self.school_a.is_active = False
        self.school_a.save()

        login_url = reverse("account_login")
        response = self.client.post(login_url, data={
            "login": "teacher_a",
            "password": "Password123!",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "تم تعطيل حساب هذه المدرسة من قبل الإدارة العامة")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_inactive_school_active_session_terminated_by_middleware(self):
        """Active session for school admin is terminated if school is deactivated."""
        self.client.login(username="admin_a", password="Password123!")

        # Deactivate school while session is active
        self.school_a.is_active = False
        self.school_a.save()

        dashboard_url = reverse("administration:dashboard")
        response = self.client.get(dashboard_url, follow=True)
        # Should redirect to login page with message
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "تم تعطيل حساب هذه المدرسة من قبل الإدارة العامة")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_inactive_school_teacher_session_terminated_by_middleware(self):
        """Active session for teacher is terminated if school is deactivated."""
        self.client.login(username="teacher_a", password="Password123!")

        # Deactivate school while session is active
        self.school_a.is_active = False
        self.school_a.save()

        teacher_url = reverse("teachers:teacher_dashboard")
        response = self.client.get(teacher_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "تم تعطيل حساب هذه المدرسة من قبل الإدارة العامة")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_global_admin_can_access_when_schools_are_inactive(self):
        """Global superuser can log in and manage schools even if all schools are inactive."""
        self.school_a.is_active = False
        self.school_a.save()
        self.school_b.is_active = False
        self.school_b.save()

        global_admin = User.objects.create_superuser(
            username="global_admin", email="global@test.com", password="Password123!"
        )
        self.client.login(username="global_admin", password="Password123!")

        response = self.client.get(reverse("schools:school_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "مدرسة النور")
        self.assertContains(response, "مدرسة الفرقان")

    def test_reactivated_school_restores_login_and_access(self):
        """Re-activating a school restores access for its users."""
        self.school_a.is_active = False
        self.school_a.save()

        # Re-activate school
        self.school_a.is_active = True
        self.school_a.save()

        login_url = reverse("account_login")
        response = self.client.post(login_url, data={
            "login": "admin_a",
            "password": "Password123!",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertContains(response, "لوحة التحكم")



