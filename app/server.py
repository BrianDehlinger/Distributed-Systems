from flask import Flask, escape, request, jsonify
from app.Questions import Question, MultipleChoiceQuestion, MatchingQuestion

app = Flask(__name__)

activeMultipleChoiceQuestion = None
activeMatchingQuestion = None

@app.route('/')
def welcome():
    name = request.args.get("name", "World")
    return f'Welcome to Quiz API v1!'

@app.route('/activateQuestion', methods=['POST'])
def activateQuestion():
	global activeMultipleChoiceQuestion
	global activeMatchingQuestion
	if activeMultipleChoiceQuestion is not None or activeMatchingQuestion is not None:
		return f'There is Already an Active Question!'
	data = request.json
	if data["questionType"] == "multChoice":
		activeMultipleChoiceQuestion = MultipleChoiceQuestion(prompt=data["prompt"], choices=data["choices"], answer=data["answer"])
	else:
		activeMatchingQuestion = MatchingQuestion(prompt=data["prompt"], left_choices=data["leftChoices"], right_choices=data["rightChoices"], answer_mapping=data["answerMapping"])
	return jsonify(data)

@app.route('/fetchResponses', methods=['GET'])
def fetchResponses():
	global activeMultipleChoiceQuestion
	global activeMatchingQuestion
	if activeMultipleChoiceQuestion is not None:
		return activeMultipleChoiceQuestion.response
	elif activeMatchingQuestion is not None:
		return activeMatchingQuestion.response
	return f'No Active Question!'

@app.route('/deactivateQuestion', methods=['POST'])
def deactivateQuestion():
	global activeMultipleChoiceQuestion
	global activeMatchingQuestion
	if activeMultipleChoiceQuestion is not None:
		responses = activeMultipleChoiceQuestion.response
		activeMultipleChoiceQuestion = None
		return f'Multiple Choice Question Deactivated!'
	if activeMatchingQuestion is not None:
		activeMatchingQuestion = None
		return f'Matching Question Deactivated!'
	return f'No Question Was Active!'

@app.route('/recordResponse', methods=['POST'])
def recordResponse():
	global activeMultipleChoiceQuestion
	if activeMultipleChoiceQuestion:
		activeMultipleChoiceQuestion.response[request.json["response"]] += 1
		return jsonify(activeMultipleChoiceQuestion.response)
	return f'No Active Question!'
