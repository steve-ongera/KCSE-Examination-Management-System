import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.utils import timezone
from exam_portal.models import Resource, ResourceType, Category, User


class Command(BaseCommand):
    help = "Bulk upload KCSE past papers from local PDF folder"

    def handle(self, *args, **options):
        pdf_path = r"C:\Users\user\Downloads\papers"

        try:
            creator = User.objects.get(username='gadafi')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ User 'gadafi' does not exist."))
            return

        try:
            resource_type = ResourceType.objects.get(name='PDF')
        except ResourceType.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ ResourceType 'PDF' not found."))
            return

        try:
            category = Category.objects.get(name='Past Papers')
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR("❌ Category 'Past Papers' not found."))
            return

        created_count = 0

        for filename in os.listdir(pdf_path):
            if filename.lower().endswith(".pdf"):
                full_path = os.path.join(pdf_path, filename)

                with open(full_path, 'rb') as f:
                    django_file = File(f)
                    title = filename.replace("_", " ").replace(".pdf", "").title()
                    file_size = int(os.path.getsize(full_path) / 1024)

                    parts = title.split()
                    year = next((p for p in parts if p.isdigit() and len(p) == 4), "Unknown Year")
                    subject = next((p for p in parts if p.lower() not in ['kcse', year.lower()]), "General")
                    description = f"This is a KCSE past paper for {subject} from {year}. It is intended for revision and preparation by students and teachers. Useful for assessing performance and understanding exam formats."

                    resource = Resource(
                        title=title,
                        description=description,
                        file_size=file_size,
                        resource_type=resource_type,
                        category=category,
                        status='published',
                        created_by=creator,
                        published_at=timezone.now()
                    )

                    resource.file.save(filename, django_file, save=True)
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"✅ Created: {title}"))

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Done. Total resources created: {created_count}"))
