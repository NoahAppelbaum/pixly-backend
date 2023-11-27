# pixly-backend

Pix.ly is a a webservice for hosting and editing images, built in Python with Flask and AWS S3. A frontend for this, built in React, can be found in [this repo](https://github.com/NoahAppelbaum/pixly-frontend).

# To Run:
To set up the dev environment, run
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

to run a local instance:
```
flask run
```

Or on most Macs:
```
flask run -p 5001 (or other port number)
```


You will need to supply a `.env` file with AWS credentials.
