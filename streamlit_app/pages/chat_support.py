import streamlit as st
from openai import OpenAI
import mysql.connector
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch RDS credentials
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'bdia-finalproject-instance.chk4u4ukiif4.us-east-1.rds.amazonaws.com'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASSWORD', 'amazonrds7245'),
    'database': os.getenv('DB_NAME', 'bdia_team6_finalproject_db'),
    'port': os.getenv('RDS_PORT', '3306')
}

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class PaymentVerifier:
    def __init__(self, config):
        self.connection_config = config

    def get_connection(self):
        return mysql.connector.connect(**self.connection_config)

    def verify_active_payment(self, username):
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT * FROM ticket_info 
            WHERE username = %s 
            AND status = 'ACTIVE'
            """
            cursor.execute(query, (username,))
            payment = cursor.fetchone()
            cursor.close()
            connection.close()
            return payment
        except mysql.connector.Error as err:
            st.error(f"Database error: {err}")
            return None

    def cancel_subscription(self, customer_id):
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            update_query = """
            UPDATE ticket_info 
            SET status = 'CANCELLED', 
                TicketDate1 = NOW() 
            WHERE username = %s 
            AND status = 'ACTIVE'
            """
            cursor.execute(update_query, (customer_id,))
            connection.commit()
            is_cancelled = cursor.rowcount > 0
            cursor.close()
            connection.close()
            return is_cancelled
        except mysql.connector.Error as err:
            st.error(f"Database error: {err}")
            return False

def create_support_ticket(customer_id, request_type, description):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        ticket_id = str(uuid.uuid4())
        query = """
        INSERT INTO support_tickets 
        (ticket_id, customer_id, request_type, description, status, created_at) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            ticket_id,
            customer_id,
            request_type,
            description,
            'OPEN',
            datetime.now()
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return ticket_id
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return None

def detect_support_action(user_message):
    refund_keywords = ['refund', 'money back', 'return payment']
    cancel_keywords = ['cancel', 'terminate', 'end subscription']
    f1_keywords = ['History', 'rules', 'information', 'Book', 'Purchase', 'driver']
    for keyword in refund_keywords:
        if keyword in user_message.lower():
            return 'REFUND'
    for keyword in cancel_keywords:
        if keyword in user_message.lower():
            return 'CANCEL_SUBSCRIPTION'
    for keyword in f1_keywords:
        if keyword in user_message.lower():
            st.switch_page("pages/AI_assistant.py")
    return None

def get_openai_response(client, messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def main():
    st.title("🤖 AI Customer Support Bot")
    st.write("Your intelligent support assistant!")

    # Sidebar configuration
    with st.sidebar:
        st.header("Configuration")

        customer_id = st.session_state.get('username')

        if customer_id:
            st.info(f"Customer ID: {customer_id}")
        else:
            st.warning("Customer ID not set in session state")


        # Initialize clients
        client = None
        payment_verifier = None

        if OPENAI_API_KEY:
            # Initialize OpenAI client
            client = OpenAI(api_key=OPENAI_API_KEY)
            # Initialize Payment Verifier
            payment_verifier = PaymentVerifier(DB_CONFIG)
        else:
            st.warning("Please provide the OpenAI API Key")

    # Session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        support_action = detect_support_action(prompt)
        conversation = [
            {"role": "system", "content": "You are a helpful Formula 1 customer support assistant. Only answer questions related to Formula1 ticket cancel or payment else give error. Only call the cancel or payment tool whenever needed"},
            *st.session_state.messages
        ]

        with st.chat_message("assistant"):
            with st.spinner("Processing your request..."):
                if client and payment_verifier and customer_id:
                    response = get_openai_response(client, conversation)
                    if support_action == 'CANCEL_SUBSCRIPTION':
                        active_payment = payment_verifier.verify_active_payment(customer_id)
                        if active_payment:
                            cancellation_result = payment_verifier.cancel_subscription(customer_id)
                            response += "\n\n*Subscription successfully cancelled.*" if cancellation_result else "\n\n*Unable to cancel subscription. Please contact support.*"
                        else:
                            response += "\n\n*No active tickets found to cancel.*"
                    if support_action:
                        ticket_id = create_support_ticket(customer_id, support_action, prompt)
                        response += f"\n\n*Support ticket (#{ticket_id}) has been created.*"
                    if response:
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Please provide all required configurations")

if __name__ == "__main__":
    main()
