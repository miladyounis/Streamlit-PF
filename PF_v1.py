import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Function to load data without caching
def load_data():
    df = pd.read_excel('https://github.com/miladyounis/Streamlit-PF/blob/main/Streamlit%20PF%20v1.xlsx', sheet_name='Sheet1')
    return df

def prepare_data(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M')
    return df

def save_data(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Expenses')
    writer.save()
    output.seek(0)
    return output

def main():
    st.title("Budget Tracker")

    df = load_data()
    df = prepare_data(df)

    if st.checkbox('Show raw data'):
        st.subheader('Raw Data')
        st.write(df)

    st.subheader('Monthly Summary')
    monthly_summary = df.groupby('Month')['Amount'].sum().reset_index()
    st.write(monthly_summary)

    st.subheader('Expenditure by Category')
    category_summary = df.groupby('Category')['Amount'].sum()
    fig, ax = plt.subplots()
    category_summary.plot(kind='bar', ax=ax)
    st.pyplot(fig)

    st.subheader('Filter by Month')
    months = df['Month'].unique()
    selected_month = st.selectbox('Select a month', months)
    filtered_data = df[df['Month'] == selected_month]
    st.write(filtered_data)

    total_expenditure = filtered_data['Amount'].sum()
    st.write(f'Total Expenditure for {selected_month}: ${total_expenditure:.2f}')

    budget_goal = 1000
    st.write(f'Budget Goal: ${budget_goal:.2f}')
    remaining_budget = budget_goal - total_expenditure
    st.write(f'Remaining Budget: ${remaining_budget:.2f}')

    st.subheader('Add New Expense')
    with st.form(key='new_expense_form'):
        date = st.date_input('Date')
        amount = st.number_input('Amount', min_value=0.0, step=0.01)
        amount_sats = st.number_input('Amount in SATs', min_value=0.0, step=0.01)
        category = st.text_input('Category')
        selee = st.text_input('Selee')
        method = st.text_input('Method')
        comments = st.text_input('Comments')
        submit_button = st.form_submit_button(label='Add Expense')

        if submit_button:
            new_record = {
                'Date': date,
                'Amount': amount,
                'Amount in SATs': amount_sats,
                'Category': category,
                'Selee': selee,
                'Method': method,
                'Comments': comments
            }
            df = df.append(new_record, ignore_index=True)
            output = save_data(df)
            st.download_button(label='Download Updated Data', data=output, file_name='updated_expenses.xlsx')

if __name__ == '__main__':
    main()
