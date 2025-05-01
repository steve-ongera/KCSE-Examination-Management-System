from django.core.management.base import BaseCommand
from exam_portal.models import Student, ExamYear, ExamRegistration, Subject, SubjectRegistration
import random

class Command(BaseCommand):
    help = "Register all unregistered students for the current exam year"

    def handle(self, *args, **kwargs):
        try:
            # Get the current exam year
            current_exam_year = ExamYear.objects.get(is_current=True)
        except ExamYear.DoesNotExist:
            self.stdout.write(self.style.ERROR("No current exam year found."))
            return

        # Get the compulsory and optional subjects
        compulsory_subjects = list(Subject.objects.filter(category='CORE', is_active=True))
        optional_subjects = list(Subject.objects.exclude(category='CORE').filter(is_active=True))

        # Ensure there are enough optional subjects
        if len(optional_subjects) < 4:
            self.stdout.write(self.style.ERROR("Not enough optional subjects to choose from."))
            return

        # Get the list of active students
        students = Student.objects.filter(is_active=True)

        for student in students:
            # Check if the student is already registered for any exam year
            already_registered = ExamRegistration.objects.filter(student=student).exists()
            if already_registered:
                self.stdout.write(f"{student} already registered.")
                continue

            # Register student for the exam in the current exam year
            registration = ExamRegistration.objects.create(student=student, exam_year=current_exam_year)

            # Register compulsory subjects for the student
            for subject in compulsory_subjects:
                SubjectRegistration.objects.create(registration=registration, subject=subject, is_compulsory=True)

            # Register 4 random optional subjects for the student
            selected_optional_subjects = random.sample(optional_subjects, 4)
            for subject in selected_optional_subjects:
                SubjectRegistration.objects.create(registration=registration, subject=subject, is_compulsory=False)

            # Print success message for the registered student
            self.stdout.write(self.style.SUCCESS(f"Registered {student} with {len(compulsory_subjects) + 4} subjects."))

        # Print completion message
        self.stdout.write(self.style.SUCCESS("Done registering students."))
