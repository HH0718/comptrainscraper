import configparser


from twilio.rest import Client

config = configparser.ConfigParser()
config.read('config.ini')

account_sid = config['twilio']['account_sid']
auth_token = config['twilio']['auth_token']
client = Client(account_sid, auth_token)


def send_message(from_, to, body):
    message = client.messages.create(
        to=to,
        body=body,
        from_=from_)
    print("Message sent.")
    return True


if __name__ == "__main__":
    body = 'this is a test message using twilio.'
    send_message(config['from']['pa'], config['to']['james'], body)
