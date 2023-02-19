from twilio.rest import TwilioRestClient
import socket

client = TwilioRestClient(account='ACce0aedbdaa15199a1dc02f76a36a066a', token='4069c08cbcf778f5a50735ec36c2ce6a')
IP = socket.gethostbyname(socket.gethostname())

sendNum = '+17328238107'
fromNum = '+12675898097'

client.messages.create(to=sendNum, from_=fromNum, body=IP)
