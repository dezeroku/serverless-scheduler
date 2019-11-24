import connexion
import six

from swagger_server.models.mail import Mail  as MailModel# noqa: E501
from swagger_server import util

import os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName, FileType, Disposition, ContentId)

def mail(body):  # noqa: E501
    """send email containing change data

     # noqa: E501

    :param body: necessary data
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = MailModel.from_dict(connexion.request.get_json())  # noqa: E501

        message = Mail(
            from_email=os.environ.get('MAIL_SENDER'),
            to_emails=body.recipients,
            subject=body.subject,
            html_content=body.html_content
        )

        attachments = []
        for x in body.data.attachments:
            name = x.filename
            content = x.content
            filetype = x.filetype

            attachment = Attachment()
            attachment.file_content = FileContent(content)
            attachment.file_type = FileType(filetype)
            attachment.file_name = FileName(name)
            attachment.disposition = Disposition('attachment')
            attachment.content_id = ContentId(name)
            attachments.append(attachment)

        message.attachment = attachments

        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.to_dict)

        return 'done'
    return 'non json data'
