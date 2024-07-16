import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def draw_cat_dist(df):
    fig, ax = plt.subplots()
    sns.barplot(df.groupby('Category')[['Amount']].sum(),
                x='Amount',
                y='Category', 
                orient='h')
    ax.set_title('Categorical Distribution')
    ax.set_xlabel('Amount')
    ax.set_ylabel('Category')
    plt.tight_layout()

    return plt.show()


def draw_monthly_plot(df):
    fig, ax = plt.subplots()
    sns.lineplot(df.groupby(df['Date_Formatted'].dt.month)[['Amount']].sum(),
                 x='Date_Formatted',
                 y='Amount')
    ax.set_title('Amount Spent per Month')
    ax.set_xlabel('Date')
    plt.tight_layout()

    return plt.show()


def draw_cumsum_plot(df):
    fig, ax = plt.subplots()
    sns.lineplot(x=df['Date'],
                 y=df['Amount'].cumsum())
    ax.set_title('Amount Spent Over Time')
    ax.set_xlabel('Date')
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
            draw_cat_dist(df)
        elif choice == 2:
            draw_monthly_plot(df)
        elif choice == 3:
            draw_cumsum_plot(df)
    except KeyError:
        print('\nInvalid option. Please enter an option from the available list.\n')
        plot(PLOTS)

def main(csv_file):
    DATE_FORMAT = '%m-%d-%Y'
    df = pd.read_csv(csv_file)

    visuals_df = df.copy()
    visuals_df['Date_Formatted'] = pd.to_datetime(visuals_df['Date'], format=DATE_FORMAT)

    PLOTS = {
        0: 'Exit',
        1: 'Amount Spent by Category',
        2: 'Amount Spent by Month',
        3: 'Cumulative Sum of Dollars Spent',
    }

    plot(PLOTS, visuals_df)

if __name__ == "__main__":
    # csv_file = 'transactions.csv'
    
    main(csv_file)






