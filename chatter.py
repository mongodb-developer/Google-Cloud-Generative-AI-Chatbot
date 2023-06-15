import vertexai
from vertexai.preview.language_models import ChatModel, TextGenerationModel


def predict_large_language_model_sample(
        project_id: str,
        model_name: str,
        temperature: float,
        max_output_tokens: int,
        top_p: float,
        top_k: int,
        location: str = "us-central1",
):
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)
    chat_model = ChatModel.from_pretrained(model_name)
    parameters = {
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
        "top_p": top_p,
        "top_k": top_k,
    }
    return chat_model, parameters


def predict_large_language_model_sentiment(
        project_id: str,
        model_name: str,
        temperature: float,
        max_decode_steps: int,
        top_p: float,
        top_k: int,
        content: str,
        location: str = "us-central1",
        tuned_model_name: str = "",
):
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    if tuned_model_name:
        model = model.get_tuned_model(tuned_model_name)
    response = model.predict(
        content,
        temperature=temperature,
        max_output_tokens=max_decode_steps,
        top_k=top_k,
        top_p=top_p, )
    return response.text


def chat_with_model(parameters, question, chat):
    conversation = {"question": question}
    response = chat.send_message(question, **parameters)
    print(response.text)
    conversation["response"] = response.text
    return response.text, conversation


def connect_cluster(srv):
    import pymongo
    client = pymongo.MongoClient(
        srv,
        tlsAllowInvalidCertificates=True)
    return client


def query_db(client, db_name, col_name, doc):
    db = client[db_name]
    col = db[col_name]
    x = col.find_one(doc)
    return x


def upsert_db(client, db_name, col_name, doc, customer_id):
    db = client[db_name]
    col = db[col_name]
    col.update_one({"customer_id": customer_id}, {"$push": {"conversation": doc}})


def insert_record(client, db_name, col_name, doc, customer_id):
    db = client[db_name]
    col = db[col_name]
    col.insert_one({"customer_id": customer_id, "conversation": ""})


def search_mongoDB_chat_base(db, col,client, question):
    db = client[db]
    col = db[col]
    response = col.aggregate([{'$search': {'index': 'default', 'text': {'query': question, 'path': 'question'}}}, {'$limit': 1}])
    return response


def search_mongoDB_claim(db, col,client, question):
    db = client[db]
    col = db[col]
    response = col.aggregate([{'$search': {'index': 'default', 'text': {'query': question, 'path': 'claim_number'}}}, {'$limit': 1}])
    return response
