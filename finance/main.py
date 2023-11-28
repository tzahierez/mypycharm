import urllib.parse

from flask import Flask, request, jsonify
import yfinance as yf
import http.client
from transformers import MarianMTModel, MarianTokenizer
import sentencepiece
import torch



import requests

app = Flask(__name__)

@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    stock_symbol = request.args.get('symbol', default='', type=str)
    if stock_symbol:
        stock = yf.Ticker(stock_symbol)
        stock_info = stock.info
        return jsonify(stock_info)  # Return the complete stock_info dictionary
    else:
        return "No stock symbol provided", 400

@app.route('/translate', methods=['GET'])
def translate_text():
    # Get query parameters for translation
    text_to_translate = request.args.get('text', default='')
    target_language = request.args.get('lang', default='he')

    conn = http.client.HTTPSConnection("text-translator2.p.rapidapi.com")

    # payload = "source_language=en&target_language=id&text=What%20is%20your%20name%3F"
    payload = urllib.parse.urlencode({
        'source_language': 'en',
        'target_language': target_language,
        'text': text_to_translate
    })

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'X-RapidAPI-Key': "e6b184d7cfmshffa15b93e8f5c3ap18013ajsne0bf016cabad",
        'X-RapidAPI-Host': "text-translator2.p.rapidapi.com"
    }

    conn.request("POST", "/translate", payload, headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

    # Check if the request was successful
    if res.status == 200:
        return data
    else:
        return jsonify({'error': 'Failed to translate text'}), res.status_code

@app.route('/translate_to_french', methods=['GET'])
def translate_to_french_api():
    # Get query parameters for translation a
    text_to_translate = request.args.get('text', default='')
    return translate_to_french(text_to_translate)


def translate_to_french(text):
    # Load the tokenizer and model
    model_name = "Helsinki-NLP/opus-mt-en-fr"
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Translate text
    translated = model.generate(**tokenizer(text, return_tensors="pt", padding=True))

    # Convert the output to text
    french_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

    return french_text[0]

# Example usage
#english_text = "Hello, how are you?"
#french_text = translate_to_french(english_text)
#print(french_text)

if __name__ == '__main__':
    app.run(debug=True)

#
# last working state:
#
# from flask import Flask, request, jsonify
# import yfinance as yf
# import http.client
#
#
# import requests
#
# app = Flask(__name__)
#
# @app.route('/get_stock_data', methods=['GET'])
# def get_stock_data():
#     stock_symbol = request.args.get('symbol', default='', type=str)
#     if stock_symbol:
#         stock = yf.Ticker(stock_symbol)
#         stock_info = stock.info
#         return jsonify(stock_info)  # Return the complete stock_info dictionary
#     else:
#         return "No stock symbol provided", 400
#
# @app.route('/translate', methods=['GET'])
# def translate_text():
#     # Get query parameters for translation
#     text_to_translate = request.args.get('text', default='')
#     target_language = request.args.get('lang', default='en')
#
#     conn = http.client.HTTPSConnection("text-translator2.p.rapidapi.com")
#
#     payload = "source_language=en&target_language=id&text=What%20is%20your%20name%3F"
#
#     headers = {
#         'content-type': "application/x-www-form-urlencoded",
#         'X-RapidAPI-Key': "e6b184d7cfmshffa15b93e8f5c3ap18013ajsne0bf016cabad",
#         'X-RapidAPI-Host': "text-translator2.p.rapidapi.com"
#     }
#
#     conn.request("POST", "/translate", payload, headers)
#
#     res = conn.getresponse()
#     data = res.read()
#
#     print(data.decode("utf-8"))
#
#     # Check if the request was successful
#     if res.status == 200:
#         return jsonify(res.msg)
#     else:
#         return jsonify({'error': 'Failed to translate text'}), res.status_code
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
