## **F1\_Intelligence: AI-Powered Formula 1 Service Platform**

### **Contributors**:

- Vishodhan Krishnan
- Vismay Devjee
- Sahiti Nallamolu

### **Project Resources**:

---

a. **Architecture Diagram**: [F1\_Architecture\_Diagram](https://github.com/user-attachments/assets/c0fdedcc-5723-4c3b-b5e1-7f2c5021be45)\
b. **CodeLabs Docuementation**: [Codelabs Preview]([https://codelabs-preview.appspot.com/?file_id=1t_GZmwSyKnDMAxhKAaY9cRZL4CEPNU9gTiNYkzEAi7o/#2](https://codelabs-preview.appspot.com/?file_id=1CUduezE76kCqx0TRpqaDo3Pl7KDuOFKQCUUVGRm7FnU#0))\
c. **Video Recording**: [Video Recording](https://northeastern.zoom.us/rec/share/teRm01lwb_YqW1MNqz4k4j1kjuFceopDvdC24ALmXLAkKH1e6bLjJCNYZ5iF5BNp.j0p14wd0cYALbO52)

### **Synopsis**

The **F1\_Intelligence** project aims to revolutionize the Formula 1 fan experience by integrating services like ticket booking, historical statistics, personalized news, and customer support into a single AI-powered platform. This unified interface uses agent-based architecture to streamline interactions, making it easier for fans to navigate the diverse and complex F1 ecosystem.

### **Technologies Used**

- **BeautifulSoup and Selenium**: To scrape relevant data from multiple websites.
- **Streamlit**: For the frontend user interface.
- **FastAPI**: To manage user authentication.
- **OpenAI API**: For race analysis and AI-enhanced customer services.
- **Amazon S3**: For unstructured data storage and management.
- **Amazon RDS**: For structured database solutions.
- **Agent-Based Architecture**: To coordinate interactions between multiple services seamlessly.

### **Problem Statement**

#### Objective:

To create an integrated and intuitive AI platform for Formula 1 enthusiasts, solving challenges such as:

- **Fragmentation**: Navigating multiple platforms for ticket booking and subscriptions.
- **Complexity**: Lack of centralized data and support services on existing platform.
- **User Experience**: Need of robust service for F1 history, race analysis and statistics.

#### Goals:

- Build a **unified platform** for accessing various F1 services.
- Implement **AI agents** to enhance user experience by automating ticket booking, customer support, and providing personalized assistance.
- Enable **real-time analysis, statistics and support** for fans and customers.

### **Desired Outcome**

The F1\_Intelligence platform will allow users to:

- **Book tickets**: For races with ease and convenience.
- **Access history of F1 and lap by lap analysis**: Historical and real-time data in an intuitive format.
- **Interact with AI agents**: For personalized customer support and service recommendations.

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
2. **F1 History Access**: Fans can explore real-time and historical race statistics using an intuitive interface.
3. **Customer Support**: AI-powered agents assist users with queries, troubleshooting, and personalized recommendations.
4. **Integration**: All services are unified in a single platform with centralized user data and preferences.

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

