from flask import Flask, request, jsonify
import json
from image_generator import generate_advertisement_collage, generate_divided_scenario
from openai import OpenAI
import base64
from io import BytesIO

app = Flask("Name")

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/generate-collage', methods=['POST'])
def generate_collage():
    data = request.json
    base_prompt = data['base_prompt']
    scenes = int(data['scenes'])

    # Create OpenAI client
    client = OpenAI(api_key='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')

    # Generate scenario
    
    divided_scenario = generate_divided_scenario(client, base_prompt, scenes)
    
    if not divided_scenario:
        return jsonify({'error': "Failed to generate a divided scenario."}), 500

    # Generate images for each scene in the scenario
    
    collage = generate_advertisement_collage(client, divided_scenario, scenes)
    
    if collage:
        
        buffered = BytesIO()
        
        collage.save(buffered, format="JPEG")
        
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return jsonify({'scenario': divided_scenario, 'images': [img_str]})
        
    else:
        return jsonify({'error': "Failed to generate collage."}), 500
    

if __name__ == '_main_':
    app.run(debug=True)