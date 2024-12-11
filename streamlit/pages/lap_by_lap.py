import streamlit as st
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.units import inch
import re
 
# Set page config
st.set_page_config(
    page_title="F1 Lap Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)
 
# Custom CSS for dark theme and proper styling
st.markdown("""
    <style>
    /* Dark theme */
    .main {
        color: white;
    }
    
    /* Header styling */
    .title {
        color: white;
        padding: 1rem 0;
    }
    
    /* Dropdown styling */
    .stSelectbox > div > div {
        background-color: #2D2D2D;
        color: white;
        border: 1px solid #9146FF;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: #FF1801;
        color: white;
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
    </style>
""", unsafe_allow_html=True)
 
# Race summary text
race_summary = """
### Race Summary: Belgian Grand Prix
 
**Race Overview:**
The Belgian Grand Prix unfolded with strategic pit stops and a strong performance from Red Bull, as they continued their dominant streak in the 2023 season. Max Verstappen secured his eighth consecutive victory, increasing his lead in the driver standings to a formidable 130 points. His win, paired with Sergio Perez's second-place finish, marked Red Bull's first 1-2 finish in a Grand Prix since Miami earlier in the season.
 
**Lap-by-Lap Analysis:**
 
- **Early Stage:** The race began with drivers focusing on preserving their medium compound tires. The initial laps saw stable positions among the top contenders, with Verstappen maintaining his lead after starting from the grid drop.
 
- **Mid-Race Developments:**
    - Lewis Hamilton, seeking to maximize performance, executed a pit stop to switch from medium to soft tires. This strategic move initially placed him behind Fernando Alonso, though he soon overtook Alonso at La Source.
    - Ferrari responded to Hamilton's pit stop by bringing in Charles Leclerc, who also switched to soft tires and re-emerged ahead of Hamilton.
    - Sergio Perez made a second pit stop to switch from mediums to softs, strategically benefiting from the timing as those behind him had just pitted, allowing him to maintain his position.
    - Fernando Alonso, after building a sufficient gap, pitted for his stop, managing to retain a significant position without losing places.
 
- **Key Race Incidents:**
    - Alexander Albon decided to pit for the final time in the race, exiting a battle he was involved in.
    - Logan Sargeant received a black-and-white flag for track limits violations, with a warning of a potential time penalty pending further infringements. However, no major on-track collisions or safety car deployments were noted during this period, indicating a relatively incident-free race.
 
- **Final Stage and Closing Laps:**
    - Verstappen came in for a routine pit stop, opting for soft tires while maintaining a comfortable lead over the field.
    - Hamilton, in pursuit of the fastest lap bonus point, decided to make an additional pit stop late in the race, reverting to medium tires.
    - Despite concerns over tire degradation, Verstappen's pace remained undeterred, showing strong communication and strategy management with his race engineer, Gianpiero Lambiase.
 
**Conclusion:**
The Belgian GP highlighted Red Bull's continuous dominance, with Verstappen showcasing not just speed but strategic brilliance. His win extends his championship lead, underscoring Red Bull's reliability and performance throughout the season. The race's outcome was a testament to Red Bull's strategic planning, pit stop efficiency, and Verstappen's consistent driving prowess, setting a high bar entering the summer break.
 
The strategic plays, especially around tire management and pit operations, influenced the race's dynamic significantly, allowing for positional shifts that were well-executed by top teams, particularly Red Bull and their championship leader, Verstappen.
"""
 
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
 
# Create two columns with proper ratio
col1, col2 = st.columns([1, 3])
 
with col1:
    col_home, col_spacer= st.columns([1, 2])
    with col_home:
        if st.button(" Home "):
            st.switch_page("pages/user_landing.py")
 
    st.markdown("## Lap by Lap Analysis")
    st.markdown("Select Grand Prix to analyse: ")
 
    # Year dropdown
    years = list(range(2024, 2020, -1))
    selected_year = st.selectbox("Select Year", years, key="year")
    
    # Grand Prix dropdown
    grand_prix_list = [
        "Bahrain", "Saudi Arabian", "Australian", "Japanese", "Chinese",
        "Miami", "Emilia Romagna", "Monaco", "Canadian", "Spanish",
        "Austrian", "British", "Hungarian", "Belgian", "Dutch",
        "Italian", "Azerbaijan", "Singapore", 
        "United States (Austin)", "Mexico City", "São Paulo",
        "Las Vegas", "Qatar", "Abu Dhabi"
    ]
    selected_gp = st.selectbox("Select Grand Prix", grand_prix_list, key="gp")
    
    # Action buttons
    if st.button("Generate Analysis"):
        st.session_state.generate_clicked = True
    
    if st.button("Download Results"):
        pdf_buffer = create_pdf(race_summary, selected_year, selected_gp)
        st.download_button(
            label="Click to Download PDF",
            data=pdf_buffer.getvalue(),
            file_name=f"{selected_gp}_GP_{selected_year}_Analysis.pdf",
            mime="application/pdf"
        )
 
with col2:
    st.markdown("## Analysis")
    
    if 'generate_clicked' in st.session_state and st.session_state.generate_clicked:
        st.markdown(race_summary)
    else:
        st.markdown("""
            <div style='
                border: 2px solid #E10600;
                border-radius: 10px;
                padding: 20px;
                min-height: 400px;
                display: flex;
                justify-content: center;
                align-items: center;
            '>
                <h3>Lap Analysis Visualization Will Appear Here</h3>
            </div>
        """, unsafe_allow_html=True)
 