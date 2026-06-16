# Expected Delivery Date Module.
# Calculates the due date and current weeks of pregnancy from the last menstrual period (LMP).

from datetime import date, timedelta


# Calculate the expected delivery date (EDD) by adding 280 days to the LMP.
def calculate_edd(lmp):
    edd = lmp + timedelta(days=280)
    return edd


# Calculate how many full weeks have passed since the LMP.
def calculate_weeks(lmp):
    today = date.today()
    days_passed = (today - lmp).days
    weeks = days_passed // 7
    return weeks

