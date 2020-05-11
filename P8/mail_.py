# -*- coding: UTF-8 -*-
"""
Using the os module to retrieve cron variables
Use of modulesmtplib to connect to the gmail client with the secure ssl protocol
Use of datetime to retrieve the current date to enter in the mail
"""
import os
import smtplib
import ssl
import datetime


class Mailing:

    """Send a variable email according to the update of the database worked"""

    def __init__(self, true_false=1):
        self.true_false = true_false

    def test_mail(self):
        """binary test on the test_mail function to modify the variable "message"""
        date_now = datetime.datetime.now()
        dict_date = {1:"Janvier", 2:"Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7:"Juillet", 8:"Août", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"}
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = os.environ.get("MAIL_SENDER")  # Enter your address
        receiver_email = os.environ.get("MAIL_RECEIVER")  # Enter receiver address
        password = os.environ.get("KEY_PASSWORD")
        print(sender_email, receiver_email, password)

        if self.true_false == 1:
            message = "Mise a jour BDD P10 le {} {} {}.".format(date_now.day, dict_date[date_now.month], date_now.year)
        else:
            message = "Echec Mise a jour BDD P10 le {} {} {}.".format(date_now.day, dict_date[date_now.month], date_now.year)

        print(message)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

if __name__ == '__main__':
    Mailing(true_false=1).test_mail()
