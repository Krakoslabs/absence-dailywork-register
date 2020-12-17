# absence-dailywork-register
Register daily work hours in absence.io

# How to start
1.- Clone repository and install python requirements

```
git clone https://github.com/Krakoslabs/absence-dailywork-register.git
cd absence-dailywork-register
pip install -r requirements.txt
```

2.- Create tokenid for your user in absence.io

```
To use the absence.io API you will need an API Key. To generate one, please go to your profile in your absence.io account and click on the Integrations tab and click on the 'Generate API Key' button.

The ApiKey consists of two parts:

- The Key Identifier (id) used to identify your key
- The actual key
```

3.- Change the [data.yml](data.yml) to customize your inputs

```
---
id: replaceme
key: replaceme
starthour: '08:00'
endhour: '16:00'
typeofwork: work
skipdays: []
```

# Usage

`python absence.py -h`

```
usage: absence.py [OPTIONS]

Fill in daily work in Absence.io.It is always filling the whole week before as it is running or it has been specified
         - Use the data.yml to customize your inputs
               id: id from abscense.io
               key: key from absence.io
               starthour: Hour string to fill in as your start hour. Format: 'XX:YY'
               endhour: Hour string to fill in as your end hour. Format: 'XX:YY'
               typeofwork: Type of daily register. Allowed value: work
               skipdays: A list of days to be skipped in the registration.
                 example:
                   skipdays: ['Monday', 'Tuesday']

optional arguments:
  -h, --help         show this help message and exit
  --day DAY, -d DAY  Specify a date to fill the previous week of this day with this format: YYYY-MM-dd
  --week, -w         Use to fill in the whole previus week. Use to be croned in your computer
```
