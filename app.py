from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_data = response.json()
        return ip_data['ip']
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
        return "None"

@app.route('/')
def ip():
    return jsonify({'ip': get_public_ip()})


@app.route('/execute_code', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')
    output_var = data.get('output', '')

    local_vars = {}
    try:
        exec(code, {}, local_vars)
        output = local_vars.get(output_var, None)
    except Exception as e:
        return jsonify({'error': str(e)})

    return jsonify({'output': output})

@app.route('/requests', methods=['POST'])
def send_request():
    data = request.get_json()
    mode = data.get('mode', 'GET')
    args = data.get('args', [])
    kwargs = data.get('kwargs', {})

    try:
        if mode == 'GET':
            response = requests.get(*args, **kwargs)
        elif mode == 'POST':
            response = requests.post(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid mode'})

        response_data = {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'content': response.content.decode('utf-8', errors='ignore'),
            'json': response.json() if response.headers.get('Content-Type') == 'application/json' else None,
            'text': response.text,
            'url': response.url,
            'encoding': response.encoding,
            'elapsed': response.elapsed.total_seconds(),
            'history': [{'status_code': r.status_code, 'url': r.url} for r in response.history]
        }

        return jsonify({'response': response_data})

    except requests.RequestException as e:
        return jsonify({'error': str(e)})
