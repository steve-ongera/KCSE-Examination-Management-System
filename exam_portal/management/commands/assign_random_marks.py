import random
from django.core.management.base import BaseCommand
from exam_portal.models import SubjectRegistration, ExamResult

class Command(BaseCommand):
    help = 'Assign random marks only to subjects with no existing marks or result.'

    def handle(self, *args, **kwargs):
        count_created = 0
        count_updated = 0

        # Get all SubjectRegistrations that do NOT have a related ExamResult
        registrations_without_results = SubjectRegistration.objects.filter(result__isnull=True)

        for reg in registrations_without_results:
            ExamResult.objects.create(
                subject_registration=reg,
                marks=random.randint(0, 100)
            )
            count_created += 1
            self.stdout.write(f"Created ExamResult for {reg}")

        # Get ExamResults with NULL marks (meaning result exists but marks aren't set)
        results_with_null_marks = ExamResult.objects.filter(marks__isnull=True)

        for result in results_with_null_marks:
            result.marks = random.randint(0, 100)
            result.save()
            count_updated += 1
            self.stdout.write(f"Updated marks for {result.subject_registration}")

        self.stdout.write(self.style.SUCCESS(
            f"Finished: Created {count_created} new ExamResults and updated {count_updated} existing ones."
        ))
