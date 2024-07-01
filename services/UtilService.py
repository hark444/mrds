from datetime import datetime
import string
import secrets

def date_format(datetime_str, current_format='%d/%m/%y %H:%M:%S', required_format='%Y-%m-%d %H:%M:%S'):
    datetime_object = datetime.strptime(datetime_str, current_format)
    datetime_str = datetime_object.strftime(required_format)
    return datetime_object, datetime_str

def generate_referral_code():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(16))
    print(password)

if __name__ == '__main__':
    str = "3/4/21 8:9:10"
    print(date_format(str))