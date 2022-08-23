#!/usr/bin/python3

# Sample usage:
# csvtoemails.py mydbrfile.csv
# csvtoemails.py mydbrfile.csv bademails.txt

from sys import argv

# Indices for emails on each row.
LEAD_COACH_MENTOR_1_PRIMARY=49-1
LEAD_COACH_MENTOR_1_ALTERNATE=50-1
LEAD_COACH_MENTOR_2_PRIMARY=62-1
LEAD_COACH_MENTOR_2_ALTERNATE=63-1
TEAM_ADMIN_PRIMARY=75-1

# Format and add email to a given set.
def add_formatted_email(email: str, emails: set):
  formattedemail = email.encode().replace(b'\x00', b'').decode('utf-8').lower().strip()
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
  with open(csvfilepath, 'rb') as csvfile:
    lines = csvfile.readlines()[1:-1]
    for line in lines:
      line = line.decode('utf-8')
      values = line.split('\t')
      add_formatted_email(values[LEAD_COACH_MENTOR_1_PRIMARY], emails)
      add_formatted_email(values[LEAD_COACH_MENTOR_1_ALTERNATE], emails)
      add_formatted_email(values[LEAD_COACH_MENTOR_2_PRIMARY], emails)
      add_formatted_email(values[LEAD_COACH_MENTOR_2_ALTERNATE], emails)
      add_formatted_email(values[TEAM_ADMIN_PRIMARY], emails)

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
