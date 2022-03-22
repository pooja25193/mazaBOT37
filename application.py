from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import processor
import sys
import datetime;

applicationlication = Flask(__name__)
CORS(applicationlication)

applicationlication.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'

@applicationlication.route('/', methods=["GET", "POST"])
def index():
    '''
    new_email = request.form.get("email")
    new_priority = request.form.get("priority")
    new_question = request.form.get("question")
    print(new_question)
    if request.method == 'POST' and new_question:
        #print(listdir) ## print listdir python 2
        # write to file
        with open('questions.txt', 'a') as f:
            f.write(str(new_email+","+new_priority+","+new_question+","+str(datetime.datetime.now())))
            f.write("\n")
        with open('questions.csv', 'a') as f:
            f.write(str(new_email+","+new_priority+","+new_question+","+str(datetime.datetime.now())))
            f.write("\n")
        print("done")
        flash('Success')
        return jsonify({'question' : new_question})
    
    '''
    return render_template('base.html', **locals())

@applicationlication.route('/process', methods=["GET", "POST"])
def process():
    new_email = request.form["email"]
    print(new_email)
    new_priority = request.form["priority"]
    print(new_priority)
    new_question = request.form["question"]
    print(new_question)
    
    if request.method == 'POST' and new_question:

        with open('questions.txt', 'a') as f:
            f.write(str(new_email+","+new_priority+","+new_question+","+str(datetime.datetime.now())))
            f.write("\n")
        with open('questions.csv', 'a') as f:
            f.write(str(new_email+","+new_priority+","+new_question+","+str(datetime.datetime.now())))
            f.write("\n")
        print("applicationlicationended in CSV")
        
        return jsonify({'name' : "Your Question: " +new_question+ " was sucessfully submitted."})
        
    return jsonify({'error' : "Unsuccessful"})

@applicationlication.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():

    if request.method == 'POST':
        the_json = request.get_json("message")
        the_question = the_json["message"]
        #the_question = request.form['question']
        print("This is the message")
        print(the_question, file=sys.stderr)

        response = processor.chatbot_response(the_question)
        print(response, file=sys.stdout)

    return jsonify({"answer": response })

# @applicationlication.route('/predict', methods=["POST"])
# def predict():
#     text = request.get_json("message")
#     response = get_response(text)
#     message = {"answer":response}
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return jsonify(message)


if __name__ == '__main__':
    #applicationlication.run(debug=True)
    applicationlication.run(host='0.0.0.0', port='5000', debug=True)


