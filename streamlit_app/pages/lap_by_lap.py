import streamlit as st
import boto3
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Load environment variables
load_dotenv()

# Initialize OpenAI and S3 Clients
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
s3 = boto3.client('s3')
S3_BUCKET_NAME= "f1-historical-data"
S3_BUCKET_NAME_LAP="f1-lap-analysis-data"

# Predefined Grand Prix list
grand_prix_list = [
    "Bahrain", "Saudi Arabian", "Australian", "Japanese", "Chinese",
    "Miami", "Emilia Romagna", "Monaco", "Canadian", "Spanish",
    "Austrian", "British", "Hungarian", "Belgian", "Dutch",
    "Italian", "Azerbaijan", "Singapore",
    "United States", "Mexico City", "São Paulo",
    "Las Vegas", "Qatar", "Abu Dhabi", "Brazilian"
]

# Streamlit Page Configuration
st.set_page_config(
    page_title="F1 Lap Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Dark theme */
    .main {
        color: black;
    }

    /* Header styling */
    .title {
        color: black;
        padding: 1rem 0;
    }

    /* Dropdown styling */
    .stSelectbox > div > div {
        background-color: white;
        color: black;
        border: 1px solid red;
    }

    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: #FF1801;
        color: black;
        border: none;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }

    .stButton > button:hover {
        background-color: #D10000;
        color: #000000
    }

    /* Container styling */
    .visualization-container {
        border: 1px solid #FF1801;
        border-radius: 10px;
        padding: 20px;
    }

    /* Summary text styling */
    .summary-text {
        white-space: pre-wrap;
        word-wrap: break-word;
        font-size: 16px;
        line-height: 1.2;
        overflow-y: auto;
        max-height: 400px;
        padding: -10px;
    }

    /* Loading spinner */
    .loading {
        text-align: center;
        color: #FF1801;
        font-size: 18px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Fetch race data from S3
@st.cache_data
def fetch_race_data():
    try:
        response = s3.get_object(
            Bucket=S3_BUCKET_NAME_LAP,
            Key='race_data.json'
        )
        return json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        st.error(f"Error fetching race data: {e}")
        return {}

# Format summary for consistent output
def format_summary(summary):
    formatted_summary = []
    
    # Add key highlights
    formatted_summary.append("### Key Highlights of the Race")
    formatted_summary.append("")
    for line in summary.split("\n"):
        if any(keyword in line.lower() for keyword in ["crash", "flag", "pit"]):
            formatted_summary.append(f"- {line.strip()}")

    formatted_summary.append("")
    formatted_summary.append("### Detailed Lap-by-Lap Analysis")
    formatted_summary.append(summary)

    return "\n".join(formatted_summary)

# Prepare analysis prompt
def prepare_prompt(data):
    """
    Prepares a prompt for race analysis based on key events in the data.
    Filters comments with specific keywords and structures them into a prompt.
    """
    events = [
        f"- {entry['time']}: {entry['comment']}"
        for entry in data if "comment" in entry and any(
            keyword in entry["comment"].lower() for keyword in ["pit", "flag", "crash", "wins"]
        )
    ]
    if not events:
        return None

    return (
        "Portion of commentary from the race is provided, provide elaborate lap-wise analysis of the race.\n"
        + "\n".join(events)
        + "\nHighlight major events in the race like crashes, flags, and pit stops. Do not mention timestamps. "
        + "Provide the summary in a structured style. Use your knowledge base to expand on the race details."
    )


# Generate analysis summary
def generate_summary(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {e}"

# Create PDF from the race summary
def create_pdf(race_summary, selected_year, selected_gp):
    """
    Create a PDF file from the race summary with formatted styling
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Get existing styles
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = styles['Heading1'].clone('TitleStyle')
    title_style.fontSize = 16
    title_style.alignment = TA_CENTER
    
    heading_style = styles['Heading2'].clone('HeadingStyle')
    heading_style.fontSize = 14
    
    bold_style = styles['Normal'].clone('BoldStyle')
    bold_style.fontName = 'Helvetica-Bold'
    
    normal_style = styles['Normal'].clone('NormalStyle')
    
    bullet_style = styles['Normal'].clone('BulletStyle')
    bullet_style.leftIndent = 20
    
    # Prepare content
    content = []
    
    # Add title
    content.append(Paragraph(f"F1 Lap Analysis - {selected_gp} Grand Prix {selected_year}", title_style))
    content.append(Spacer(1, 12))
    
    # Process markdown-like formatting
    lines = race_summary.split('\n')
    for line in lines:
        # Handle headers
        if line.startswith('###'):
            content.append(Paragraph(line.replace('### ', ''), heading_style))
            content.append(Spacer(1, 6))
        
        # Handle bold text
        elif '**' in line:
            # Replace bold markers
            line = line.replace('**', '')
            content.append(Paragraph(line, bold_style))
            content.append(Spacer(1, 6))
        
        # Handle bullet points
        elif line.startswith('- '):
            # Remove bullet marker and process
            bullet_text = line.replace('- ', '')
            # Check for nested or bold bullets
            if '**' in bullet_text:
                bullet_text = bullet_text.replace('**', '')
                content.append(Paragraph(bullet_text, bullet_style))
            else:
                content.append(Paragraph(bullet_text, bullet_style))
            content.append(Spacer(1, 6))
        
        # Regular text
        elif line.strip():
            content.append(Paragraph(line, normal_style))
            content.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(content)
    
    return buffer




# Main logic
race_data = fetch_race_data()

if 'race_summary' not in st.session_state:
    st.session_state['race_summary'] = 'Lap Analysis Will Appear Here'
if 'analysis_in_progress' not in st.session_state:
    st.session_state['analysis_in_progress'] = False

col1, col2 = st.columns([1, 3])

with col1:
    col_home, col_spacer = st.columns([1, 2])
    with col_home:
        if st.button(" Home "):
            st.switch_page("pages/user_landing.py")

    st.markdown("## Lap by Lap Analysis")
    st.markdown("Select Grand Prix to analyse: ")

    years = list(range(2024, 2020, -1))
    selected_year = st.selectbox("Select Year", years, key="year")
    selected_country = st.selectbox("Select Country", grand_prix_list, key="country")

    if st.button("Generate Analysis"):
        st.session_state['race_summary'] = 'Generating analysis...'
        st.session_state['analysis_in_progress'] = True

        selected_race = next(
            (info['race'] for title, info in race_data.items()
             if selected_country.lower() in title.lower()
             and selected_year == datetime.fromisoformat(info['race'][0]['time'].replace('Z', '+00:00')).year),
            None
        )

        if selected_race:
            prompt = prepare_prompt(selected_race)
            if prompt:
                summary = generate_summary(prompt)
                st.session_state['race_summary'] = format_summary(summary)
            else:
                st.session_state['race_summary'] = "No significant events found for analysis."
        else:
            st.session_state['race_summary'] = "No matching race data found for the selected year and country."

        st.session_state['analysis_in_progress'] = False
        st.rerun()

    if st.button("Download Results"):
        pdf_buffer = create_pdf(st.session_state['race_summary'], selected_year, selected_country)
        st.download_button(
            label="Download Analysis as PDF",
            data=pdf_buffer,
            file_name=f"{selected_country}_GP_{selected_year}_Analysis.pdf",
            mime="application/pdf"
        )

with col2:
    st.markdown("## Analysis")
    if st.session_state['analysis_in_progress']:
        st.markdown("""
            <div class='loading'>
                Generating Analysis... Please wait
                <br>
                <span style='font-size: 14px;'>This may take up to 30 seconds</span>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='
                border: 2px solid #E10600;
                border-radius: 10px;
                padding: 20px;
                min-height: 400px;
                overflow-y: auto;
            '>
                <div class='summary-text'>
                    {st.session_state['race_summary'].replace('\n', '<br>')}
                </div>
            </div>
        """, unsafe_allow_html=True)