import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title and description
st.title("📊 Expense Tracker & Insights Dashboard")
st.write("Track your expenses and gain insights into your spending habits.")

# Initialize session state for storing expenses
if "expenses" not in st.session_state:
    st.session_state["expenses"] = pd.DataFrame(columns=["Date", "Category", "Amount"])

# Input section
st.header("Add a New Expense")
date = st.date_input("Date")
category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
amount = st.number_input("Amount", min_value=0.0, step=0.01)

if st.button("Add Expense"):
    new_expense = {"Date": date, "Category": category, "Amount": amount}
    st.session_state["expenses"] = pd.concat(
        [st.session_state["expenses"], pd.DataFrame([new_expense])],
        ignore_index=True,
    )
    st.success(f"Added ₹{amount} under {category}!")

# Display expenses
st.header("Your Expenses")
if not st.session_state["expenses"].empty:
    st.dataframe(st.session_state["expenses"])

    # Insights section
    st.header("Insights")
    category_summary = (
        st.session_state["expenses"]
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    # Display category summary
    st.subheader("Spending by Category")
    st.bar_chart(category_summary)

    # Pie chart
    st.subheader("Category Distribution")
    fig, ax = plt.subplots()
    ax.pie(
        category_summary,
        labels=category_summary.index,
        autopct="%1.1f%%",
        startangle=90,
    )
    ax.axis("equal")
    st.pyplot(fig)
else:
    st.write("No expenses added yet.")
