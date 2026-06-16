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

# Calculate which trimester based on weeks pregnant.
def get_trimester(weeks):
    """Return trimester name and week range as a tuple."""
    if weeks <= 13:
        return "First trimester", "Weeks 1-13"
    elif weeks <= 26:
        return "Second trimester", "Weeks 14-26"
    elif weeks <= 40:
        return "Third trimester", "Weeks 27-40"
    else:
        return "Post-term", "After week 40"


# Calculate how many days remain until the expected delivery date.
def days_until_edd(edd_date):
    """Return days remaining until due date, minimum 0."""
    return max((edd_date - date.today()).days, 0) 

