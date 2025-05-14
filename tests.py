# utils.py

def test_nutrition(calories, proteins, fats, carbs):
    """Ensure all nutrition values are non-negative and realistic."""
    if any(n < 0 for n in [calories, proteins, fats, carbs]):
        return False
    if calories > 5000 or proteins > 500 or fats > 300 or carbs > 600:
        return False
    return True