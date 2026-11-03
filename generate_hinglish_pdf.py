"""
Script to generate a comprehensive, publication-quality Project Synopsis PDF in Hinglish
for Bharat Yatra: India Tourist Cities Travel Cost Calculator & AI Planner.
Includes dedicated Frontend vs Backend Architecture & Data Flow Breakdown.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically render total page numbers and running header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#52796F"))
        
        # Running header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, letter[1] - 36, "Bharat Yatra — Project Synopsis & Technical Architecture (Hinglish)")
            self.setStrokeColor(colors.HexColor("#D8E2DC"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
        # Running footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, footer_text)
        self.drawString(54, 32, "Confidential • Bharat Yatra Project Documentation")
        self.setStrokeColor(colors.HexColor("#D8E2DC"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)
        
        self.restoreState()


def build_hinglish_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Nature-toned Palette
    C_PRIMARY = colors.HexColor("#1B4332")      # Deep Forest Green
    C_SECONDARY = colors.HexColor("#2D6A4F")    # Sage Green
    C_ACCENT = colors.HexColor("#40916C")       # Mint / Grass Green
    C_BG_LIGHT = colors.HexColor("#F4F7F4")     # Soft Nature Tint
    C_BG_CARD = colors.HexColor("#EBF2EC")      # Slightly deeper card tint
    C_TEXT_DARK = colors.HexColor("#1F2421")     # Charcoal Text
    C_TEXT_MUTED = colors.HexColor("#52796F")    # Slate Green Text

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=C_PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=C_SECONDARY,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=C_PRIMARY,
        spaceBefore=11,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=C_SECONDARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=C_TEXT_DARK,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.5,
        textColor=C_TEXT_DARK,
        leftIndent=14,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=C_PRIMARY
    )

    code_block_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10,
        textColor=colors.HexColor("#0F3826"),
        backColor=colors.HexColor("#F0F4EF"),
        borderPadding=5,
        spaceAfter=6
    )

    qa_box_style = ParagraphStyle(
        'QABox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_TEXT_DARK,
        spaceAfter=4
    )

    story = []

    # ==================== COVER / HEADER BANNER ====================
    story.append(Paragraph("PROJECT SYNOPSIS & TECHNICAL SPECIFICATION (HINGLISH)", ParagraphStyle('SuperTitle', fontName='Helvetica-Bold', fontSize=8.5, textColor=C_ACCENT, leading=10, spaceAfter=4)))
    story.append(Paragraph("BHARAT YATRA", title_style))
    story.append(Paragraph("Smart Indian Tourist Cities Cost Calculator & AI Tour Planning Studio", subtitle_style))
    
    # Metadata Box
    meta_data = [
        [
            Paragraph("<b>Domain:</b> Domestic Indian Tourism & Budgeting", table_cell_style),
            Paragraph("<b>Stack:</b> Python / Streamlit / SQLite / Gemini AI", table_cell_style),
            Paragraph("<b>Deployment:</b> Docker / Render Cloud (Live)", table_cell_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 180, 154])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D1E2D2")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1E2D2")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceAfter=8))

    # ==================== SECTION 1: INTRODUCTION & PROBLEM STATEMENT ====================
    story.append(Paragraph("1. Project Overview & Problem Statement (Yeh Project Kyun Banaya?)", h1_style))
    story.append(Paragraph(
        "<b>Purana Background vs Naya Mission:</b> Yeh project originally ek US Government (GSA Per-Diem Rates & Chicago guidelines, USD $) travel cost calculator tha. Humne isko completely re-architect kiya aur specifically <b>Indian Domestic Tourism (INR Currency)</b> ke liye tailor-made banaya jisme pure India ke 45+ top tourist cities ka real dataset shaamil kiya gaya hai.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Real-World Problem:</b> Jab bhi koi Indian traveler apni family ya friends ke sath trip plan karta hai (jaise Goa, Manali, Jaipur, Kerala), toh use alag-alag websites par jaakar hotels, trains/flights, daily food aur local cabs ka andaza lagana padta hai. Is fragmented process ki wajah se budget hamesha exceed ho jata hai ya trip plan adhoora reh jata hai.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Bharat Yatra ka Solution:</b> Ek unified, modern web application jisme user ko single-click me complete itemized budget breakdown (Lodging, Food, Transit, Local commute, 10% Emergency buffer) milta hai, sath hi <b>Google Gemini 3.8 Flash AI</b> user ke personalized budget ke according day-wise itinerary generate karta hai.",
        body_style
    ))

    # ==================== SECTION 2: FRONTEND VS BACKEND DEEP DIVE ====================
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Frontend vs Backend Complete Architecture Breakdown", h1_style))
    story.append(Paragraph(
        "Project ka architecture do primary layers me cleanly separated hai: <b>Frontend (UI / UX Layer)</b> jo user interaction handle karta hai, aur <b>Backend (Business Logic, Security, Data & AI Layer)</b> jo computational aur storage operations manage karta hai.",
        body_style
    ))

    story.append(Paragraph("A. Frontend Layer (User Interface & Experience)", h2_style))
    story.append(Paragraph("• <b>UI Framework:</b> <b>Streamlit</b> (Python-based modern reactive web UI framework) jo without heavy JS setup ke clean, fast web interfaces render karta hai.", bullet_style))
    story.append(Paragraph("• <b>Custom Design System & Styling:</b> Streamlit me custom CSS injection ke zariye <b>Nature-Toned Modern Palette</b> create kiya gaya hai (Deep Forest Green <code>#1B4332</code>, Sage Green <code>#2D6A4F</code>, Mint <code>#52B788</code>, aur Warm Sand cards).", bullet_style))
    story.append(Paragraph("• <b>Core UI Screens:</b>", bullet_style))
    story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;1. <i>Authentication Portal:</i> Clean Login, Sign Up, aur Forgot Password OTP input forms.<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;2. <i>Cost Calculator Dashboard:</i> Dropdowns (Origin, Destination), Date Pickers, Number Inputs (Travelers, Nights), Budget Tier Radio Buttons.<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;3. <i>Visual KPI Cards:</i> Color-coded metric tiles showing Lodging, Food, Transit, Local Cab, Sightseeing, aur Emergency Buffer.<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;4. <i>AI Travel Studio Chat:</i> Interactive real-time chat interface (<code>st.chat_message</code>, <code>st.chat_input</code>) Copilot ke sath converse karne ke liye.<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;5. <i>Saved Trips Dashboard:</i> Past calculations ki list, detailed view, aur PDF download options.", body_style))
    story.append(Paragraph("• <b>Frontend Controller Files:</b> <code>app.py</code> (Main controller & dynamic page router) aur <code>.streamlit/config.toml</code> (Theme configuration).", bullet_style))

    story.append(Spacer(1, 3))
    story.append(Paragraph("B. Backend Layer (Logic, Security, Data & AI Intelligence)", h2_style))
    story.append(Paragraph("Backend screen ke peeche ka saara mathematical calculation, database persistence, cryptographic security aur AI intelligence run karta hai. Yeh 5 core modules me divided hai:", body_style))

    fe_be_table_data = [
        [Paragraph("Backend Module", table_header_style), Paragraph("Source File", table_header_style), Paragraph("Core Technology", table_header_style), Paragraph("Kaam / Responsibility in Project", table_header_style)],
        [
            Paragraph("Calculation Engine", table_cell_bold),
            Paragraph("src/travel_calculator.py", table_cell_style),
            Paragraph("Python Core Math", table_cell_style),
            Paragraph("Lodging, meals, intercity flights/trains, local cabs, aur 10% emergency buffer calculate karta hai. Indian numbering (Rs.) format karta hai.", table_cell_style)
        ],
        [
            Paragraph("Auth & Security", table_cell_bold),
            Paragraph("src/auth.py", table_cell_style),
            Paragraph("SQLite3 + hashlib", table_cell_style),
            Paragraph("Salted SHA-256 password hashing, user registration/login verify karna, aur 6-digit OTP generate/expire karna.", table_cell_style)
        ],
        [
            Paragraph("AI Agent Engine", table_cell_bold),
            Paragraph("src/ai_agent.py", table_cell_style),
            Paragraph("Google Gemini 3.8 Flash", table_cell_style),
            Paragraph("Gemini Cloud API ke sath communicate karta hai; trip context inject karke structured day-wise itinerary aur smart chat responses generate karta hai.", table_cell_style)
        ],
        [
            Paragraph("Email Dispatch", table_cell_bold),
            Paragraph("src/email_service.py", table_cell_style),
            Paragraph("Resend REST API", table_cell_style),
            Paragraph("Transactional email delivery handle karta hai; user ke verified inbox par instant 6-digit OTP deliver karta hai.", table_cell_style)
        ],
        [
            Paragraph("Data Processing", table_cell_bold),
            Paragraph("src/data.py + CSVs", table_cell_style),
            Paragraph("Pandas Library", table_cell_style),
            Paragraph("45+ Indian cities ke hotel rates, local transport rates aur ground distances ko query aur index karta hai.", table_cell_style)
        ]
    ]

    t_fe_be = Table(fe_be_table_data, colWidths=[90, 115, 95, 204])
    t_fe_be.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1E2D2")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT]),
    ]))
    story.append(t_fe_be)

    story.append(Spacer(1, 4))
    story.append(Paragraph("C. Frontend aur Backend Aapas Mein Connect Kaise Hote Hain? (Data Flow)", h2_style))
    story.append(Paragraph("1. <b>Reactive Event Triggering:</b> Jab user frontend screen (<code>app.py</code>) par koi button click karta hai (e.g. <i>Calculate Costs</i> ya <i>Login</i>), Streamlit synchronous function calls ke zariye backend module (<code>src/</code>) ko execute karta hai.", bullet_style))
    story.append(Paragraph("2. <b>Session State Persistence:</b> User ka login token, active trip metadata aur AI chat history memory me <code>st.session_state</code> ke zariye maintain rehti hai.", bullet_style))
    story.append(Paragraph("3. <b>Database & External API Sync:</b> Backend functions SQLite database se credentials/trips fetch karte hain aur external APIs (Google Gemini & Resend) se data process karke wapas frontend screen par dynamically render kar dete hain.", bullet_style))

    # ==================== SECTION 3: TECHNOLOGY STACK ====================
    story.append(PageBreak())
    story.append(Paragraph("3. Technology Stack Specification (Kaunsi Technology Kyun Use Hui?)", h1_style))
    story.append(Paragraph("Project me use kiye gaye sabhi major technologies, libraries aur unka specific role neeche table me detailed hai:", body_style))

    tech_table_data = [
        [Paragraph("Component", table_header_style), Paragraph("Technology Used", table_header_style), Paragraph("Version", table_header_style), Paragraph("Role & Significance in Project", table_header_style)],
        [Paragraph("Web Framework", table_cell_bold), Paragraph("Streamlit", table_cell_style), Paragraph("1.65.0+", table_cell_style), Paragraph("Rapid reactive web UI, multi-page routing, state management", table_cell_style)],
        [Paragraph("Language", table_cell_bold), Paragraph("Python", table_cell_style), Paragraph("3.11 / 3.14", table_cell_style), Paragraph("Core backend logic, data transformation, algorithms", table_cell_style)],
        [Paragraph("Data Manipulation", table_cell_bold), Paragraph("Pandas", table_cell_style), Paragraph("3.0.6+", table_cell_style), Paragraph("CSV parsing, travel rates aggregation, distance indexing", table_cell_style)],
        [Paragraph("Generative AI", table_cell_bold), Paragraph("Google GenAI SDK (Gemini 3.8 Flash)", table_cell_style), Paragraph("2.21.0+", table_cell_style), Paragraph("High-speed AI itinerary generation & dynamic copilot chat", table_cell_style)],
        [Paragraph("Email Dispatch", table_cell_bold), Paragraph("Resend REST API", table_cell_style), Paragraph("2.36.0+", table_cell_style), Paragraph("Transactional email delivery for 6-digit password reset OTP", table_cell_style)],
        [Paragraph("Database", table_cell_bold), Paragraph("SQLite3", table_cell_style), Paragraph("Built-in", table_cell_style), Paragraph("Zero-config relational database for users, OTPs, and saved trips", table_cell_style)],
        [Paragraph("Cryptography", table_cell_bold), Paragraph("Python hashlib", table_cell_style), Paragraph("Standard Lib", table_cell_style), Paragraph("Salted SHA-256 password hashing for robust user security", table_cell_style)],
        [Paragraph("Testing Suite", table_cell_bold), Paragraph("Pytest", table_cell_style), Paragraph("9.1.1+", table_cell_style), Paragraph("9 automated test cases covering math, validation, and currency", table_cell_style)],
        [Paragraph("Containerization", table_cell_bold), Paragraph("Docker", table_cell_style), Paragraph("Latest", table_cell_style), Paragraph("Containerized image with dynamic $PORT binding for Render", table_cell_style)],
        [Paragraph("Cloud Hosting", table_cell_bold), Paragraph("Render.com", table_cell_style), Paragraph("Cloud PaaS", table_cell_style), Paragraph("Automated GitHub CI/CD web service with secret env variables", table_cell_style)]
    ]

    t_tech = Table(tech_table_data, colWidths=[90, 115, 55, 244])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1E2D2")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT]),
    ]))
    story.append(t_tech)

    # ==================== SECTION 4: MATHEMATICAL ALGORITHMS ====================
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Mathematical Budgeting Algorithm (Kharcha Calculate Karne Ka Formula)", h1_style))
    story.append(Paragraph(
        "Cost Calculation Engine transparent, deterministic aur mathematically verifiable formulas par operate karta hai:",
        body_style
    ))

    math_box = [
        [Paragraph("<b>Step 1: Per Person Cost Formula</b><br/>"
                   "<code>Cost_Per_Pax = (Lodging_Rate * Nights / Pax_Per_Room) + (Daily_Food_Rate * Days) + Intercity_Transit + (Local_Transit_Rate * Days) + Sightseeing_Fees</code><br/><br/>"
                   "<b>Step 2: Total Group Subtotal</b><br/>"
                   "<code>Group_Subtotal = Cost_Per_Pax * Number_Of_Travelers</code><br/><br/>"
                   "<b>Step 3: 10% Emergency Buffer & Final Budget</b><br/>"
                   "<code>Emergency_Buffer = Group_Subtotal * 0.10</code><br/>"
                   "<code>Total_Trip_Cost = Group_Subtotal + Emergency_Buffer</code>", code_block_style)]
    ]
    t_math = Table(math_box, colWidths=[504])
    t_math.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A3C4BC")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_math)

    # ==================== SECTION 5: DATABASE SCHEMA ====================
    story.append(Spacer(1, 6))
    story.append(Paragraph("5. Database Architecture & Relational Schema (SQLite3)", h1_style))
    story.append(Paragraph("Application me 3 core relational tables hain jo complete user lifecycle aur trip history manage karte hain:", body_style))

    schema_data = [
        [Paragraph("Table Name", table_header_style), Paragraph("Fields / Columns", table_header_style), Paragraph("Constraints & Security Purpose", table_header_style)],
        [
            Paragraph("<b>users</b>", table_cell_bold),
            Paragraph("id (INT PK), username (TEXT), email (TEXT UNIQUE), password_hash (TEXT), created_at (DATETIME)", table_cell_style),
            Paragraph("User identification; passwords stored as salt$sha256_hash", table_cell_style)
        ],
        [
            Paragraph("<b>otps</b>", table_cell_bold),
            Paragraph("id (INT PK), email (TEXT), otp_code (TEXT), expires_at (REAL), is_used (INT)", table_cell_style),
            Paragraph("Forgot password verification; 10 min expiry, invalidated upon use", table_cell_style)
        ],
        [
            Paragraph("<b>saved_trips</b>", table_cell_bold),
            Paragraph("id (INT PK), user_email (TEXT), origin (TEXT), destination (TEXT), days (INT), travelers (INT), tier (TEXT), total_cost (REAL), itinerary (TEXT), created_at (DATETIME)", table_cell_style),
            Paragraph("Persistent storage for user's past calculations and AI itineraries", table_cell_style)
        ]
    ]

    t_schema = Table(schema_data, colWidths=[80, 240, 184])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1E2D2")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT]),
    ]))
    story.append(t_schema)

    # ==================== SECTION 6: CODEBASE & ARCHITECTURE ====================
    story.append(PageBreak())
    story.append(Paragraph("6. Project Directory & Architecture Breakdown", h1_style))
    story.append(Paragraph("Project structure modular aur clean architecture follow karta hai, jisme concerns cleanly separated hain:", body_style))

    code_tree = """travel_cost_calculator/
