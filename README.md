# AI-Candidate-Interview-Assistant-with-OpenAI-LLM-NLP-and-Redis
This project uses OpenAI's LLM and NLP to streamline recruitment by automating interviews, analyzing candidate responses and assessing culture fit. Using Redis for real-time data handling, ensuring efficient processing, seamless interactions, and intelligent decision-making. Designed to modernize hiring, it offers actionable insights for recruiters

---
### **Problem**  
1. Traditional interviews rely heavily on interviewer judgment, which can lead to unconscious bias and inconsistent evaluations of candidates.  
2. Screening resumes, conducting interviews, and evaluating candidates require substantial time and resources, especially for large-scale recruitment drives.  
3. Identifying candidates who align with a company’s unique culture and values is complex and often subjective.  
4. Manual recruitment processes struggle to handle large volumes of applications and interviews.  
5. Many organizations fail to leverage data-driven insights to improve decision making and optimize their hiring processes.  


### **Aim**  
To enhance the recruitment process by providing a scalable, intelligent, and unbiased system that reduces time-to-hire, improves candidate evaluation accuracy, and aligns hiring decisions with organizational goals and cultural values. This project aspires to redefine how companies approach hiring by making AI an integral part of recruitment strategy.


You're absolutely correct—there were 9 points in your description. I unintentionally combined some and missed maintaining the count explicitly. Let me correct that by ensuring all 9 points are distinctly addressed while keeping the descriptions concise and structured.

---

### **How It Works**

#### **1. Landing Page and Sign-In**
The system starts with a minimalist design approach:  
- **Landing Page**: Features a centered title and call-to-action with a "Get Started" button. Subtle design elements, such as scattered dots, enhance visual appeal without distraction.  
- **Sign-In Page**: Maintains a clean, consistent design with centrally aligned form fields and buttons. Ample white space ensures a user-friendly experience.
<img width="600" alt="image" src="https://github.com/user-attachments/assets/73af68d6-5910-4401-a66a-b45d38387561" />
<img width="600" alt="image" src="https://github.com/user-attachments/assets/5447d07a-41ba-41f6-a490-47a113f792d4" />


---

#### **2. Company Onboarding**
The onboarding process is intuitive and efficient:  
- A large input field allows companies to detail their mission clearly.  
- Navigation buttons ("Previous" and "Next") guide users through the steps, ensuring a seamless experience.  
- The consistent, modern design encourages engagement and ease of use.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/a80b1785-66b9-4e39-bc62-cdee24dcb139" />

---

#### **3. Company Profile Management**
The company profile page enables easy management of key details:  
- Sections like **Company Name, Mission, Vision, Values, and Working Environment** are editable and clearly presented.  
- Navigation buttons ("Cancel" and "Save") at the bottom simplify input management, while the layout prioritizes readability and navigation.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/143b60b6-e128-4a2b-974e-c9b186173cb3" />

---

#### **4. Company Attributes**
The Company Attributes page is organized into a structured grid layout:
- Attributes such as Agreeableness, Neuroticism, Conscientiousness, Openness to Experience, and Extraversion are displayed as cards.
- Each card provides a brief description, a score, and an explanation, enabling easy comparison and understanding.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/248625b0-15f9-469e-b51c-c6d44bba24d8" />

---

#### **5. Interview Creation**
Creating an interview is a straightforward two-step process:  
- **Step 1**: Upload a CV or enter details manually. The interface supports drag-and-drop functionality and clear buttons for file analysis or manual data entry.  
- **Step 2**: Fill in the candidate's information, including **Name, Email, Phone Number, Education,** and **Work Experience.** The organized layout ensures user comfort during this process.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/1dfcd703-469d-43d0-be7f-22dd8209f22d" />
<img width="600" alt="image" src="https://github.com/user-attachments/assets/4d616402-c931-427a-a687-3a2019467724" />

---

#### **6. Confirmation of Interview Scheduling**
Once a CV is uploaded or details are manually entered, the system confirms interview scheduling with a pop-up modal.  
- This confirmation step reassures users of successful interview creation.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/70254767-bd82-4f64-be76-73fc68846f63" />


---

#### **7. Interview Dashboard**
The dashboard offers a centralized view of scheduled interviews:  
- Users can monitor the **status** of interviews and manage them effectively from this interface.  

<img width="600" alt="image" src="https://github.com/user-attachments/assets/4587ec26-dca9-4b7c-8c21-608f5a0a68d7" />


---

#### **8. Interview Assessment**
The assessment module provides detailed insights into candidate performance:  
- It features a **Congruence Score**, displayed prominently as a percentage, helping recruiters evaluate culture fit at a glance.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/0cb1445e-92d7-4199-a27a-ca04499545c5" />

---

#### **9. Candidate Introduction**
Candidates are welcomed with a concise introduction screen:  
- Instructions for the interview process are clearly laid out, ensuring candidates are well-prepared.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/a4ee384f-dd22-4483-b0b6-c880468ce193" />

---

#### **10. Candidate Interview Session**
The interview session guides candidates through various stages:  
- Real-time feedback and visual cues enhance the experience.  
- Each screen is designed for clarity and simplicity, enabling candidates to focus on the interview process.

<img width="600" alt="image" src="https://github.com/user-attachments/assets/88eabc76-8412-4245-b0d6-3ec328e29221" />
<img width="600" alt="image" src="https://github.com/user-attachments/assets/b6e9abf9-7fab-41f0-922e-8e0123d8ed22" />
<img width="600" alt="image" src="https://github.com/user-attachments/assets/49a222d6-cfd2-4a01-98c9-15077157f6eb" />


---

### **Technical Details**
1. **Backend**:  
   - Built with **FastAPI** for efficient routing and API development.
   - Integration with **Redis** for fast, in-memory data retrieval and session management.

2. **AI Models**:  
   - **Speech-to-Text**: Utilizing tools like ElevenLabs for audio transcription.  
   - **Natural Language Processing (NLP)**: Large language models (e.g., OpenAI GPT) generate and analyze interview questions and responses.  
   - **Collaborative Filtering**: Calculates similarity scores between company and candidate embeddings to evaluate culture fit.

3. **Database**:  
   - Redis stores session data, embeddings, and interview details for low-latency access.
   - Structured ERD ensures clean management of candidate and company data.

4. **Deployment**:  
   - **Serverless Architecture**: Configured using AWS ECS and Fargate for scalable and cost-efficient operations.
   - **YAML** configuration for defining AWS resources and services.

5. **Dependencies**:  
   - Core libraries include TensorFlow (ML), FastAPI (backend), Redis (data management), and PyPDF2 (CV parsing).

6. **Frontend**:  
   - Designed with React for a responsive and intuitive user interface.
   - State management ensures a seamless user experience across various modules (e.g., onboarding, interview creation).

