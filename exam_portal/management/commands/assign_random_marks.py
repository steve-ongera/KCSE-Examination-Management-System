import random
from django.core.management.base import BaseCommand
from exam_portal.models import SubjectRegistration, ExamResult

class Command(BaseCommand):
    help = 'Assign random marks to registered subjects that have no marks or no result.'

    def handle(self, *args, **kwargs):
        count_created = 0
        count_updated = 0

        subject_regs = SubjectRegistration.objects.all()

        for reg in subject_regs:
            try:
                result = reg.result  # Try to access related ExamResult
                if result.marks is None:  # Check if marks are None
                    result.marks = random.randint(0, 100)
                    result.save()
                    count_updated += 1
                    self.stdout.write(f"Updated marks for {reg}")
                else:
                    self.stdout.write(f"Skipped {reg} as it already has marks.")
            except ExamResult.DoesNotExist:
                # If no ExamResult exists, create a new one with random marks
                result = ExamResult.objects.create(
                    subject_registration=reg,
                    marks=random.randint(0, 100)
                )
                count_created += 1
                self.stdout.write(f"Created ExamResult for {reg}")

        self.stdout.write(self.style.SUCCESS(
            f"Finished: Created {count_created} new ExamResults and updated {count_updated} existing ones."
        ))
