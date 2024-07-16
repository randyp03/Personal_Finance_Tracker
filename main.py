import csv
from data_entry import get_date, get_category, get_memo, get_amount
import data_visuals
import os
import pandas as pd
import time

class CSV:
    CSV_file = 'transactions.csv'
    COLUMNS = ['Date','Category','Memo','Amount']
    date_format = "%m-%d-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_file, index=False)

    @classmethod
    def add_entry(cls, date:str, category:str, memo:str, amount:int):
        new_entry = {
            'Date': date,
            'Category': category,
            'Memo': memo,
            'Amount': amount
        }
        with open(cls.CSV_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, cls.COLUMNS)
            writer.writerow(new_entry)

        print('Transaction added successfully')

    @classmethod
    def get_summary(cls, start_date:str, end_date:str):
        df = pd.read_csv(cls.CSV_file)

        df['Date'] = pd.to_datetime(df['Date'], format="%d-%m-%Y").dt.strftime(cls.date_format)
        transaction_period = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
        if transaction_period.empty:
            print(f"\nThere are no transactions within {start_date} and {end_date}\n")
        else:
            print()
            print(f"Total Income: ${transaction_period[transaction_period['Category']=='Income']['Amount'].sum()}")     
            print(f"Total Spent: ${transaction_period[~transaction_period['Category'].isin(['Income','Savings'])]['Amount'].sum()}")   
            print(f"Total Savings: ${transaction_period[transaction_period['Category'].isin(['Savings'])]['Amount'].sum()}")

            if input('\nWould you like to view the dataset? (y/n) ').lower().startswith('y'):
                print()
                print(transaction_period)
    
    @classmethod
    def get_visuals(cls):
        data_visuals.main(cls.CSV_file)

            


if __name__ == "__main__":

    CSV.initialize_csv()

    while True:
        print(f'\n{"*" * 20} Choose an option {"*" * 20}')
        print('1: Add transaction')
        print('2: View transaction summary within a date range')
        print('3: View spending trends')
        print('4: Exit')
        
        choice = int(input('\nEnter an option: '))

        if choice == 1:
            print('\nYou chose to add a transaction\n')

            date = get_date()
            category = get_category()
            memo = get_memo()
            amount = get_amount()

            CSV.add_entry(date=date, category=category, memo=memo, amount=amount)

        elif choice == 2:
            print('\nYou chose to view transaction summary')

            print('\nEnter the start date and end date for the period you want to summarize (mm-dd-yyyy)')
            start_date = input('Start Date: ')
            end_date = input('End Date: ')

            CSV.get_summary(start_date=start_date,end_date=end_date)

        elif choice == 3:
            CSV.get_visuals()

        elif choice == 4:
            print('\nYou chose to exit')
            break

        else:
            print('Invalid option. Please chose one of the options available.')