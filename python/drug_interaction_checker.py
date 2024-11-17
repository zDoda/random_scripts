#!/usr/bin/env python3

# Here is an example script for a basic drug interaction check

import requests

def get_interaction(drug_list):
    url = "https://rxnav.nlm.nih.gov/REST/interaction/list.json?rxcuis=" + '+'.join(drug_list)
    response = requests.get(url)
    if response.status_code != 200:
        print("Error: Could not retrieve information")
        return None
    return response.json()

def print_interactions(interactions):
    for interactionTypeGroup in interactions.get("interactionTypeGroup", []):
        for interactionType in interactionTypeGroup.get("interactionType", []):
            for interactionPair in interactionType.get("interactionPair", []):
                for interactionConcept in interactionPair.get("interactionConcept", []):
                    minConcept = interactionConcept.get("minConceptItem", {})
                    name = minConcept.get("name")
                    print("Drug:", name)
                severity = interactionPair.get("severity")
                description = interactionPair.get("description")
                print("Severity:", severity)
                print("Description:", description)
                print()

def main():
    # Example list of drug RxNorm IDs
    drug_list = ["341248", "860975"]  # These are RxNorm IDs for Aspirin and Ibuprofen
    
    print("Checking drug interactions...")
    interactions = get_interaction(drug_list)
    if interactions:
        print_interactions(interactions)
    else:
        print("No interactions found or an error occurred.")

if __name__ == "__main__":
    main()
