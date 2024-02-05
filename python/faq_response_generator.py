#!/usr/bin/env python3

import random

class FAQGenerator:

    def __init__(self):
        self.faq_template = {
            "greeting": ["Hello, how can I help you?", "Hi there! What would you like to know?", "Greetings! How may I assist you today?"],
            "hours": ["We are open from {opening_time} to {closing_time}.", "Our working hours are from {opening_time} to {closing_time}.", "You can visit us between {opening_time} and {closing_time}."],
            "location": ["We are located at {address}.", "You can find us at {address}.", "Our address is {address}."],
            "payment_methods": ["We accept {methods}.", "You can pay through {methods}.", "The available payment methods are {methods}."],
            "refund_policy": ["Our refund policy is: {policy}.", "Regarding refunds, {policy}.", "For refunds, {policy}."]
        }

    def get_response(self, faq_category, **kwargs):
        if faq_category not in self.faq_template:
            return "I'm sorry, but I don't have information on that topic."

        template_options = self.faq_template[faq_category]
        template = random.choice(template_options)
        response = template.format(**kwargs)
        return response

def main():
    faq_gen = FAQGenerator()

    # Example usage
    print(faq_gen.get_response("greeting"))
    print(faq_gen.get_response("hours", opening_time="9 AM", closing_time="5 PM"))
    print(faq_gen.get_response("location", address="123 Example St."))
    print(faq_gen.get_response("payment_methods", methods="cash, cards, and mobile payments"))
    print(faq_gen.get_response("refund_policy", policy="you have 30 days to return your product for a full refund"))

if __name__ == "__main__":
    main(