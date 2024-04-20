from src.helper import extract_answers_from_qr
from src.instantiate_fhir import questionnaire_from_json, questionnaireresponse_from_json, patient_from_answers

def main():
    # define the file paths for the example data inputs
    questionnaire_file = 'data/patient-q.json'
    response_file = 'data/patient-qr.json'
    
    # Convert JSON files to FHIR resources
    questionnaire = questionnaire_from_json(questionnaire_file)
    response = questionnaireresponse_from_json(response_file)
    
    # Extract answers with codes from QuestionnaireResponse
    extracted_values = extract_answers_from_qr(questionnaire, response)

    # Initialize the patient resource using extracted values
    patient = patient_from_answers(extracted_values)

    # Output the populated patient resource
    print(patient.json(indent=4))

if __name__ == "__main__":
    main()
