import imaplib, email
import re
from typing import List
from decouple import config
from energy_usage import EnergyUsage
from datetime import date

def setup_connection() -> imaplib.IMAP4_SSL:
    '''Sets up the connection to the email'''

    USERNAME = config("EMAIL_USERNAME")
    PASSWORD = config("EMAIL_KEY")
    HOST = "imap.gmail.com"
    mail = imaplib.IMAP4_SSL(HOST)
    mail.login(USERNAME, PASSWORD)
    return mail

def get_latest_energy_data():
    mail = setup_connection()
    mail.select("INBOX")
    _, from_reliant = mail.uid('search', None, '(SUBJECT "Your Reliant Weekly Summary")')
    energy_summary_emails = from_reliant[0].split()
    # week_summary = energy_summary_emails[:-4:-1][::-1] #we need the oldest one first (3 weeks back)
    week_summary = energy_summary_emails[:-2:-1] #newest
    energy_data: List[EnergyUsage] = []

    for each_mail in week_summary:
        _, data = mail.fetch(each_mail, '(RFC822)')
        raw_email = data[0][1]
        email_content = email.message_from_string(raw_email.decode('utf-8'))
        date_range = email_content["subject"].split(": ")[-1]
        usage = ""
        cost = ""

        for body in email_content.walk():
            if body.get_content_type() =="text/plain":
                message = body.get_payload(decode=True)
                decoded_message = message.decode("utf-8")
                usage, cost = re.findall(r"......kWh?|\$.....", decoded_message)[:2]
                usage = usage.replace("kWh","").strip()
                break
        energy_data.append(EnergyUsage(date_range, usage, cost))
    mail.close()
    mail.logout()
    return energy_data


def store_energy_data(energy_data: List[EnergyUsage]):
    with open("energy_usages.txt", 'a') as file:
        for usage in energy_data:
            file.write(f'{usage.get_dates()},{usage.get_usage()},{usage.get_cost()}\n')


def get_stored_energy_data()-> List[dict]:
    energy_data: List[dict] = []
    with open("energy_usages.txt", 'r') as file:
        last_three_recent_data = file.readlines()[::-1][:3]
        for data in last_three_recent_data:
            dates,usage,cost = data.strip().split(",")
            energy_data.append(
                {
                    "dates": dates,
                    "usage": usage,
                    "cost": cost
                }
            )
    return energy_data


def handle_energy_data_request():
    weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")
    weekday = date.today().weekday()

    #only update the stored dataon Tuesdays after a new summary has been published
    if weekday == weekDays.index("Tuesday"):
        latest_data = get_latest_energy_data()
        store_energy_data(latest_data)
    
    return get_stored_energy_data()
    

        



        



if __name__ == "__main__":
    # ---------Done only on Tuesdays when a new update is published-------
    # data = get_latest_energy_data()
    # store_energy_data(data)
    # print(get_stored_energy_data())
    print(handle_energy_data_request())

