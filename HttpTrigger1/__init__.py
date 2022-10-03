import logging
import azure.functions as func
import json

import MeCab

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        body = json.dumps(req.get_json())
    except ValueError:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )
    
    if body:
        result = compose_response(body)
        return func.HttpResponse(result, mimetype="application/json")
    else:
        return func.HttpResponse(
             "Invalid body",
             status_code=400
        )


def compose_response(json_data):
    values = json.loads(json_data)['values']
    
    # Prepare the Output before the loop
    results = {}
    results["values"] = []
    
    for value in values:
        output_record = transform_value(value)
        if output_record != None:
            results["values"].append(output_record)
    return json.dumps(results, ensure_ascii=False)

## Perform an operation on a record
def transform_value(value):
    try:
        recordId = value['recordId']
    except AssertionError  as error:
        return None

    # Validate the inputs
    try:         
        assert ('data' in value)
        data = value['data']        
        assert ('text' in data)
    except AssertionError  as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    try:                
        tagged_text, extract_words = extract_word(data)

    except Exception as error:
        return (
            {
            "recordId": recordId,
            "errors": [ { "message": "Error:" + error.args[0] }   ]       
            })

    return ({
            "recordId": recordId,
            "data": {
                "tagged_text": tagged_text,
                "extract_words": extract_words
                    }
            })


def extract_word(text):
    word_list = []
    tagger = MeCab.Tagger("-Owakati")
    tag_list = tagger.parse(str(text)).split()
    target_list = ["公立", "歴史", "私立"]
    for target in target_list:
        if target in tag_list:
            print(target, "OK")
            word_list.append(target)
    return tag_list, word_list 