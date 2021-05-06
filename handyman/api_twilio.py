## Twilio API

import os
from twilio.rest import Client

account_sid = os.environ["TWILIOSID"]
auth_token = os.environ["TWILIOTOKEN"]
client = Client(account_sid, auth_token)

# Text

message = client.messages \
.create(
  body="Hello World",
  from_= os.environ["TWILIOPHONE"],
  to = os.environ["MYPHONE"]
)

print(message.sid)

# Call

call = client.calls.create(
  twiml='<Response><Say>Hello World</Say></Response>',
  to = os.environ["MYPHONE"],
  from_ = os.environ["TWILIOPHONE"]
)

print(call.sid)