|-- app.py                     # Frontend controller & multi-page navigation router
|-- requirements.txt           # Python dependencies (streamlit, google-genai, resend, etc.)
|-- Dockerfile                 # Container setup with dynamic $PORT binding for Render
|-- .env                       # API keys (GEMINI_API_KEY, RESEND_API_KEY)
|-- Bharat_Yatra_Synopsis.pdf  # Project formal synopsis in PDF format
|-- generate_pdf.py            # Automated ReportLab PDF generator script
|-- src/                       # Backend Source Code Modules
|   |-- auth.py                # User login, signup, SHA-256 hashing & SQLite queries
|   |-- email_service.py       # Resend REST API integration for email OTP delivery
|   |-- ai_agent.py            # Gemini 3.8 Flash prompt engineering & dynamic copilot
|   |-- travel_calculator.py   # Core math calculation engine & INR currency formatter
|   `-- data.py                # Fallback city master data & transport matrices
|-- data/                      # Backend Dataset Files
|   |-- cities_india.csv       # 45+ cities tier, hotel rates, and daily living costs
|   `-- ground_transport_rates.csv # Local transport matrices across Indian cities
`-- tests/                     # Automated Test Suites
    `-- test_calculator.py     # 9 Pytest test cases (currency, math, validation)"""

    story.append(Paragraph(code_tree.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_block_style))

    # ==================== SECTION 7: DEPLOYMENT & DEVOPS ====================
    story.append(Paragraph("7. Cloud Deployment & DevOps Lifecycle (Render & GitHub)", h1_style))
    story.append(Paragraph(
        "Application ko continuous cloud deployment pipeline ke zariye live kiya gaya hai:",
        body_style
    ))
    story.append(Paragraph("• <b>GitHub Repository:</b> Complete source code <code>https://github.com/ShaikhVaiz/travel_cost_calculator.git</code> par version controlled hai.", bullet_style))
    story.append(Paragraph("• <b>Dynamic Port Binding:</b> Render jaise cloud platforms par dynamic port allot hota hai. Dockerfile me hardcoded port ke bajaye <code>--server.port=${PORT:-8501}</code> configure kiya gaya hai.", bullet_style))
    story.append(Paragraph("• <b>Secrets Management:</b> Gemini API Key aur Resend API Key ko code me hardcode karne ke bajaye Render ke Environment Variables dashboard me securely inject kiya gaya hai.", bullet_style))
    story.append(Paragraph("• <b>Zero-Downtime Builds:</b> Jab bhi GitHub par naya commit push hota hai, Render automatically Docker image rebuild karke bina kisi downtime ke deployment live kar deta hai.", bullet_style))

    # ==================== SECTION 8: VIVA & INTERVIEW PREPARATION GUIDE ====================
    story.append(Spacer(1, 6))
    story.append(Paragraph("8. Viva & Interview Questions Guide (Hinglish Q&A)", h1_style))
    story.append(Paragraph("Examiners aur interviewers dwara puche jane wale top questions aur unke crisp answers:", body_style))

    qa_list = [
        ("Q1: Is project ka Frontend aur Backend alag kaise hai?", 
         "Ans: Frontend Streamlit aur custom CSS par based hai jo interactive UI, forms aur AI chat render karta hai. Backend Python modules par bana hai: calculation ke liye travel_calculator.py, SQLite database aur SHA-256 hashing ke liye auth.py, email OTP ke liye Resend API, aur AI generation ke liye Google Gemini 3.8 Flash."),
        ("Q2: Passwords ko database me kaise protect kiya gaya hai?", 
         "Ans: Plain text passwords bilkul store nahi hote. Har user ke liye unique cryptographic salt generate hota hai aur SHA-256 algorithm se hash karke SQLite me store kiya jata hai."),
        ("Q3: Forgot Password me OTP kaise dispatch hota hai?", 
         "Ans: Resend REST API SDK ke zariye user ke email par instant 6-digit verification code jata hai. Is code ki validity SQLite me 10 minute tak rehti hai aur ek baar verify hone par ye expire ho jata hai."),
        ("Q4: Gemini 3.8 Flash model kyun use kiya gaya?", 
         "Ans: Gemini 3.8 Flash ultra-fast inference speed deta hai jisse user ko bina kisi delay ke instant structured itinerary aur dynamic answers mil jate hain."),
        ("Q5: Render cloud deployment me kya challenge aaya tha?", 
         "Ans: Cloud platforms fixed port 8501 allow nahi karte. Humne Docker entrypoint me dynamic shell expansion ${PORT:-8501} use karke container ko dynamic port-aware banaya.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, qa_box_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Hinglish PDF with Frontend/Backend successfully generated: {filename}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(current_dir, "Bharat_Yatra_Project_Synopsis_Hinglish.pdf")
    build_hinglish_pdf(output_pdf)
