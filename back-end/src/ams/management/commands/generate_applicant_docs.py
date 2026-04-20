import logging
import os

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from ams.models.applicants import Applicant
from ams.views.applicants import generate_documents_for_applicant

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate documents for selected applicants by email"

    def add_arguments(self, parser):
        parser.add_argument(
            "--email",
            "-e",
            action="append",
            dest="emails",
            default=[],
            help="Applicant corporate email (can be specified multiple times)",
        )
        parser.add_argument(
            "--emails-file",
            "-f",
            type=str,
            help="Path to file containing emails (one per line)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without actually generating documents",
        )

    def handle(self, *args, **options):
        emails = list(options["emails"])
        emails_file = options.get("emails_file")
        dry_run = options.get("dry_run", False)

        # Validate arguments
        if not emails and not emails_file:
            raise CommandError("At least one of --email or --emails-file is required")

        # Collect all emails from file if specified
        if emails_file:
            if not os.path.exists(emails_file):
                raise CommandError(f"Emails file not found: {emails_file}")
            with open(emails_file, "r", encoding="utf-8") as f:
                for line in f:
                    email = line.strip()
                    if email and not email.startswith("#"):
                        emails.append(email)

        if not emails:
            raise CommandError("No emails specified")

        self.stdout.write(
            self.style.SUCCESS(
                f"Starting document generation for {len(emails)} applicant(s)..."
            )
        )

        # Find applicants by emails
        applicants = Applicant.objects.filter(
            Q(contact_info__corporate_email__in=emails)
        ).select_related("user", "application_process")

        found_emails = {app.contact_info.corporate_email for app in applicants}
        not_found_emails = set(emails) - found_emails

        if not_found_emails:
            self.stdout.write(
                self.style.WARNING(
                    f"Applicants not found for emails: {', '.join(not_found_emails)}"
                )
            )

        if not applicants:
            raise CommandError("No applicants found for the specified emails")

        self.stdout.write(
            self.style.SUCCESS(
                f"Found {applicants.count()} applicant(s) for document generation"
            )
        )

        # Generate documents for each applicant
        success_count = 0
        failed_count = 0

        for applicant in applicants:
            email = applicant.contact_info.corporate_email

            if dry_run:
                self.stdout.write(f"[DRY RUN] Would generate documents for: {email})")
                success_count += 1
                continue

            try:
                self.stdout.write(f"Processing: ({email})...")
                generate_documents_for_applicant(applicant)
                self.stdout.write(
                    self.style.SUCCESS("Documents generated successfully")
                )
                success_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to generate documents: {str(e)}")
                )
                failed_count += 1

        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS("Generation complete:"))
        self.stdout.write(f"  Successful: {success_count}")
        self.stdout.write(f"  Failed: {failed_count}")
        self.stdout.write(f"  Not found: {len(not_found_emails)}")
        self.stdout.write("=" * 50)
