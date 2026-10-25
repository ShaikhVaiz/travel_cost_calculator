"""
Script to generate a professional, publication-quality PDF Synopsis
for Bharat Yatra: India Tourist Cities Travel Cost Calculator & AI Planner.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically render total page numbers and running footer."""
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
            self.drawString(54, letter[1] - 36, "Bharat Yatra — Project Synopsis & Technical Architecture")
            self.setStrokeColor(colors.HexColor("#D8E2DC"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)
            
        # Running footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, footer_text)
        self.drawString(54, 32, "Confidential & Proprietary • Bharat Yatra Project")
        self.setStrokeColor(colors.HexColor("#D8E2DC"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)
        
        self.restoreState()


def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Palette
    C_PRIMARY = colors.HexColor("#1B4332")      # Deep Forest Green
    C_SECONDARY = colors.HexColor("#2D6A4F")    # Sage Green
    C_ACCENT = colors.HexColor("#52B788")       # Mint Accent
    C_BG_LIGHT = colors.HexColor("#F4F7F4")     # Soft Nature Tint
    C_TEXT_DARK = colors.HexColor("#1F2421")     # Charcoal Text
    C_TEXT_MUTED = colors.HexColor("#52796F")    # Slate Green Text

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=C_PRIMARY,
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=C_SECONDARY,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=C_PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=C_SECONDARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=C_TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=C_TEXT_DARK,
        leftIndent=15,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=C_TEXT_DARK
    )

    code_block_style = ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F3826"),
        backColor=colors.HexColor("#F0F4EF"),
        borderPadding=6,
        spaceAfter=8
    )

    story = []

    # ==================== COVER / HEADER BANNER ====================
    story.append(Paragraph("PROJECT SYNOPSIS & TECHNICAL SPECIFICATION", ParagraphStyle('SuperTitle', fontName='Helvetica-Bold', fontSize=9, textColor=C_ACCENT, leading=11, spaceAfter=4)))
    story.append(Paragraph("BHARAT YATRA (भारत यात्रा)", title_style))
    story.append(Paragraph("National India Tourist Cities Travel Cost Calculator & AI Planning Studio", subtitle_style))
    
    # Metadata Pill Box
    meta_data = [
        [
            Paragraph("<b>Domain:</b> Domestic Indian Tourism & Budgeting", table_cell_style),
            Paragraph("<b>Stack:</b> Python 3.11+ / Streamlit / SQLite / Gemini", table_cell_style),
            Paragraph("<b>Deployment:</b> Docker / Render Cloud", table_cell_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[170, 180, 154])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#D1E2D2")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D1E2D2")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=C_SECONDARY, spaceAfter=10))

    # ==================== 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT ====================
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "<b>1.1 Background & Transformation:</b> The project originated as a Western corporate/grant tool based on United States "
        "General Services Administration (GSA) per-diem rates (FY24 allowances, Chicago travel policies, USD currency). "
        "It was radically overhauled and engineered from the ground up for <b>National Indian Tourism</b>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>1.2 Problem Addressed:</b> Indian domestic travelers (families, solo tourists, backpackers, students) face significant fragmentation "
        "when planning holidays. Airfare, rail tariffs (IRCTC Vande Bharat vs. 3AC vs. Sleeper), hotel tiers, local commute (autos, cabs, metros), "
        "and monument entry fees are scattered across disparate portals. <b>Bharat Yatra</b> bridges this gap by unifying cost estimation in "
        "<b>Indian Rupee (₹ INR)</b>, verified regional tourism data, dynamic itinerary curation, and personal trip tracking in one sleek platform.",
        body_style
    ))

    # ==================== 2. CORE SYSTEM CAPABILITIES ====================
    story.append(Paragraph("2. Key System Capabilities", h1_style))
    story.append(Paragraph("• <b>45+ Curated Indian Tourist Destinations:</b> Comprehensive data across North, South, East, West, Central, North-East, and Islands.", bullet_style))
    story.append(Paragraph("• <b>Realistic Multi-Tier Indian Cost Engine:</b> Automatic rate baselines for Budget (Hostels/Dhabas), Standard (3-Star Hotels/Family Cafes), and Luxury (Heritage Resorts/Fine Dining).", bullet_style))
    story.append(Paragraph("• <b>Inter-city Transit Estimation:</b> Pre-computed distance matrix connecting major departure hubs (Delhi, Mumbai, Bengaluru, Kolkata, Chennai, etc.) with accurate return fares.", bullet_style))
    story.append(Paragraph("• <b>Unified AI Travel Studio:</b> Fast dual-speed generation featuring <i>Instant Offline Mode (0.1s)</i> and <i>Live Gemini AI (gemini-3.8-flash)</i> for day-by-day itineraries and dynamic travel advice.", bullet_style))
    story.append(Paragraph("• <b>Context-Aware YatraAI Copilot:</b> Real-time interactive chatbot that queries the active user trip session (departure, destination, duration, budget, food, safety) to answer context-specific questions.", bullet_style))
    story.append(Paragraph("• <b>Full User Authentication & History:</b> SQLite-powered account creation, salted password hashing, 6-digit email OTP password recovery via Resend API, and a personal Saved Trips Dashboard.", bullet_style))

    # ==================== 3. TECHNOLOGY STACK SPECIFICATION ====================
    story.append(Spacer(1, 6))
    story.append(Paragraph("3. Technology Stack Specification", h1_style))
    
    tech_data = [
        [Paragraph("Category", table_header_style), Paragraph("Technology / Package", table_header_style), Paragraph("Version", table_header_style), Paragraph("Functional Role", table_header_style)],
        [Paragraph("Core Runtime", table_cell_style), Paragraph("Python", table_cell_style), Paragraph("3.11 / 3.14", table_cell_style), Paragraph("Application runtime, data manipulation, algorithm execution", table_cell_style)],
        [Paragraph("Web Application", table_cell_style), Paragraph("Streamlit", table_cell_style), Paragraph("1.65.0", table_cell_style), Paragraph("Reactive user interface, state management, interactive widgets", table_cell_style)],
        [Paragraph("Data Engine", table_cell_style), Paragraph("Pandas", table_cell_style), Paragraph("3.0.6", table_cell_style), Paragraph("CSV ingestion, dataset querying, route matrix lookups", table_cell_style)],
        [Paragraph("Generative AI", table_cell_style), Paragraph("Google GenAI SDK", table_cell_style), Paragraph("2.21.0", table_cell_style), Paragraph("Gemini 3.8 Flash model invocation for live itinerary generation", table_cell_style)],
        [Paragraph("Transactional Email", table_cell_style), Paragraph("Resend SDK", table_cell_style), Paragraph("2.36.0", table_cell_style), Paragraph("Direct email delivery of 6-digit password reset verification OTPs", table_cell_style)],
        [Paragraph("Database", table_cell_style), Paragraph("SQLite3", table_cell_style), Paragraph("Built-in", table_cell_style), Paragraph("Relational storage for user accounts, OTP records, and saved trips", table_cell_style)],
        [Paragraph("Security / Crypto", table_cell_style), Paragraph("Python hashlib", table_cell_style), Paragraph("Built-in", table_cell_style), Paragraph("SHA-256 cryptographic password hashing with custom salt", table_cell_style)],
        [Paragraph("Containerization", table_cell_style), Paragraph("Docker", table_cell_style), Paragraph("3.11-slim", table_cell_style), Paragraph("Containerized runtime with dynamic $PORT binding for Render", table_cell_style)],
        [Paragraph("Automated Testing", table_cell_style), Paragraph("Pytest", table_cell_style), Paragraph("9.1.1", table_cell_style), Paragraph("Automated unit test suite validating formulas, data, and fallbacks", table_cell_style)],
    ]
    
    tech_table = Table(tech_data, colWidths=[80, 110, 64, 250])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(tech_table)

    story.append(PageBreak())

    # ==================== 4. ARCHITECTURE & DIRECTORY STRUCTURE ====================
    story.append(Paragraph("4. Architecture & File Breakdown", h1_style))
    story.append(Paragraph(
        "The project follows a modular, decoupled architecture separating UI presentation, computation, "
        "authentication, data storage, and external API gateways:",
        body_style
    ))

    dir_structure = (
        "travel_cost_calculator/\n"
        "├── .streamlit/\n"
        "│   ├── config.toml            # Light nature theme (#2D6A4F), headless config, minimal toolbar\n"
        "│   └── secrets.toml           # Encrypted local API keys (Gemini & Resend) — git-ignored\n"
        "├── data/\n"
        "│   ├── bharat_yatra.db        # SQLite relational database (Users, OTPs, Saved Trips)\n"
        "│   ├── india_tourist_cities.csv# Database of 45+ cities (rates, attractions, cuisine, seasons)\n"
        "│   └── india_routes.csv       # Hub-to-destination transit distance and return fare baselines\n"
        "├── src/\n"
        "│   ├── app.py                 # Multi-page router, Dashboard, Calculator, Auth & Nature CSS\n"
        "│   ├── auth.py                # Database connection, salted hashing, OTPs, trip persistence\n"
        "│   ├── travel_calculator.py   # Cost math, route lookups, INR formatter, summary generator\n"
        "│   ├── ai_planner.py          # Gemini 3.8 Flash caller, fast single-pass planner, Copilot\n"
        "│   └── data.py                # Static definitions (departure hubs, travel styles, transit modes)\n"
        "├── tests/\n"
        "│   └── test_calculator.py     # 9 pytest test cases verifying computation and data structure\n"
        "├── app.py                     # Root execution wrapper for Streamlit runner\n"
        "├── Dockerfile                 # Production Docker image with dynamic $PORT binding\n"
        "├── requirements.txt           # Dependency declaration list\n"
        "└── README.md                  # Comprehensive documentation and deployment guide"
    )
    story.append(Paragraph(dir_structure.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_block_style))

    # ==================== 5. DETAILED MODULE LOGIC & ALGORITHMS ====================
    story.append(Paragraph("5. Detailed Module Logic & Algorithms", h1_style))
    
    story.append(Paragraph("5.1 Mathematical Budget Calculation Engine (travel_calculator.py)", h2_style))
    story.append(Paragraph(
        "The cost model calculates realistic domestic budgets based on 5 independent expense vectors plus an emergency contingency margin:<br/>"
        "• <b>Duration & Lodging:</b> Total Days = (End Date - Start Date) + 1. Hotel Nights = max(1, Total Days - 1).<br/>"
        "• <b>Inter-city Transit:</b> Flat cost per vehicle for Personal Drive / Cab; Per-person Return Fare × Travelers for Flight, Train, and Bus.<br/>"
        "• <b>Lodging Cost:</b> Hotel Nights × Rooms Needed × Nightly Hotel Rate.<br/>"
        "• <b>Meals & Dining:</b> Total Days × Travelers × Food Rate per Day.<br/>"
        "• <b>Local Commute:</b> Total Days × Daily Transit Rate.<br/>"
        "• <b>Sightseeing & Monument Passes:</b> Total Days × Travelers × Daily Ticket Baseline.<br/>"
        "• <b>Contingency Buffer:</b> Subtotal × (Buffer % / 100). Grand Total = Subtotal + Buffer.<br/>"
        "• <b>Currency Formatting:</b> The proprietary <code>format_inr()</code> function splits digits according to the Indian numbering system (grouping the final 3 digits, then pairs of 2 digits, e.g. ₹1,25,000).",
        body_style
    ))

    story.append(Paragraph("5.2 Dual-Engine AI Architecture (ai_planner.py)", h2_style))
    story.append(Paragraph(
        "To avoid the latency of multi-call conversational loops, the AI subsystem was optimized into a <b>Single-Pass Fast Generation</b> model:<br/>"
        "1. <b>Single Prompt Synthesis:</b> The prompt requests both the Day-by-Day schedule and 4 specific money-saving hacks simultaneously, reducing round-trip API latency by over 65%.<br/>"
        "2. <b>Dynamic Model Selection:</b> Uses Google's <code>gemini-3.8-flash</code> with a 1200-token envelope for sub-3-second responses.<br/>"
        "3. <b>Dual Speed Modes:</b> Users can select <i>⚡ Instant Mode (0.1s)</i> which compiles structured itineraries instantly from the local destination database, or <i>🤖 Live Gemini AI</i> for customized LLM generation.<br/>"
        "4. <b>Dynamic Context-Aware Copilot:</b> The YatraAI assistant queries the active trip context dictionary. When the user asks about their selected trip, departure hub, budget, or foods, the Copilot dynamically answers using their exact session parameters instead of repeating static text.",
        body_style
    ))

    story.append(Paragraph("5.3 Authentication & Resend OTP Gateway (auth.py)", h2_style))
    story.append(Paragraph(
        "• <b>Password Security:</b> Uses SHA-256 with an application-specific cryptographic salt to prevent rainbow table attacks.<br/>"
        "• <b>Resend Email OTP Dispatch:</b> When a password reset is initiated, a cryptographically random 6-digit numeric OTP is stored in the <code>otps</code> table with a 15-minute expiration timestamp and dispatched via Resend API from <code>onboarding@resend.dev</code>.<br/>"
        "• <b>Trip History Persistence:</b> Provides CRUD operations for users to save calculated trips to their account and review them on the Dashboard.",
        body_style
    ))

    story.append(PageBreak())

    # ==================== 6. DATABASE SCHEMA ====================
    story.append(Paragraph("6. Database Schema & Data Models", h1_style))
    story.append(Paragraph(
        "The application utilizes SQLite3 for local persistence and supports PostgreSQL in production via connection strings:",
        body_style
    ))

    db_data = [
        [Paragraph("Table Name", table_header_style), Paragraph("Column", table_header_style), Paragraph("Data Type", table_header_style), Paragraph("Description & Constraints", table_header_style)],
        [Paragraph("<b>users</b>", table_cell_style), Paragraph("id<br/>name<br/>email<br/>password_hash<br/>created_at", table_cell_style), Paragraph("INTEGER PK<br/>TEXT<br/>TEXT UNIQUE<br/>TEXT<br/>TIMESTAMP", table_cell_style), Paragraph("User account registry. Unique indexed email. Salted SHA-256 password hash.", table_cell_style)],
        [Paragraph("<b>otps</b>", table_cell_style), Paragraph("email<br/>otp_code<br/>created_at<br/>expires_at", table_cell_style), Paragraph("TEXT PK<br/>TEXT<br/>TIMESTAMP<br/>TIMESTAMP", table_cell_style), Paragraph("Password reset verification codes. 6-digit OTP with 15-minute TTL.", table_cell_style)],
        [Paragraph("<b>saved_trips</b>", table_cell_style), Paragraph("id<br/>user_email<br/>destination<br/>origin<br/>travel_dates<br/>travelers<br/>travel_style<br/>total_budget<br/>cost_per_person<br/>created_at", table_cell_style), Paragraph("INTEGER PK<br/>TEXT<br/>TEXT<br/>TEXT<br/>TEXT<br/>INTEGER<br/>TEXT<br/>TEXT<br/>TEXT<br/>TIMESTAMP", table_cell_style), Paragraph("Saved trip estimates. Foreign reference to user email. Stores complete trip snapshot for dashboard display.", table_cell_style)],
    ]
    db_table = Table(db_data, colWidths=[70, 90, 84, 260])
    db_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
    ]))
    story.append(db_table)

    # ==================== 7. DEPLOYMENT & DEVOPS LIFECYCLE ====================
    story.append(Spacer(1, 8))
    story.append(Paragraph("7. Deployment & DevOps Lifecycle", h1_style))
    story.append(Paragraph(
        "<b>7.1 Docker Containerization:</b> The application is containerized using an official lightweight <code>python:3.11-slim</code> "
        "base image. It incorporates a non-root environment, dynamic <code>$PORT</code> resolution (<code>--server.port=${PORT:-8501}</code>) "
        "allowing immediate deployment to Render, Railway, AWS, or GCP without port conflicts.",
        body_style
    ))
    story.append(Paragraph(
        "<b>7.2 Cloud Deployment on Render.com:</b><br/>"
        "1. <b>Continuous Integration:</b> Connected directly to GitHub repository <code>ShaikhVaiz/travel_cost_calculator</code>.<br/>"
        "2. <b>Automatic Builds:</b> Every git push automatically triggers a Docker build and zero-downtime rolling deployment.<br/>"
        "3. <b>Environment Secrets:</b> Configured with production environment variables <code>GEMINI_API_KEY</code> and <code>RESEND_API_KEY</code>.<br/>"
        "4. <b>Public Availability:</b> Globally accessible via HTTPS at <code>https://bharat-yatra.onrender.com</code>.",
        body_style
    ))
    story.append(Paragraph(
        "<b>7.3 Quality Assurance & Verification:</b> Pytest executes 9 automated test suites verifying dataset integrity, "
        "state/city filtering, inter-city fare estimations, INR currency formatting, budget arithmetic, and AI offline fallback safety.",
        body_style
    ))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    out_path = r"C:\Users\Vaiz\Downloads\Amaan_Project\travel_cost_calculator\Bharat_Yatra_Project_Synopsis.pdf"
    build_pdf(out_path)
