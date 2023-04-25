import os
from flask import Flask, request
import json
from guru2 import get_booking_page
from waitress import serve

app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    # To handle if another request is received while the API processing the previous request
    # Because we have one account to login the Guru website.
    if 'request_status.txt' in os.listdir():
        with open('request_status.txt', 'r') as f:
            file = f.read()
            in_process = int(file)
            if not in_process:
                with open('request_status.txt', 'w') as f:
                    f.write('1')
                    in_process = 0
            else:
                result = {
                    'GetAllCrudRobotsResponseItemViewModels': [],
                    'success': False,
                    'responseMessages': ['Please retry after 15 seconds.']
                }
                return result

    else:
        with open('request_status.txt', 'w') as f:
            f.write('1')
            in_process = 0

    if not in_process:
        if (request.method == 'POST'):
            data = json.loads(request.data.decode('utf-8'))
            try:
                result = get_booking_page(data)
                with open('request_status.txt', 'w') as f:
                    f.write('0')
                    in_process = 0
            except:
                with open('request_status.txt', 'w') as f:
                    f.write('0')
                    in_process = 0

            result['success'] = True
            result['responseMessages'] = []
            return result
    else:
        result = {
            'GetAllCrudRobotsResponseItemViewModels': [],
            'success': False,
            'responseMessages': ['Please retry after 15 seconds.']
        }
        return result


# host_IP = f'{input("Please inset IP:")}'
# host_port = f'{input("Please inset port:")}'
if __name__ == '__main__':
    serve(app=app, host='192.168.40.155', port='8087')
