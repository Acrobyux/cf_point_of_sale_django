import smtplib

from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from decouple import config
from .abstracts import AbstractMailer


class NewCampaignMailer(AbstractMailer):
    """Class to handle sending new campaign emails."""
    def send_mail(self, mail: EmailMultiAlternatives):
        """
                Send the given email.

                Args:
                    mail (EmailMultiAlternatives): Email to be sent.

                Raises:
                    Exception: If there is an error while sending the email.
                """
        try:
            mail.send(fail_silently=False)
        except smtplib.SMTPDataError as e:
            # Daily user sending quota exceeded.
            print(e)

    def create_mail(self, subject: str, template_path: str, context: dict, recipients: set):
        """
                Create an email for a new campaign.

                Args:
                    subject (str):
                        Email subject.
                    template_path (str):
                        Path to the email template.
                    context (dict):
                        Context data for the template.
                    recipients (set):
                        List of recipient email addresses.

                Returns:
                    EmailMultiAlternatives: Created email instance.

                Raises:
                    Exception: If there is an error while creating the email.
                """
        template = get_template(template_path)
        content = template.render(context)

        mail = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=config('EMAIL_HOST_USER'),
            to=recipients,
            cc=[
                superadmin.email for superadmin
                in
                User.objects.filter(is_superuser=True)
            ]
        )

        mail.attach_alternative(content, 'text/html')

        return mail

    def attach_file(self, mail: EmailMultiAlternatives, file_path: str, file_name: str):
        with open(file_path, 'rb') as f:
            image_content = f.read()
            mail.attach(
                file_name,
                image_content
            )