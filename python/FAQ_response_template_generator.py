#!/usr/bin/env python3

import json
from jinja2 import Template

# Sample FAQs data, typically this would be read from a file or database
faqs_data = [
    {
        "question": "What is the return policy?",
        "answer": "You can return the product within 30 days of purchase."
    },
    {
        "question": "How long does shipping take?",
        "answer": "Shipping takes 5-7 business days."
    },
    {
        "question": "Do you provide international shipping?",
        "answer": "Yes, we ship to select countries outside the US."
    }
]

# Template for the FAQ response
response_template = """
<h1>Frequently Asked Questions (FAQ)</h1>
{% for faq in faqs %}
    <div class="faq-item">
        <h2>{{ faq.question }}</h2>
        <p>{{ faq.answer }}</p>
    </div>
{% endfor %}
"""

def generate_faq_response(faqs, template):
    """
    Generate a FAQ response based on the given template.

    :param faqs: List of FAQ objects.
    :param template: Jinja template for the FAQ layout.
    :return: The rendered template as a string.
    """
    template = Template(template)
    return template.render(faqs=faqs)

# Create the FAQ response using the template and the data
faq_response = generate_faq_response(faqs_data, response_template)

# Let's assume you want to write the response to an HTML file
output_filename = "faq_response.html"
with open(output_filename, "w") as f:
    f.write(faq_response)
