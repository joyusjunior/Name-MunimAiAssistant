
import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
import os

# Initialize ledger if it doesn't exist
LEDGER_FILE = "ledger.csv"
if not os.path.exists(LEDGER_FILE):
    df_init = pd.DataFrame(columns=["Date", "Type", "Description", "Amount"])
    df_init.to_csv(LEDGER_FILE, index=False)

st.set_page_config(page_title="MunimAi Assistant", layout="centered")

st.title("📚 MunimAi Assistant")
st.markdown("Your ultimate accounting buddy – create invoices, track expenses, and manage your ledger.")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🧾 Create Invoice", "💰 Add to Ledger", "📊 View Ledger"])

# ---------------- INVOICE GENERATOR ----------------
with tab1:
    st.header("🧾 Invoice Generator")
    client = st.text_input("Client Name")
    item = st.text_input("Service/Product")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    today = datetime.date.today()

    if st.button("Generate Invoice"):
        if client and item and amount:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="INVOICE", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(100, 10, txt=f"Date: {today}", ln=True)
            pdf.cell(100, 10, txt=f"Client: {client}", ln=True)
            pdf.cell(100, 10, txt=f"Item: {item}", ln=True)
            pdf.cell(100, 10, txt=f"Amount: ₹{amount}", ln=True)

            file_name = f"invoice_{client.replace(' ', '_')}_{today}.pdf"
            pdf.output(file_name)

            with open(file_name, "rb") as f:
                st.download_button("📥 Download Invoice", f, file_name=file_name)
        else:
            st.warning("Please fill in all fields.")

# ---------------- ADD TO LEDGER ----------------
with tab2:
    st.header("💰 Record Transaction")
    t_type = st.selectbox("Transaction Type", ["Income", "Expense"])
    desc = st.text_input("Description")
    t_amt = st.number_input("Amount", min_value=0.0, step=0.01)
    t_date = st.date_input("Date", value=today)

    if st.button("Save Transaction"):
        if desc and t_amt:
            new_entry = pd.DataFrame([[t_date, t_type, desc, t_amt]],
                                     columns=["Date", "Type", "Description", "Amount"])
            new_entry.to_csv(LEDGER_FILE, mode='a', header=False, index=False)
            st.success("Transaction saved!")
        else:
            st.warning("Please fill in all fields.")

# ---------------- VIEW LEDGER ----------------
with tab3:
    st.header("📊 Ledger Summary")
    ledger = pd.read_csv(LEDGER_FILE)

    st.subheader("Recent Entries")
    st.dataframe(ledger.tail(10))

    income = ledger[ledger["Type"] == "Income"]["Amount"].sum()
    expense = ledger[ledger["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    st.metric("💵 Total Income", f"₹{income:,.2f}")
    st.metric("🧾 Total Expenses", f"₹{expense:,.2f}")
    st.metric("💰 Current Balance", f"₹{balance:,.2f}")
