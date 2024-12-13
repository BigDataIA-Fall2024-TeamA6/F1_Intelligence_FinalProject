## **F1\_Intelligence: AI-Powered Formula 1 Service Platform**

### **Contributors**:

- Vishodhan Krishnan
- Vismay Devjee
- Sahiti Nallamolu

### **Project Resources**:

---

a. **Architecture Diagram**: [F1\_Architecture\_Diagram](https://github.com/user-attachments/assets/c0fdedcc-5723-4c3b-b5e1-7f2c5021be45)\
b. **CodeLabs Docuementation**: [Codelabs Preview](https://codelabs-preview.appspot.com/?file_id=1CUduezE76kCqx0TRpqaDo3Pl7KDuOFKQCUUVGRm7FnU#0)\
c. **Video Recording**: [Video Recording](https://northeastern.zoom.us/rec/share/teRm01lwb_YqW1MNqz4k4j1kjuFceopDvdC24ALmXLAkKH1e6bLjJCNYZ5iF5BNp.j0p14wd0cYALbO52)

Here’s an elaboration of the **F1_Intelligence** project concept:

---

### **Synopsis**

The **F1_Intelligence** project aspires to redefine the Formula 1 fan experience by merging advanced AI capabilities with a seamless user interface. This comprehensive platform integrates ticket booking, historical insights, real-time statistics, personalized news feeds, lap-by-lap race analysis, and 24/7 customer support into a single, cohesive digital ecosystem. By leveraging an agent-based architecture, **F1_Intelligence** eliminates the need for fans to juggle multiple platforms, offering an efficient, engaging, and intuitive way to immerse themselves in the thrilling world of Formula 1.

---

### **Problem Statement**

#### **Objective:**

The Formula 1 fan journey today faces several hurdles that diminish the overall experience. Fans often have to rely on disparate platforms to meet their diverse needs—be it purchasing race tickets, exploring historical statistics, accessing real-time race data, or finding answers to their queries. The **F1_Intelligence** platform seeks to solve these challenges by offering a single, AI-driven solution to:

1. **Fragmentation**:
   - Fans must navigate multiple websites and apps for ticket bookings, news updates, and customer service inquiries. This scattered experience creates frustration and inefficiency.

2. **Complexity**:
   - Accessing accurate, centralized data for race analysis, historical comparisons, and detailed statistics is a cumbersome task due to the lack of unified platforms catering to such needs.

3. **User Experience**:
   - Existing solutions often fail to provide personalized, interactive services. Fans seek a tailored experience that aligns with their preferences, such as curated historical insights, lap-by-lap race details, and dynamic service recommendations.

---

#### **Goals:**

The **F1_Intelligence** project aims to:

1. **Leverage AI Agents**:
   - Introduce AI-powered agents to automate key processes, such as:
     - Simplified ticket booking.
     - Real-time customer support via conversational AI.
     - Personalized service recommendations based on user preferences and behavior.

2. **Provide Real-Time Data & Insights**:
   - Enable real-time race tracking, lap-by-lap analysis, and statistical insights, presented in an easily digestible format.

3. **Historical Knowledge Base**:
   - User would not have to scroll through multiple tables to get answers to their queries on historical events in F1. A chat assistant should be able to answer based on its knowledge base.

---

### **Desired Outcome**

With the **F1_Intelligence** platform, Formula 1 enthusiasts will gain access to a transformative digital experience that:

1. **Streamlines Ticket Booking**:
   - Fans can simply ask an AI assistant to book tickets for them and will need to make payment directly for races worldwide without navigating multiple platforms.
   - AI agents assist in finding the best ticket options based on user preferences and budget constraints.

2. **Offers Historical and Real-Time Data**:
   - Fans can explore comprehensive historical data, including driver and team performances, race highlights, and iconic moments in F1 history.
   - The platform delivers real-time lap-by-lap race analysis, integrating detailed telemetry, pit stop strategies, and live standings.

3. **Delivers Personalized News & Insights**:
   - AI-curated news feeds tailored to individual interests, such as updates on favorite drivers, teams, or upcoming races.

4. **Provides 24/7 AI-Driven Customer Support**:
   - Virtual agents answer queries on topics like ticket bookings, event schedules, and race-day logistics in real-time.
   - Support is also extended for troubleshooting technical issues and resolving ticket-related concerns.

---

### **Technologies Used**

- **BeautifulSoup and Selenium**: To scrape relevant data from multiple websites.
- **Streamlit**: For the frontend user interface.
- **FastAPI**: To manage user authentication.
- **OpenAI API**: For race analysis and AI-enhanced customer services.
- **Amazon S3**: For unstructured data storage and management.
- **Amazon RDS**: For structured database solutions.
- **Agent-Based Architecture**: To coordinate interactions between multiple services seamlessly.

### **File Structure**

```plaintext
F1_Intelligence_FinalProject/
  ├── utils/
  │   └── f1_history_jolpica.py
  │   └── f1_history_vectordb.py
  │   └── lap_analysis.py
  │   └── news.py
  │   └── page1_calendar.py
  │   └── page1_standings.py
  ├── architecture_diagram/
  │   └── arch_diagram.png
  ├── fastapi_backend/
  │   ├── api.py               # FastAPI backend for managing services
  ├── streamlit_app/
  │   ├── app.py              # Main Streamlit application
  │   ├── pages/
  │   ├── tests/
  │   ├── db.py
  │   ├── research_agent.py
  │   ├── state.py
  │   ├── tool.py
  ├── requirements.txt                 
  ├── docker-compose.yaml              
  └── README.md                   
```

### **How It Works**

1. **Ticket Booking**: Users can book tickets for F1 races directly through the platform.
2. **Lap-by-Lap Analysis**: Users can browse through previous races and get an overview of the entire race including major events, pitstops, scores, etc in a downloadable PDF format.
3. **F1 History Access**: Fans can explore current and historical race statistics using an intuitive interface.
4. **Customer Support**: AI-powered agents assist users with queries, troubleshooting, and personalized recommendations.
5. **Integration**: All services are unified in a single platform with centralized user data and preferences.

### **Architecture Diagram**

![F1_Architecture_Diagram](https://github.com/BigDataIA-Fall2024-TeamA6/F1_Intelligence_FinalProject/blob/main/architecture_diagram/F1_ArchDiag.jpeg)

### **Steps to Run this Application**

1. **Clone this repository** to your local machine:

   ```bash
   git clone https://github.com/BigDataIA-Fall2024-TeamA6.git
   ```

2. **Install dependencies** using Poetry:

   ```bash
   poetry install
   ```

3. **Add credentials** to a `.env` file in the root directory:

   - AWS Access Key
   - Pinecone Access Details
   - OpenAI API Key

4. **Run the applications**:

   - **fastapi**:

     ```bash
     docker-compose up --build
     ```

   - **Streamlit**:

     ```bash
     docker-compose up --build
     ```

5. **Explore the application**:

   - Use the interface to book tickets, view race statistics, and view lap-by-lap analysis.
   - Interact with AI agents for support and recommendations.

### **References**

1. [Streamlit Documentation](https://docs.streamlit.io/)
2. [FastAPI Documentation](https://fastapi.tiangolo.com/)

