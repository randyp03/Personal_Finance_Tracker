import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def draw_net_income(df):
    net_income_df = df.copy()
    net_income_df.loc[net_income_df['Category'] != 'Income', 'Amount'] *= -1
    net_income_df = net_income_df.groupby(['Month'])[['Amount']].sum().sort_values('Amount', ascending=False)
    net_income_df['Net_Status'] = ['Negative' if x < 0 else 'Positive' for x in net_income_df['Amount']]
    palette = {'Positive': '#4bd02b', 'Negative': '#e33434'}

    fig, ax = plt.subplots()
    sns.barplot(net_income_df,
                x='Month',
                y='Amount',
                hue = 'Net_Status',
                palette=palette,
                legend=False)
    ax.set_title('Net Income')
    ax.set_xlabel('Month')
    ax.set_ylabel('Amount')
    plt.tight_layout()

    return plt.show()

def draw_categorical_expenses(df):
    fig, ax = plt.subplots()
    sns.barplot(df.loc[df['Category'] != 'Income'].groupby('Category')[['Amount']].sum().sort_values('Amount', ascending=False),
                x='Amount',
                y='Category',
                orient='h')
    ax.set_title('Categorical Expenses')
    ax.set_xlabel('Amount')
    ax.set_ylabel('Category')
    plt.tight_layout()

    return plt.show()

def draw_monthly_expenditure(df):
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(df.loc[df['Category'] != 'Income'].groupby(['Month','Sub-Category'])[['Amount']].sum().sort_values('Amount', ascending=False),
                x='Amount',
                y='Month',
                hue="Sub-Category",
                dodge=False,
                orient='h')
    ax.set_title('Monthly Expenditure')
    ax.set_xlabel('Amount')
    ax.set_ylabel('Category')
    plt.tight_layout()

    return plt.show()

def draw_cumsum_plot(df):
    df=df.loc[df['Category'] != 'Income']
    fig, ax = plt.subplots()
    sns.lineplot(x=df['Date'],
                 y=df['Amount'].cumsum())
    ax.set_title('Amount Spent Over Time')
    ax.set_xlabel('Date')
    ax.set_xticks(ax.get_xticks()[::5]) 
    plt.tight_layout()

    return plt.show()


def plot(PLOTS, df):
    print()
    print(f"{'*' * 15} Available Charts {'*' * 15}")
    for plot in PLOTS:
        print(f"{plot} - {PLOTS[plot]}")

    choice = int(input('\nWhich visual would you like to view? '))
    
    try:
        if choice == 0:
            return
        elif choice == 1:
            draw_net_income(df)
        elif choice == 2:
            draw_categorical_expenses(df)
        elif choice == 3:
            draw_monthly_expenditure(df)
        elif choice == 4:
            draw_cumsum_plot(df)
    except KeyError:
        print('\nInvalid option. Please enter an option from the available list.\n')
        plot(PLOTS)

def main(csv_file):
    DATE_FORMAT = '%m-%d-%Y'
    df = pd.read_csv(csv_file)

    visuals_df = df.copy().sort_values('Date')
    visuals_df['Date_Formatted'] = pd.to_datetime(visuals_df['Date'], format=DATE_FORMAT)
    visuals_df['Month'] = visuals_df['Date_Formatted'].dt.month

    PLOTS = {
        0: 'Exit',
        1: 'Monthly Net Income',
        2: 'Categorical Expenses',
        3: 'Monthy Expenditure',
        4: 'Cumulative Sum of Dollars Spent',
    }

    plot(PLOTS, visuals_df)

if __name__ == "__main__":
    csv_file = 'transactions.csv'
    
    main(csv_file)