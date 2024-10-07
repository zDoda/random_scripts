#!/usr/bin/env python3

from docxtpl import DocxTemplate
import jinja2
import datetime

# Define the data for the legal document
context = {
    'party1_name': 'John Doe',
    'party2_name': 'Jane Smith',
    'agreement_date': datetime.date.today().strftime('%B %d, %Y'),
    'effective_date': (datetime.date.today() + datetime.timedelta(days=10)).strftime('%B %d, %Y'),
    'agreement_subject': 'Confidentiality Agreement',
    # More context variables can be added depending on the legal document requirements
}

def generate_legal_document(template_path, context, output_path):
    """
    Generate a legal document based on a template and context

    :param template_path: string, path to the docx template
    :param context: dict, data to be applied to the template
    :param output_path: string, path for the generated legal document
    """
    try:
        # Load the docx template
        doc = DocxTemplate(template_path)
        
        # Render the context (variables) in the docx template
        doc.render(context)
        
        # Save the generated legal document
        doc.save(output_path)
        print(f"Legal document generated successfully at: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Define paths to the template and the output file
    template_path = 'path/to/legal_document_template.docx'
    output_path = 'path/to/generated_legal_document.docx'
    
    # Generate the legal document
    generate_legal_document(template_path, context, output_path)
