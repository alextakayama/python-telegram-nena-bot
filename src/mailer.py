from debug import Debuggable
from email import policy, utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email
import imaplib
import os
import smtplib

class Mailer(Debuggable):
    def __init__(self, debug: bool = False):
        super().__init__(debug)
        self._load_credentials()
        self.imap = None
        self.smtp = None

    def __del__(self):
        self.disconnect_imap()
        self.disconnect_smtp()

    def _load_credentials(self):
        self.imap_host = os.getenv("IMAP_HOST")
        self.imap_port = os.getenv("IMAP_PORT")
        self.imap_username = os.getenv("IMAP_USERNAME")
        self.imap_password = os.getenv("IMAP_PASSWORD")

        self.smtp_from = os.getenv("SMTP_FROM")
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = os.getenv("SMTP_PORT")
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")

    def connect_imap(self) -> bool:
        """Connect and login to IMAP server"""
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_host)
            self.imap.login(self.imap_username, self.imap_password)
        except Exception as e:
            self.log_debug(f"IMAP connection failed: {e}")
            return False
        return True

    def connect_smtp(self) -> bool:
        """Connect and login to SMTP server"""
        try:
            self.smtp = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            self.smtp.login(self.smtp_username, self.smtp_password)
        except Exception as e:
            self.log_debug(f"SMTP connection failed: {e}")
            return False
        return True

    def disconnect_imap(self) -> bool:
        try:
            self.imap.logout() if self.imap else None
        except Exception as e:
            self.log_debug(f"Error disconnecting IMAP: {e}")

        self.imap = None
        return True

    def disconnect_smtp(self) -> bool:
        try:
            self.smtp.quit() if self.smtp else None
        except Exception as e:
            self.log_debug(f"Error disconnecting SMTP: {e}")

        self.smtp = None
        return True

    def ensure_imap_connected(self) -> None:
        if self.imap is not None:
            self.disconnect_imap()
        self.connect_imap()

    def ensure_smtp_connnected(self) -> None:
        if self.smtp is not None:
            self.disconnect_smtp()
        self.connect_smtp()

    def _select_inbox(self) -> None:
        self.ensure_imap_connected()
        self.imap.select("INBOX")

    def list_inbox_messages(self, all: bool = False):
        """Retrieve a list of messages in INBOX"""
        self._select_inbox()

        messages = []

        criteria = "ALL" if all else "UNSEEN"

        result, data = self.imap.search(None, criteria)
        if result != "OK":
            return messages

        msg_ids = data[0].split()

        for msg_id in msg_ids:
            result, msg_data = self.imap.fetch(msg_id, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
            if result != "OK":
                self.log_debug(f"Unable to fetch message id: {msg_id}")
                continue
            
            msg = email.message_from_bytes(msg_data[0][1], policy=policy.default)

            messages.append({
                "Id": msg_id, 
                "From": msg.get("From"), 
                "Subject": msg.get("Subject"), 
                "Date": msg.get("Date")
            })

        return messages

    def _extract_email_body(self, msg) -> str:
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_disposition = part.get("Content-Disposition", "")
                if part.get_content_type() == "text/plain":
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or "utf-8"
                    body += payload.decode(charset, errors="replace")
        else:
            payload = msg.get_payload(decode=True)
            body = payload.decode('utf-8', errors="replace")

        return body

    def read_message(self, msg_id):
        """Retrieve the details of a message"""
        self._select_inbox()

        result, msg_data = self.imap.fetch(msg_id, "(RFC822)")
        if result != "OK":
            self.log_debug(f"Unable to fetch message id: {msg_id}")
            return None

        msg = email.message_from_bytes(msg_data[0][1], policy=policy.default)

        message = {
            "Id": msg_id, 
            "From": msg.get("From"), 
            "Subject": msg.get("Subject"), 
            "Date": msg.get("Date")
        }

        message["Body"] = self._extract_email_body(msg)

        return message

    def send_text_message(self, to_addrs, subject: str, body: str) -> bool:
        """Retrieve the details of a message"""
        self.ensure_smtp_connected()

        msg = MIMEMultipart()

        msg["From"] = self.smtp_from
        msg["To"] = to_addrs
        msg["Subject"] = subject

        # Add common headers
        msg["Message-ID"] = utils.make_msgid()
        msg["Date"] = utils.formatdate(localtime=True)

        # Attach the text body
        msg.attach(MIMEText(body, "plain"))

        try:
            self.smtp.sendmail(self.smtp_from, to_addrs, msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print("Error sending email: ", e)

        return True

    def delete_message(self, msg_id) -> bool:
        """Delete a message from INBOX"""
        self._select_inbox()

        result, _ = self.imap.store(msg_id, '+FLAGS', "\\Deleted")
        if result == "OK":
            self.imap.expunge()
        else:
            self.log_debug(f"Unable to delete message id: {msg_id}")

        return True
