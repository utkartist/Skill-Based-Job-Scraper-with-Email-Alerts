import os
import time
import csv
import json
import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import argparse

# Email configuration
EMAIL_ADDRESS = 'xxx'  # Your Outlook email address
EMAIL_PASSWORD = 'xxx'  # Your Outlook password
TO_EMAIL = 'xxx'  # Recipient's email address

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        # Use Outlook's SMTP server
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, text)
        print("Email sent successfully.")
    except smtplib.SMTPAuthenticationError:
        print("Failed to send email: Authentication error.")
    except smtplib.SMTPDataError as e:
        if e.smtp_code == 554:
            print(f"Failed to send email: {e.smtp_error.decode()}")
            print("Pausing for 10 minutes before retrying...")
            time.sleep(600)  # Wait for 10 minutes before retrying
        else:
            print(f"Failed to send email: {e}")

# Argument parser for configurable wait time
parser = argparse.ArgumentParser(description='Job Scraper Configuration')
parser.add_argument('--wait_time', type=int, default=10, help='Waiting time between iterations in minutes')
args = parser.parse_args()

time_wait = args.wait_time

# Ask the user for the number of skills they want to filter out
num_skills = int(input('How many skills do you want to filter out? '))

# Collect the skills from the user
unfamiliar_skills = []
for i in range(num_skills):
    skill = input(f'Enter skill {i+1}: ').strip().lower()
    unfamiliar_skills.append(skill)

print(f'Filtering out jobs that require the following skills: {", ".join(unfamiliar_skills)}')

def save_job_data(index, job_data):
    """Save job data to both CSV and JSON formats."""
    if not os.path.exists('posts'):
        os.makedirs('posts')

    with open(f'posts/{index}.json', 'w') as json_file:
        json.dump(job_data, json_file, indent=4)

    csv_file = f'posts/jobs.csv'
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, 'a', newline='') as csvfile:
        fieldnames = ['Company Name', 'Required Skills', 'More Info', 'Published Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'Company Name': job_data['Company Name'],
            'Required Skills': job_data['Required Skills'],
            'More Info': job_data['More Info'],
            'Published Date': job_data['Published Date']
        })

def find_jobs():
    total_jobs = 0
    filtered_out_jobs = 0
    saved_jobs = 0

    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_ = 'clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):
        total_jobs += 1
        published_date = job.find('span', class_ = 'sim-posted').span.text
        
        company_name = job.find('h3', class_ = 'joblist-comp-name').text.strip()
        skills = job.find('span', class_ = 'srp-skills').text.replace(' ', '').replace('\n', '').lower().split(',')
        more_info = job.header.h2.a['href']

        # Check if none of the unfamiliar skills are in the job's required skills
        if not any(skill in skills for skill in unfamiliar_skills):
            saved_jobs += 1
            job_data = {
                'Company Name': company_name,
                'Required Skills': ', '.join(skills),
                'More Info': more_info,
                'Published Date': published_date.strip()
            }
            save_job_data(index, job_data)
            print(f'File Saved: {index}')

            # Send email notification
            subject = f"New Job Post: {company_name}"
            body = f"Company Name: {company_name} \n Required Skills: {', '.join(skills)} \n More Info: {more_info}"
            send_email(subject, body)
        else:
            filtered_out_jobs += 1
            print(f"Filtered out job {index} at {company_name} due to skills: {', '.join(skills)}")

    summary = (f"Total Jobs Found: {total_jobs}\n"
               f"Filtered Out Jobs: {filtered_out_jobs}\n"
               f"Saved Jobs: {saved_jobs}\n")
    print(summary)

    with open('summary.txt', 'a') as summary_file:
        summary_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Iteration Summary\n")
        summary_file.write(summary + '\n')

if __name__ == '__main__':
    while True:
        find_jobs()   
        print(f'Waiting {time_wait} minutes....')  
        time.sleep(time_wait * 60)
