from datetime import datetime

date_format = "%m-%d-%Y"
CATEGORIES = {'I': 'Income',
              'S': 'Savings',
              'E': 'Expense'}

def get_date(date_format=date_format):
    date_str = input('Enter Transaction Date or press enter for today\'s date: ')
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
    category = input('\nEnter Category Code: ')
    try:
        if category in categories.keys():
            return categories[category]
        else:
            raise KeyError('Invalid Category Code. Enter a Category Code from the Category List')
    except KeyError as e:
        print()
        print(e)
        print()
        return get_category(categories)

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
