from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS package

from secret_ai_sdk.secret_ai import ChatSecret
from secret_ai_sdk.secret import Secret
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
# load from environment variables or from a .env file
from dotenv import load_dotenv
load_dotenv()

# Create a Secret object to interact with the Secret Network
secret_client = Secret()
# Get all the models registered with the smart contracts
models = secret_client.get_models()
# For the chosen model, you may obtain a list of LLM instance URLs to connect to
urls = secret_client.get_urls(model=models[0])
# You previously exported the env var SECRET_AI_API_KEY=YOUR-API-KEY
secret_ai_llm = ChatSecret(
    base_url=urls[0],  # in this case, we choose to access the first URL in the list
    model=models[0],  # your previously selected model
    temperature=0,  # set the temperature to 0 for deterministic results
)


class Invoice(BaseModel):
    invoice_number: str = Field(description="number of the invoice")
    date: str = Field(description="date of the invoice")
    client_name: str = Field(description="name of the client")
    type: str = Field(description="type of products or services")
    total_amount: str = Field(description="total amount of the invoice included tax")
    tax_amount: str = Field(description="tax amount")
    currency: str = Field(description="currency")


invoice_parser = PydanticOutputParser(pydantic_object=Invoice)


class Credibility(BaseModel):
    credibility: int = Field(description="credibility of the invoice")


credibility_parser = PydanticOutputParser(pydantic_object=Credibility)
credibility_instructions = credibility_parser.get_format_instructions()
print("credibility_instructions: ", credibility_instructions)
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/api/invoice', methods=['POST'])
def llm_proxy():
    dict_data = request.json
    # Traitez les données avec votre SDK LLM
    # response = your_llm_sdk.process(data)
    print("data from react: ", dict_data["data"])
    messages = [
        ("system", "You are a helpful assistant and accountant. " +
         "Given an invoice extract the invoice number, date," +
         "client name, type of products or services, " +
         "total amount of the invoice included tax, tax amount. " +
         "and currency." +
         "When you answer, give only the result in this json format: " +
         "{invoice_number: '1234', date: '2022-01-01', client_name: 'John Doe', " +
         "type: 'Software', total_amount: '1000', tax_amount: '200', currency: 'EUR'}"),
        ("human", dict_data["data"]),
    ]
    # Invoke the LLM
    response = secret_ai_llm.invoke(messages, stream=False)
    dict_response = dict(invoice_parser.invoke(response.content))
    print("answer: ", dict_response)
    return jsonify(dict_response)


@app.route('/api/credibility', methods=['POST'])
def credibility_proxy():
    dict_data = request.json
    # Traitez les données avec votre SDK LLM
    # response = your_llm_sdk.process(data)
    print("\n******\n")
    print("data from react: ", dict_data)
    messages = [
        ("system", "You are a helpful assistant and financial accounting auditor." +
         "Given an invoice and an accounting row in dict format, " +
         "determine if the invoice and row data are credible or not." +
         "Give a score between 0 and 100." +
         "0 is not credible, 100 is credible." +
         "If data of the row is not compatiblie with the invoice, " +
         "lower the score." +
         "Use a weighted approach for each field (e.g. invoice number, date, currency, amount, vendor). " +
         "Start at 100, subtract penalties based on mismatch levels, and clamp the final score between 0 and 100. " +
         "Give only your final score in this json format without your thinkings process."),
        ("human", "<instructions>" + credibility_instructions + "</instructions>" +
         "\nUse these inputs : \n" + "\naccouning row : \n" + str(dict_data["accounting_row"]) +
         "\ninvoice : \n" + dict_data["invoice"]),
    ]
    # Invoke the LLM
    response = secret_ai_llm.invoke(messages, stream=False)
    print("response:", response.content)
    dict_response = dict(credibility_parser.invoke(response.content))
    print("parsed json answer: ", dict_response)
    return jsonify(dict_response)


if __name__ == '__main__':
    app.run(debug=True)
