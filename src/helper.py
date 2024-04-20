import json
from datetime import datetime
from fhir.resources.questionnaireresponse import QuestionnaireResponse
from fhir.resources.questionnaire import Questionnaire
from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName

def instantiate_patient_from_answers(extracted_answers):
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

def extract_answers_from_qr(questionnaire, response):
    # Create a mapping from linkId to code from the Questionnaire
    linkid_to_code = {item.linkId: next((code.code for code in item.code if code.code), None) for item in questionnaire.item}

    extracted_values = []

    # Iterate through each response item
    for item in response.item:
        linkId = item.linkId
        code = linkid_to_code.get(linkId, 'Unknown Code')  # Get the code associated with the linkId, default to 'Unknown Code'
        if item.answer:  # Ensure there is at least one answer
            answer = item.answer[0]

            # Directly extracting the value based on its type
            value = None
            if hasattr(answer, 'valueString') and answer.valueString is not None:
                value = answer.valueString
            elif hasattr(answer, 'valueCoding') and hasattr(answer.valueCoding, 'display') and answer.valueCoding.display is not None:
                value = answer.valueCoding.display
            elif hasattr(answer, 'valueDate') and answer.valueDate is not None:
                value = answer.valueDate.isoformat()  # Convert date to string format if it's a datetime object

            # Append the result as a tuple of (linkId, code, value)
            if value is not None:
                extracted_values.append((linkId, code, value))

    return extracted_values
