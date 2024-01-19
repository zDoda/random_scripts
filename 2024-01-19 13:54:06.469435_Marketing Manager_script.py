
# Here is a simple python script for a marketing manager
# You can customize and expand this according to your specific requirements

# Define a function to calculate the return on investment (ROI)
def calculate_roi(investment, revenue):
    return (revenue - investment) / investment * 100

# Example usage of the function
investment_amount = 1000
revenue_generated = 1500
roi = calculate_roi(investment_amount, revenue_generated)
print("The ROI is: {}%".format(roi))
