#!/usr/bin/python3

# Sample usage:
# csvtoemails.py mydbrfile.csv
# csvtoemails.py mydbrfile.csv bademails.txt

from csv import reader
from sys import argv

# Indices for emails on each row.
PURCHASER_EMAIL_INDEX = 54
PRIMARY_COACH_EMAIL_INDEX = 36
SECONDARY_COACH_EMAIL_INDEX = 45

# Format and add email to a given set.
def add_formatted_email(email: str, emails: set):
  formattedemail = email.lower().strip()
  if not formattedemail.isspace() and formattedemail != '':
    emails.add(formattedemail)

def main(csvfilepath: str, ignorefilepath:str = None):
  # Generate the set of known bad emails.
  ignoreemails = set()
  if ignorefilepath is not None:
    with open(ignorefilepath) as ignorefile:
      for line in ignorefile:
        add_formatted_email(line, ignoreemails)

  # Generate the set of emails in the csv from myDBR.
  emails = set()
  with open(csvfilepath) as csvfile:
    # Read all rows except the header
    emailreader = reader(csvfile)
    next(emailreader)

    for row in emailreader:
      add_formatted_email(row[PURCHASER_EMAIL_INDEX], emails)
      add_formatted_email(row[PRIMARY_COACH_EMAIL_INDEX], emails)
      add_formatted_email(row[SECONDARY_COACH_EMAIL_INDEX], emails)

  # Generate the set of good emails
  goodemails = sorted(emails.difference(ignoreemails))
  outputfilename = csvfilepath.split('.')[0] + '-emails.txt'
  with open(outputfilename, 'w') as outputfile:
    for email in goodemails:
      outputfile.write(email)
      outputfile.write('\n')

if __name__ == "__main__":
  if len(argv) == 2:
    main(argv[1])
  elif len(argv) == 3:
    main(argv[1], argv[2])
  else:
    print("Must include the csv containing the team information.")
