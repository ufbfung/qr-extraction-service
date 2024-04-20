import json
from fhir.resources.questionnaireresponse import QuestionnaireResponse
from fhir.resources.questionnaire import Questionnaire
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName

def questionnaire_from_json(questionnaire_file):
    with open(questionnaire_file, 'r') as file:
        questionnaire_data = json.load(file)
    questionnaire = Questionnaire.parse_obj(questionnaire_data)

    return questionnaire

def questionnaireresponse_from_json(response_file):
    with open(response_file, 'r') as file:
        response_data = json.load(file)
    response = QuestionnaireResponse.parse_obj(response_data)

    return response

def patient_from_answers(extracted_answers):
    """Instantiates and returns a new Patient resource using extracted answers with dictionary mappings."""
    patient = Patient()
    patient.name = [HumanName(use='official')]

    # Mapping dictionary to convert codes to patient attributes
    attribute_mappings = {
        'first-name': ('name[0].given', lambda x: [x]),
        'lastname': ('name[0].family', lambda x: x),
        'sexatbirth': ('gender', lambda x: x.lower()),
        'dob': ('birthDate', lambda x: x)  # Assuming the date is already in the correct format
    }

    # Apply mappings to set patient attributes
    for linkId, code, value in extracted_answers:
        if code in attribute_mappings:
            attribute_path, transform = attribute_mappings[code]
            # Using exec to set the attribute dynamically
            exec(f"patient.{attribute_path} = transform(value)")

    return patient
