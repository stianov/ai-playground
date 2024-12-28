from flask import Flask, request, jsonify
import requests, json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <title>AI playground</title>
    </head>
    <body>
        <section id="ai-playground">
        <h1>Lily's Flower Repository</h1>
        </section>
<script>
    const aiPlayground = document.getElementById('ai-playground');
    let improve = function() {
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: "Reply ONLY with HTMl code. Do not call any external resources like CSS or image files. Go crazy with colors etc.! Improve this page: " + aiPlayground.innerHTML }),
        })
        .then(response => response.json())
        .then(data => {
            aiPlayground.innerHTML = data.response;
            setTimeout(improve, 1000);
        })
        .catch(error => console.error('Error:', error));
};
        improve();
</script>
    </body>
</html>
    """

@app.route('/generate', methods=['POST'])
def generate():
    json_data = request.json
    prompt = json_data.get('prompt') if json_data else None

    if prompt is None:
        return jsonify({'error': 'No prompt provided'}), 400

    response = requests.post(
        "http://localhost:11434/api/generate",
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
        })
    )

    print(response.json())

    if response.status_code != 200:
        return jsonify({'error': 'Failed to fetch data from the external API'}), response.status_code

    response_data = response.json()

    ai_response = response_data.get('response')

    return jsonify({'response': ai_response})

if __name__ == '__main__':
    app.run()