from twilio.rest import Client

account_sid = 'AC02d3219bbbc3a0edac9af72329f85a68'
auth_token = '3e1b37038e727c91dcdda733d3860210'

def send_sms(body,reciver):

    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+13392253483',
    body=str(body),
    to=reciver
    )

    print(message.sid)