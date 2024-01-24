#!/usr/bin/env python3

import json

# Define the FAQ dictionary
faq_dict = {
    "What is your return policy?":
        "Our return policy lasts 30 days. If 30 days have gone by since your purchase, "
        "unfortunately, we can’t offer you a refund or exchange. To be eligible for a return, your item must "
        "be unused and in the same condition that you received it. It must also be in the original packaging.",
    "How do I change my order?":
        "If you need to change or cancel your order, please contact us immediately. Once our warehouse has "
        "processed your order, we will be unable to make any changes.",
    "Do you ship internationally?":
        "Yes, we ship worldwide. Shipping costs will apply, and will be added at checkout. "
        "We run discounts and promotions all year, so stay tuned for exclusive deals."
}

# Function to auto-generate response templates based on frequently asked questions
def generate_response_templates(faq):
    templates = {}
    for question, answer in faq.items():
        template_name = "Response to \"" + question + "\""
        templates[template_name] = {
            "question": question,
            "response": answer
        }
    return templates

# Generate the response templates
response_templates = generate_response_templates(faq_dict)

# Optionally write the response templates to a JSON file
json_filename = "response_templates.json"
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(response_templates, f, ensure_ascii=False, indent=4)

print(f"Response templates saved to {json_filename}")

# To use a template, just call the function with a specific question
def get_response(question):
    return response_templates.get("Response to \"" + question + "\"", {}).get('response', "Sorry, I don't understand the question.")

# Example of using the get_response function
example_question = "Do you ship internationally?"
print(f"Response to the question '{example_question}': {get_response(example_question)}")
