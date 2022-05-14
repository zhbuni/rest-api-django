import random
import string

from django.db import models
from uuid import uuid4
from dotenv import load_dotenv
import os


class User(models.Model):
    username = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    password = models.CharField(max_length=50)
    ifLogged = models.BooleanField(default=False)
    token = models.CharField(max_length=500, null=True, default="")

    def __str__(self):
        return "{} -{}".format(self.username, self.email)


class Token(models.Model):
    token = models.CharField(max_length=255, null=False, default=''.join(random.choice(string.ascii_uppercase
                                                                                       + string.digits) for _ in range(6)))
    is_registered = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, null=False)

    def save(self, *args, **kwargs):
        pk = self.pk  # pk will be None like objects if self is new instance
        super().save(*args, **kwargs)
        if not self.is_registered:
            import smtplib, ssl

            port = 465  # For SSL

            # Create a secure SSL context
            context = ssl.create_default_context()
            load_dotenv()
            smtp = os.getenv('smtp_server')
            password = os.getenv('password')
            email = os.getenv('email')
            print(smtp, password, email)

            with smtplib.SMTP_SSL(smtp, port, context=context) as server:
                server.login(email, password)
                msg = f'''From: {email}\n\nYour code is {self.token} '''
                server.sendmail(f'{email}', to_addrs=self.email, msg=msg)