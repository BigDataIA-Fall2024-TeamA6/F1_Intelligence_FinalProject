import streamlit as st
from streamlit.components.v1 import html
import streamlit.components.v1 as components
import mysql.connector
import json

import os
from dotenv import load_dotenv
import stripe

load_dotenv()

stripe.api_key = os.getenv("STRIPE_KEY")

connection = mysql.connector.connect(
    host = 'bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com',
    user='admin',
    password='amazonrds7245',
    database='bdia_team6_finalproject_db'    
)

def validate_output(ticket_info):
    cursor = connection.cursor()
    if ticket_info['location'] or ticket_info['count'] or ticket_info['cost']:
        race_results = cursor.execute("SELECT * FROM validation_table LIMIT 1;")
        upcoming_race = cursor.fetchall()
        st.write("Data from database")
        st.write(upcoming_race[0])
        
        


customer_id = st.session_state.get('username')

ticket_info = st.session_state.get("ticket_info")
# st.write(ticket_info)
# validate_output(ticket_info)



if 'payment_status' not in st.session_state:
    st.session_state.payment_status = None
if 'checkout_id' not in st.session_state:
    st.session_state.checkout_id = None


def create_checkout_session(amount,ticket_nos, currency='usd'):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': currency,
                        'unit_amount': int(amount), 
                        'product_data': {
                            'name': 'F1 Race Tickets',
                        },
                    },
                    'quantity':ticket_nos,
                }],
                mode='payment',
                success_url= 'http://localhost:8501/success.html',
                cancel_url= 'http://localhost:8501/cancel.html',
            )
            return checkout_session
        except Exception as e:
            st.error(f"Error creating checkout session: {str(e)}")
            return None
        
def check_payment_status(session_id):
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status
    except Exception as e:
        st.error(f"Error checking payment status: {str(e)}")
        return None
    
        

# validate_output(ticket_info)    
st.title("Ticket Checkout Page")

with st.form("payment_form"):
    # event_dates = st.text_input("Event dates",value=ticket_info.get('dates',""))
    event_loc = st.text_input("Race location",value=ticket_info.get('location',""))
    ticket_count = st.number_input("Ticket Count",step=1,value=ticket_info.get('count',0))
    total_amount = st.number_input("Total Amount (USD)", step=1,value=int(ticket_count * ticket_info.get('cost',0)))
    
    # Submit button
    submitted = st.form_submit_button("Confirm")
    if submitted:
        
            checkout_session = create_checkout_session(total_amount,ticket_count,currency='usd')
            if checkout_session:
                st.session_state.checkout_id = checkout_session.id
                st.write("Redirecting to payment...")
                st.link_button(label="Pay Now",url=checkout_session.url)
                
                
                if st.session_state.checkout_id:
                        # if st.button("Check Payment Status"):
                        status = check_payment_status(st.session_state.checkout_id)
                        if status:
                            st.session_state.payment_status = status
                            if status == "paid":
                                st.success("Payment successful! Thank you for your purchase.")
                            elif status == "unpaid":
                                st.warning("Payment pending. Please complete the payment.")
                            else:
                                st.info(f"Payment status: {status}")
                    
                
        