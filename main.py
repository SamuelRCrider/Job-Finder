"""import libraries"""
import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from secret_keys import MAILPASSWORD
from email.message import EmailMessage


def startup_jobs():
    url = "https://topstartups.io/jobs/?role=engineer"
    raw_html = requests.get(url).text
    soup = BeautifulSoup(raw_html, "lxml")

    jobs = soup.find_all("div", class_="col-8 col-xl-5")

    # Initialize job list
    startup_job_list = []

    for job in jobs:
        # Initialize new job dictionary
        job_dict = {}

        company_name = job.find("h7").text.strip()
        job_title = job.find("h5").text.strip()
        location = job.find_all("h7")[1].text.strip()
        learn_more = job.find_all("a")[1]["href"]

        job_dict["Company"] = company_name
        job_dict["Job"] = job_title
        job_dict["Location"] = location
        job_dict["Learn More"] = learn_more

        # Add current job dictionary to list
        startup_job_list.append(job_dict)
    
    return startup_job_list




def hot_startups():
    url = "https://topstartups.io/?sort=valuation"
    raw_html = requests.get(url).text
    soup = BeautifulSoup(raw_html, "lxml")

    startups = soup.find_all("div", class_="col-12 col-md-6 col-xl-4 infinite-item")

    # Initialize startup list
    startup_list = []

    for startup in startups:
        # Initialize new startup dictionary
        startup_dict = {}

        company = startup.find("h3").text
        description = startup.find("p").br.next_sibling.strip()
        funding = startup.find_all("span", id="funding-tags")
        company_funding = []
        for fund in funding:
            company_funding.append(fund.text)
        jobs = startup.find_all("a")[-1]["href"]

        startup_dict["Company"] = company
        startup_dict["Description"] = description
        startup_dict["Funding"] = company_funding
        startup_dict["View Jobs"] = jobs

        # Add current startup dictionary to list
        startup_list.append(startup_dict)
    
    return startup_list


if __name__ == '__main__':

    # Store function results to be used in email body
    startups = hot_startups()
    jobs_ = startup_jobs()

    # Define email sender and receiver
    email_sender = "startup.job.finder@gmail.com"
    email_password = MAILPASSWORD
    email_receiver = "sam.crider@aol.com"

    # Set the subject and body of the email
    subject = "Your Daily JobFinder Results"
    body = f"Startups to Watch:\n\n{startups}\n\nStartup Job Postings:\n\n{jobs_}"

    # Set up multipart email
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)

            


    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())