CATEGORIES = ["food", "transport", "utilities", "entertainment", "other", "salary"]

# Categories that count as expenses (used by the recommendation engine --
# "salary" is income so it never shows up as something to "cut back on").
EXPENSE_CATEGORIES = [c for c in CATEGORIES if c != "salary"]

# JWT token lifetime
JWT_EXPIRATION_HOURS = 24
