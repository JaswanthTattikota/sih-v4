from flask import Flask, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

api = os.getenv("GEMINI_API_KEY")
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api
@app.route('/', methods=['POST'])
def get_response():
    try:
        course = request.get_json().get('courseData')
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": 
                            f'''
                            Generate 18 multiple choice questions with 4 options from the {course}. It must include 10 easy, 5 medium and 3 hard questions in order. It should cover all the concepts present in the {course} and all the modules present in the {course}.
                            Give the output strictly in json format:
                            {{
                                "quizName": "string",
                                "easy" : [
                                    {{
                                        "question": "string",
                                        "options": ["strings"],
                                        "correctOption": "Number" // index of correct option
                                    }}],
                                "medium" : [
                                    {{
                                        "question": "string",
                                        "options": ["strings"],
                                        "correctOption": "Number" // index of correct option
                                    }}],
                                "hard" : [
                                    {{
                                        "question": "string",
                                        "options": ["strings"],
                                        "correctOption": "Number" // index of correct option
                                    }}],
                                        
                            }}
                          '''
                        }
                    ]
                }
            ]
        }

        # Set the headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the API call
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            # Parse and print the response JSON
            response_json = response.json()
            if (response_json["candidates"][0]["content"]["parts"][0]["text"][0]=="{"):
                return (response_json["candidates"][0]["content"]["parts"][0]["text"])
            else:
                if response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3][0]=="J" or response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3][0]=="j":
                    return (response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3])
                else:
                    return (response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3])
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return json.dump(
            {
                "msg":"Error Assessing AI"
            }
            ) 

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)