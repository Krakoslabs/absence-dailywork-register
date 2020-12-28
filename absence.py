#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import datetime
import argparse, textwrap
import yaml
from requests_hawk import HawkAuth

ABSENCE_URL = "https://app.absence.io"
DATA_FILE = "data.yml"
daysofweek=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def readdata(file):
  with open(r"%s" % file) as file:
    return yaml.full_load(file)

def sendwork(day, id, key, typeofwork, starthour='08:00', endhour='16:00'):

  hawk_auth = HawkAuth(id=id, key=key)
  response = requests.get("%s/api/v2/users/%s" % (ABSENCE_URL, id), auth=hawk_auth)
  if response.status_code != 200:
    print("Fail connecting to: %s, with id: %s and key: %s" % (ABSENCE_URL, id, key))
    exit(1)

  headers = {
      'Content-Type': "application/json",
  }
  data = {
    "userId": "%s" % id,
    "start": "%sT%s:00.000Z" % (day, starthour),
    "end": "%sT%s:00.000Z" % (day, endhour),
    "timezoneName": "CET",
    "timezone": "+0000",
    "type": "%s" % typeofwork
  }

  resp = requests.post("%s/api/v2/timespans/create" % ABSENCE_URL, auth=hawk_auth ,data=json.dumps(data), headers=headers)

def previous_week_range(date):
    start_date = date + datetime.timedelta(-date.weekday(), weeks=-1)
    return str(start_date)

def parse_arguments():
    """Parse the commandline arguments"""
    parser = argparse.ArgumentParser(
        add_help=True,
        usage='%(prog)s [OPTIONS]',
        formatter_class=argparse.RawTextHelpFormatter,
        description="Fill in daily work in Absence.io. It is always filling the whole week before as it is running or it has been specified \n\n \
        - Days of the week can be excluded by means of:\n \
            - Argument -e. This option has preference over the data.yml file. \n \
            - data.yml file \n\n \
        - Use the data.yml to customize your inputs \n \
              id: id from abscense.io \n \
              key: key from absence.io \n \
              starthour: Hour string to fill in as your start hour. Format: 'XX:YY' \n \
              endhour: Hour string to fill in as your end hour. Format: 'XX:YY' \n \
              typeofwork: Type of daily register. Allowed value: work \n \
              skipdays: List of the days to be excluded. Format: [Monday,Wednesday] \n \
        ")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--day',
        '-d',
        dest='day',
        help='Specify a date to fill the previous week of this day with this format: YYYY-MM-dd',
        type=str)
    group.add_argument(
        '--week',
        '-w',
        dest='week',
        action="store_true",
        help='Used to fill in the whole previus week. Use to be croned in your computer')
    parser.add_argument(
      "--exclusion",
      "-e",
      dest='exclusion',
      help='Specify the days of the week that should not be filled \n \
           Example: absence.py -w -e "Monday Friday"',
      default="file")
    return parser.parse_args()

def Convert(string):
  excludedDays = list(string.split(" "))
  return excludedDays

def main():
  args = parse_arguments()
  data = readdata(DATA_FILE)

  if args.week:
    today_obj = datetime.date.today()
    monday_ago = previous_week_range(datetime.date(today_obj.year, today_obj.month, today_obj.day))
  else:
    monday_ago = previous_week_range(datetime.date(int(args.day[:4]), int(args.day[5:7]), int(args.day[8:])))

  obj_date = datetime.datetime.strptime(monday_ago, "%Y-%m-%d")

  excludedDays = Convert(args.exclusion)
  

  if "file" in excludedDays:
    excludedDays = data['skipdays']

  for i in range(5):
      if daysofweek[i] not in excludedDays:
       sendwork(day="%s" % (obj_date + datetime.timedelta(days=i)).strftime('%Y-%m-%d'),
              id=data['id'],
              key=data['key'],
              typeofwork=data['typeofwork'],
              starthour=str(data['starthour']),
              endhour=str(data['endhour']))

if __name__ == '__main__':
    main()
