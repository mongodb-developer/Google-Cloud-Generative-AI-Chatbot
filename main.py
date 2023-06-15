from flask import Flask, request, render_template

import chatter
from vertexai.preview.language_models import InputOutputTextPair

conversation = []

app = Flask(__name__)

# Constants
customer_id = "111"
db_name = "XYZ-Corp"
srv = "<your-connection-string>"
project_name = "gcp-pov"
# MongoDB initialization
conn = chatter.connect_cluster(srv)
intro_context = chatter.query_db(conn, db_name, "Insurance", {"type": "Intro"})
try:
    saved_conversation = chatter.query_db(conn, db_name, "Customer", {"customer_id": customer_id})
except:
    chatter.insert_record(conn, db_name, "Customer", {"customer_id": customer_id})

# Set Chat context and parameters
context = intro_context["context"]
chat_model, parameters = chatter.predict_large_language_model_sample(project_name, "chat-bison@001", 0.9, 200, 1, 40,
                                                                     "us-central1")

if saved_conversation:
    for i in saved_conversation["conversation"]:
        conversation.append(
            InputOutputTextPair(
                input_text=i["question"],
                output_text=i["response"]
            )
        )

chat = chat_model.start_chat(
    context=context,
    examples=conversation
)


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route('/chat', methods=["GET", "POST"])
def chat_with_ai():
    question = request.form['question']
    sentiment = chatter.predict_large_language_model_sentiment(project_name, "text-bison@001", 0.2, 5, 0.8, 1, '''respond only with sentiment and sentiment score. If positive respond "Positive" and its sentiment score separated by space. if negative respond with "Negative" and its sentiment score separated by space. Reply with Positive for all numeric values. reply with Negative value lesser than -1 for customer inputs like 'Not satisfied' for  input:'''+ question +'''"Classify the sentiment of the message:"''', "us-central1")
    if len(question) == 5 and question.isnumeric():
        claim_details = chatter.query_db(conn, db_name, "Claims", {"claim_number": question, "customer_id": customer_id})
        if claim_details:
            question = str(claim_details["claim_number"]) + " "+ claim_details["Name"]+" " + claim_details["Claim_status"] + " " + str(claim_details["Claim_amount"])+ " "+ claim_details["Currency"]
        else:
            question = "can not find the claim that you are looking for"
    search_response = chatter.search_mongoDB_index(conn,question)

    for item in search_response:
        print(question)
        print(">>>>>>>>>>>>>>>>")
        print(item)
        question = question + ": respond with abstract of the answer: " + item["Answer"]

    if sentiment.split(" ")[0] == "Negative" and float(sentiment.split(" ")[1]) < -1:
        question = question + ": respond with abstract of the answer: Do you want to connect with the customer " \
                              "service representative? "
    response_text, conversation = chatter.chat_with_model(parameters, question + ". Sentiment:"+ sentiment, chat)
    conversation["sentiment"] = sentiment
    chatter.upsert_db(conn, db_name, "Customer", conversation, customer_id)
    return response_text + " -- " + str(sentiment)


app.run(debug=True)
