import re
import requests

from apps.base.models import Sms_log


def is_valid_iran_code(input):
    if not re.search(r'^\d{10}$', input): return False
    check = int(input[9])
    s = sum(int(input[x]) * (10 - x) for x in range(9)) % 11
    return check == s if s < 2 else check + s == 11


def SendSms(code, type, receiver, message=None):
    res = requests.get(
        "https://api.kavenegar.com/v1/534A752B43716864485257724269726A2F624C3278696F7768472B314C504158/verify/lookup.json?receptor=" + receiver + "&token=" + code + "&template=" + type)
    obj = Sms_log()
    obj.type = type
    obj.receiver = receiver
    obj.code = code
    obj.message = message
    obj.status_code = res.status_code
    obj.save()
    return res.status_code

#
# def email_request(code, type, receiver, subject, message):
#     from_email = 'milad7akbari@gmail.com'
#     res = send_mail(subject, message, from_email, [receiver])
#     if res == 1:
#         EmailLog.objects.create(code=code, receiver=receiver, type=type , subject=subject , message=message)
#     return res
