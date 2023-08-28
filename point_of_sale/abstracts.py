from abc import ABC, abstractmethod
from django.core.mail import EmailMultiAlternatives


class AbstractMailer(ABC):
    """An abstract base class for mailer implementations.

    This class defines the interface for sending emails and
    creating email messages with attachments.

    Attributes:
        None

    Methods:
        send_mail(mail):
            Sends an email message.
        create_mail(subject, template_path, context, recipients):
            Creates an email message.
        attach_file(mail, file_path, file_name):
            Attaches a file to an email message.
    """

    @abstractmethod
    def send_mail(self, mail: EmailMultiAlternatives):
        """Send an email message.

        This method sends the provided email message.

        Args:
            mail (EmailMultiAlternatives):
                The email message to be sent.

        Returns:
            None
        """
        pass

    @abstractmethod
    def create_mail(self, subject: str, template_path: str, context: dict, recipients: set):
        """Create an email message.

        This method creates an email message with the provided subject, template,
        context, and recipients.

        Args:
            subject (str):
                The subject of the email.
            template_path (str):
                The path to the email template.
            context (dict):
                The context data for rendering the email template.
            recipients (set):
                A set of recipient email addresses.

        Returns:
            EmailMultiAlternatives: The created email message.
        """
        pass

    @abstractmethod
    def attach_file(self, mail: EmailMultiAlternatives, file_path: str, file_name: str):
        """Attach a file to an email message.

        This method attaches a file located at the specified path to the provided
        email message.

        Args:
            mail (EmailMultiAlternatives):
                The email message to which the file will be attached.
            file_path (str):
                The path to the file to be attached.
            file_name (str):
                The name of the attached file.

        Returns:
            None
        """
        pass
