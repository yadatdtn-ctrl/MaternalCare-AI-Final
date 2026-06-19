# BMI Calculator Module.
# Calculates Body Mass Index from weight and height, then classifies the result.


# Calculate BMI from weight (kg) and height (metres).
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)


# Classify a BMI value as Underweight, Normal, or Overweight.
def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal"
    else:
        return "Overweight"

