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

def get_date(date_format=DATE_FORMAT):
    date_str = input('Enter Transaction Date or press enter for today\'s date (mm-dd-yyyy): ')
    if not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        date = datetime.strptime(date_str, date_format)
        return date.strftime(date_format)
    except ValueError:
        print('\nInvalid date format. Please enter in mm-dd-yyyy format.\n')
        return get_date(date_format)


def get_category(categories=CATEGORIES):
    print(f"{'*' * 15} Categories {'*' * 15}")
    for cat in categories:
        print(f"{cat} - {categories[cat]}")
    try:
        category = input('\nEnter Category Code: ').upper()
        if category in categories.keys():
            return categories[category]
        else:
            raise KeyError('Invalid Category Code. Enter a Category Code from the Category List')
    except KeyError as e:
        print()
        print(e)
        print()
        return get_category(categories)

def get_sub_cat(chosen_cat, sub_cats=SUB_CATEGORIES):
    sub_cat_list = SUB_CATEGORIES[chosen_cat[0]]
    print(f"{'*' * 15} Sub-Categories {'*' * 15}")
    for i in range(len(sub_cat_list)):
        print(f'{i+1} - {sub_cat_list[i]}')
    try:
        sub_cat_choice = int(input('\nEnter Sub-Category Code: '))
        return sub_cat_list[sub_cat_choice - 1]
    except IndexError:
        print('\nPlease enter a sub-category from list above')
        return get_sub_cat()
    pass

def get_memo():
    memo = input('Enter a short memo: ')
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