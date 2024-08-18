# Automated Job Scraper with Skill-Based Filtering and Email Notifications

This project is an automated web job scraper for the TimesJobs website, filtering job postings based on specified skills and sending email notifications for relevant opportunities. It efficiently saves job details in CSV and JSON formats for easy tracking and analysis.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Important Warning](#important-warning)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Project Overview
This project is designed to streamline the job search process by automatically web scraping job listings from the TimesJobs website, filtering out positions that require specific skills, and sending email notifications for jobs that match the user’s preferences. The job details are saved in both CSV and JSON formats for easy access and analysis.

## Features

- **Skill-Based Filtering:**
  - Filter out jobs that require specified skills you want to avoid.

- **Automated Email Notifications:**
  - Receive email alerts for jobs that match your criteria.

- **Data Persistence:**
  - Save job details in CSV and JSON formats for easy tracking.

- **Customizable Scraping Interval:**
  - Configure the wait time between scraping iterations to suit your needs.

- **Error Handling:**
  - Includes robust error handling for email sending and data scraping processes.

- **Session Summaries:**
  - Each scraping session generates a summary, logged in a `summary.txt` file, for easy review of the scraping results.

## Tech Stack

- **Python:**
  - Core programming language used for the project.

- **BeautifulSoup:**
  - Library used for web scraping and parsing HTML.

- **Requests:**
  - Library for making HTTP requests to retrieve web pages.

- **SMTP (smtplib):**
  - Used for sending automated emails through Outlook.

- **CSV:**
  - Built-in Python library for saving data in CSV format.

- **JSON:**
  - Built-in Python library for saving data in JSON format.

- **argparse:**
  - Library for command-line argument parsing to customize scraping intervals.

- **OS:**
  - Used for file management and directory creation.

## Setup and Installation
1. **Clone the Repository:**

   
   ```bash
   git clone https://github.com/utkartist/job-scraper.git

python job_scraper.py --wait_time 10
The --wait_time argument sets the interval between scraping iterations in minutes.


**Input Skills to Filter:**



When prompted, input the number of skills you want to filter out.
Enter each skill one by one.

**Check Saved Jobs:**



Job details will be saved in the posts/ directory as both .json and .csv files.
A summary of each scraping session will be appended to summary.txt.

**Email Configuration:**



Set your Outlook email address and password in the EMAIL_ADDRESS and EMAIL_PASSWORD variables within the script.

Set the recipient’s email address in the TO_EMAIL variable.

### Skill Filtering:

Input the skills you want to avoid during the script execution when prompted.

Use the --wait_time command-line argument to specify the interval (in minutes) between each scraping session.


## Important Warning:

This script sends automated emails using your Outlook account. Please be cautious when setting up the script to avoid sending too many emails in a short period, as this could trigger Outlook’s spam detection mechanisms and result in your account being blocked or restricted.


**To minimize the risk:**

Avoid setting very short intervals between scraping sessions.
Ensure the recipient of the emails is aware of the frequency and content of the notifications.
Use this tool responsibly to avoid potential issues with your email account.

## Future Enhancements:
**Support for Multiple Job Portals:**

Extend the scraper to work with additional job websites.

**GUI Interface:**

Develop a simple graphical user interface to make the tool more user-friendly.

**Advanced Filtering:**

Add more sophisticated filtering options, such as filtering by job location, salary range, etc.
## Contributing:
Contributions are welcome! Please fork the repository and submit a pull request with your changes.
