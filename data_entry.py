# This file gets the information of transactions before adding to csv file

# importing libraries
from datetime import datetime

DATE_FORMAT = "%m-%d-%Y"
CATEGORIES = {'I': 'Income',
              'S': 'Savings & Investments',
              'E': 'Essential',
              'N': 'Non-Essential'}

SUB_CATEGORIES = {
    'I': ['Income','Income 2','Income 3'],
    'S': ['Emergency Fund','Roth IRA'],
    'E': ['Bills & Utilities',
          'Medical',
          'Auto & Transport',
          'Education',
          'Health & Fitness',
          'Pets',
          'Groceries',
          'Student Loan',
          'Car Payment'],
    'N': ['Shopping',
          'Entertainment',
          'Food & Dining',
          'Gifts',
          'Travel',
          'Charity',
          'Subscriptions',
          'Other']
}

# returns either current date or custom date that user enters
def get_date(date_format=DATE_FORMAT):
    date_str = input('Enter Transaction Date or press enter for today\'s date (mm-dd-yyyy): ')
    # get today's date if user enters nothing
    if not date_str:
        return datetime.today().strftime(date_format)
    try:
        # checks if date entered is a future date
        if datetime.strptime(date_str, date_format) > datetime.today():
            raise ValueError
        # if date is valid, return the date
        date = datetime.strptime(date_str, date_format)
        return date.strftime(date_format)
    except ValueError:
        print('\nInvalid date. Enter a valid date (mm-dd-yyyy) or press Enter to enter today\'s date. \n')
        return get_date(date_format)

# returns the category of the transaction
def get_category(categories=CATEGORIES):
    print(f"{'*' * 15} Categories {'*' * 15}")
    for cat in categories:
        print(f"{cat} - {categories[cat]}")
    try:
        category_code = input('\nEnter Category Code: ').upper()
        # checks if category code entered is a valid category code
        if category_code in categories.keys():
            return categories[category_code]
        else:
            raise KeyError('Invalid Category Code. Enter a Category Code from the Category List')
    except KeyError as e:
        print()
        print(e)
        print()
        return get_category()

# returns the sub-category of transaction
def get_sub_cat(chosen_cat, sub_cats=SUB_CATEGORIES):
    # uses first letter of category choses previously to determine which sub-categories to display
    sub_cat_list = sub_cats[chosen_cat[0]]
    print(f"{'*' * 15} Sub-Categories {'*' * 15}")
    for i in range(len(sub_cat_list)):
        print(f'{i+1} - {sub_cat_list[i]}')

    # checks if sub-category choice entered is a valid choice
    try:
        sub_cat_choice = int(input('\nEnter Sub-Category Code: '))
        return sub_cat_list[sub_cat_choice - 1]
    except IndexError or ValueError:
        print('\nPlease enter a sub-category from list above')
        return get_sub_cat()

# returns brief description of the transaction
def get_memo():
    memo = input('Enter a short memo: ')
    # memo has to be 50 characters or less
    if len(memo) > 50:
        print('\nMemo passed character limit. Please enter a memo no greater then 50 characters.\n')
        return get_memo()
    return memo

# returns the amount of the transaction
def get_amount():
    try:
        amount = float(input('Enter the amount: '))
        if amount <= 0:
            raise ValueError('Amount must be non-negative.')
        return amount
    except ValueError as e:
        print()
        print(e)
        print()
        return get_amount()