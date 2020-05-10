# -*- coding: UTF-8 -*-
import os
import smtplib, ssl
import datetime

class Mailing():
    def __init__(self, True_False=1):
        self.True_False = True_False

    def test_mail(self):
        dt = datetime.datetime.now()
        dict_date = {1:"Janvier", 2:"Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin", 7:"Juillet", 8:"Août", 9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"}
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = os.environ.get("MAIL_SENDER")  # Enter your address
        receiver_email = os.environ.get("MAIL_RECEIVER")  # Enter receiver address
        password = os.environ.get("KEY_PASSWORD")
        print(sender_email, receiver_email, password)

        if self.True_False == 1 :
            message = "Mise a jour BDD P10 le {} {} {}.".format(dt.day, dict_date[dt.month], dt.year)
        else:
            message = "Echec Mise a jour BDD P10 le {} {} {}.".format(dt.day, dict_date[dt.month], dt.year)

        print(message)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

if __name__ == '__main__':
    Mailing(True_False=1).test_mail()