import os
import json
import jsonschema
from jsonschema import validate
from jsonschema import Draft7Validator

def validate_json(json_data, schema):
    errorLogs = []
    try:
        validate(instance=json_data, schema=schema)
        
    except jsonschema.exceptions.ValidationError as err:
    	
        v = Draft7Validator(schema)
        errors = sorted(v.iter_errors(json_data), key=lambda e: e.path)
        
        for error in errors:
            errorLogs.append("<br />")
            errorLogs.append(error.message)
            
        return False, "Due to error(s) above, given JSON data is inValid!", errorLogs

    message = "Given JSON data is Valid!"
    successLog = []
    return True, message, successLog

logs = []
for jsonFile in os.listdir("event"):
    if jsonFile.endswith(".json"): 
        logs.append("-------------------------------------------------------------------------------<br />")
        logs.append("------------Checking " +  jsonFile + " file------------<br />")
        with open(os.path.join("event", jsonFile), 'r') as file:
            jsonFile = json.load(file)
        
        for schemaFile in os.listdir("schema"):
        
            if schemaFile.endswith(".schema"): 
                logs.append("*** Checking against " + schemaFile + " ***")
                with open(os.path.join("schema", schemaFile), 'r') as file:
                    schemaFile = json.load(file)
                is_valid, msg, errorLogs = validate_json(jsonFile, schemaFile)
                logs = logs + errorLogs
                logs.append(msg)
                logs.append("\n")
        logs.append("\n")
        continue
    else:
        continue

with open('logs.txt', 'w') as f:
    for item in logs:
        f.write("%s\n" % item)
       


