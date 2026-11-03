"""
Script to generate a comprehensive, publication-quality Project Synopsis PDF in Hinglish
for Bharat Yatra: India Tourist Cities Travel Cost Calculator & AI Planner.
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
            self.drawString(54, letter[1] - 36, "Bharat Yatra — Project Synopsis (Hinglish Guide & Architecture)")
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
        spaceBefore=12,
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
        spaceBefore=8,
        spaceAfter=4,
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

    # ==================== SECTION 2: KEY MODULES & CAPABILITIES ====================
    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Core Modules & Key Features (Project ke Main Features)", h1_style))

    story.append(Paragraph("A. User Authentication & Password Security (SQLite + SHA-256 + Resend OTP)", h2_style))
    story.append(Paragraph("• <b>User Registration & Login:</b> Har user apna secure account create kar sakta hai. Passwords ko plain-text me store nahi kiya jata; Python <code>hashlib</code> ke through unique random salt aur SHA-256 cryptographic hashing use hoti hai.", bullet_style))
    story.append(Paragraph("• <b>Forgot Password via Email OTP:</b> Agar user password bhool jata hai, toh <b>Resend REST API</b> ke zariye user ke verified email par 6-digit dynamic OTP bheja jata hai. SQLite me 10-minute expiry window aur single-use verification logic implement kiya gaya hai.", bullet_style))

    story.append(Paragraph("B. Smart Travel Cost Calculator Engine (INR Currency)", h2_style))
    story.append(Paragraph("• <b>45+ Indian Destinations:</b> North, South, East, West aur North-East ke sabhi prominent tourist hubs (Jaipur, Varanasi, Udaipur, Shimla, Manali, Goa, Munnar, Ooty, Gangtok, Ladakh, etc.) covered hain.", bullet_style))
    story.append(Paragraph("• <b>Multi-Tier Travel Styles:</b> <i>Budget</i> (Hostels/Dhabas), <i>Standard</i> (3-star hotels/popular restaurants/AC cabs), aur <i>Luxury</i> (4/5-star resorts/fine dining/private cabs) me customized calculation hoti hai.", bullet_style))
    story.append(Paragraph("• <b>Itemized Expense Categorization:</b> Hotel Stay, Food Preferences (North/South Indian, Street Food, Cafe Culture), Inter-City Transit (Flight, Rajdhani/Express Train, Volvo Bus), Local City Commute (Auto, Metro, Full-day Cab), Sightseeing & Entry fees, aur 10% Emergency Safety Buffer.", bullet_style))
    story.append(Paragraph("• <b>Indian Numbering System:</b> Amounts ko standard Indian format (e.g., Rs. 1,45,200) me cleanly display kiya jata hai.", bullet_style))

    story.append(Paragraph("C. AI Travel Studio & Dynamic Copilot (Google Gemini 3.8 Flash)", h2_style))
    story.append(Paragraph("• <b>Customized Day-Wise Itinerary:</b> Destination, days, budget tier aur travel mode ko parse karke Gemini 3.8 Flash structured Morning-Afternoon-Evening plan generate karta hai.", bullet_style))
    story.append(Paragraph("• <b>Dynamic Contextual Copilot:</b> Static jawab dene ke bajaye, AI user ki current trip ke exact context (Origin, Destination, Days, Budget) ko dhyan me rakh kar real-time chat replies deta hai.", bullet_style))
    story.append(Paragraph("• <b>Packing List & Safety Guidelines:</b> Destination ke season aur terrain ke mutabiq packing essentials aur emergency precautions automatically provide karta hai.", bullet_style))

    story.append(Paragraph("D. Saved Trips & History Dashboard", h2_style))
    story.append(Paragraph("• Users apne generated budgets aur AI itineraries ko apne profile me Save kar sakte hain aur future me kabhi bhi review ya export kar sakte hain.", bullet_style))

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
|-- app.py                     # Main application entry point & page navigation router
|-- requirements.txt           # Python dependencies (streamlit, google-genai, resend, etc.)
|-- Dockerfile                 # Container setup with dynamic $PORT binding for Render
|-- .env                       # API keys (GEMINI_API_KEY, RESEND_API_KEY)
|-- Bharat_Yatra_Synopsis.pdf  # Project formal synopsis in PDF format
|-- generate_pdf.py            # Automated ReportLab PDF generator script
|-- src/                       # Backend Source Code
|   |-- auth.py                # User login, signup, SHA-256 hashing & SQLite queries
|   |-- email_service.py       # Resend REST API integration for email OTP delivery
|   |-- ai_agent.py            # Gemini 3.8 Flash prompt engineering & dynamic copilot
|   |-- travel_calculator.py   # Core math calculation engine & INR currency formatter
|   `-- data.py                # Fallback city master data & transport matrices
|-- data/                      # Dataset Files
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

    qa_box_style = ParagraphStyle(
        'QABox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_TEXT_DARK
    )

    qa_list = [
        ("Q1: Is project ka core purpose kya hai?", 
         "Ans: Ye ek intelligent Indian tourism budget calculator aur AI trip planner hai. User ko ek single screen par realistic travel expenses (hotels, food, transit, cabs) milte hain aur Gemini 3.8 Flash personalized day-wise plan provide karta hai."),
        ("Q2: Passwords ko database me kaise protect kiya gaya hai?", 
         "Ans: Plain text passwords bilkul store nahi hote. Har user ke liye unique cryptographic salt generate hota hai aur SHA-256 algorithm se hash karke SQLite me store kiya jata hai."),
        ("Q3: Forgot Password me OTP kaise dispatch hota hai?", 
         "Ans: Resend REST API SDK ke zariye user ke email par instant 6-digit verification code jata hai. Is code ki validity SQLite me 10 minute tak rehti hai aur ek baar verify hone par ye expire ho jata hai."),
        ("Q4: Gemini 3.8 Flash model kyun use kiya gaya?", 
         "Ans: Gemini 3.8 Flash ultra-fast inference speed deta hai jisse user ko bina kisi delay ke instant structured itinerary aur dynamic answers mil jate hain."),
        ("Q5: Render cloud deployment me kya challenge aaya tha?", 
         "Ans: Cloud platforms fixed port 8501 allow nahi karte. Humne Docker entrypoint me dynamic shell expansion `${PORT:-8501}` use karke container ko dynamic port-aware banaya.")
    ]

    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, qa_box_style))
        story.append(Spacer(1, 2))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Hinglish PDF successfully generated: {filename}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(current_dir, "Bharat_Yatra_Project_Synopsis_Hinglish.pdf")
    build_hinglish_pdf(output_pdf)
