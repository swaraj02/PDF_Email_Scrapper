import os
import re
import csv
import pdfplumber

def extract_emails_from_pdf(pdf_path):
    emails = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                # Use regular expression to find email addresses
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails.extend(re.findall(email_pattern, text))
    except Exception as e:
        print(f"Error processing PDF '{pdf_path}': {str(e)}")
    return emails

def extract_emails_from_folder(folder_path):
    emails = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            emails.extend(extract_emails_from_pdf(pdf_path))
    return emails

def save_emails_to_csv(emails, csv_file):
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            fieldnames = ['Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for email in emails:
                writer.writerow({'Email': email})
    except Exception as e:
        print(f"Error saving emails to CSV '{csv_file}': {str(e)}")

# Replace 'folder_path' with the path to your folder containing PDF files
folder_path = '/Users/swaraj/Resume/Resume'
# Replace 'output.csv' with the desired CSV file name
csv_file = 'output.csv'

emails = extract_emails_from_folder(folder_path)
save_emails_to_csv(emails, csv_file)

