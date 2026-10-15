"""
Authentication and User Database Module for Bharat Yatra.
Manages user accounts, SQLite database, session states, saved trips, and Resend OTP delivery.
"""

import os
import sqlite3
import hashlib
import random
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple, List, Dict, Any

# Path to SQLite database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "bharat_yatra.db")


def get_db_connection():
    """Returns a SQLite connection with row dict access."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str) -> str:
    """Hash password using SHA-256 with a fixed salt."""
    salt = "bharat_yatra_secure_salt_2026"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


def init_db():
    """Initialize database tables for users, OTPs, and saved trips."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # OTPs table for password resets
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otps (
        email TEXT PRIMARY KEY,
        otp_code TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL
    )
    """)

    # Saved Trips table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL,
        destination TEXT NOT NULL,
        origin TEXT NOT NULL,
        travel_dates TEXT NOT NULL,
        travelers INTEGER NOT NULL,
        travel_style TEXT NOT NULL,
        total_budget TEXT NOT NULL,
        cost_per_person TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Seed default demo account if not exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@yatra.com",))
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            ("Amaan Demo", "demo@yatra.com", hash_password("demo123"))
        )

    conn.commit()
    conn.close()


def register_user(name: str, email: str, password: str) -> Tuple[bool, str]:
    """Register a new user account."""
    if not name.strip() or not email.strip() or not password.strip():
        return False, "Please fill out all required fields."
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    email = email.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name.strip(), email, hash_password(password))
        )
        conn.commit()
        return True, "Account created successfully! You can now log in."
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."
    finally:
        conn.close()


def authenticate_user(email: str, password: str) -> Tuple[bool, Optional[Dict[str, Any]], str]:
    """Authenticate user credentials."""
    email = email.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, email, password_hash FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return False, None, "No account found with this email address."
    
    if user["password_hash"] != hash_password(password):
        return False, None, "Incorrect password. Please try again."

    return True, {"id": user["id"], "name": user["name"], "email": user["email"]}, "Login successful!"


def send_password_reset_otp(email: str, resend_api_key: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
    """
    Generate 6-digit OTP and send via Resend API.
    Returns: (success, message, demo_otp_if_testing)
    """
    email = email.strip().lower()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return False, "No account found with this email.", None

    # Generate 6-digit OTP
    otp_code = "".join(random.choices(string.digits, k=6))
    expires_at = datetime.now() + timedelta(minutes=15)

    cursor.execute("""
    INSERT INTO otps (email, otp_code, expires_at)
    VALUES (?, ?, ?)
    ON CONFLICT(email) DO UPDATE SET
        otp_code = excluded.otp_code,
        expires_at = excluded.expires_at,
        created_at = CURRENT_TIMESTAMP
    """, (email, otp_code, expires_at))
    conn.commit()
    conn.close()

    # Attempt sending via Resend API
    api_key = resend_api_key or os.environ.get("RESEND_API_KEY")
    if api_key:
        try:
            import resend
            resend.api_key = api_key.strip()
            params = {
                "from": "Bharat Yatra <onboarding@resend.dev>",
                "to": [email],
                "subject": f"Your Bharat Yatra Password Reset OTP: {otp_code}",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; border: 1px solid #e2e8f0; border-radius: 8px;">
                    <h2 style="color: #FF6B35; text-align: center;">🇮🇳 Bharat Yatra</h2>
                    <p>Hello <b>{user['name']}</b>,</p>
                    <p>You requested to reset your password. Use the verification code below to complete your reset. This OTP is valid for 15 minutes.</p>
                    <div style="background-color: #F8FAFC; border: 2px dashed #FF6B35; padding: 15px; text-align: center; font-size: 28px; font-weight: bold; letter-spacing: 6px; color: #1E3A8A; margin: 20px 0;">
                        {otp_code}
                    </div>
                    <p style="color: #64748B; font-size: 13px;">If you didn't request a password reset, you can safely ignore this email.</p>
                </div>
                """
            }
            resend.Emails.send(params)
            return True, f"OTP sent to {email} via Resend!", None
        except Exception as e:
            return True, f"Resend delivery error ({e}). Using offline preview: Code is {otp_code}", otp_code

    # If no Resend key provided yet, return OTP for testing
    return True, f"OTP generated! (Resend key not set, use demo code: {otp_code})", otp_code


def verify_otp_and_reset_password(email: str, otp_code: str, new_password: str) -> Tuple[bool, str]:
    """Verify OTP and update user password."""
    if len(new_password) < 6:
        return False, "New password must be at least 6 characters long."

    email = email.strip().lower()
    otp_code = otp_code.strip()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT otp_code, expires_at FROM otps WHERE email = ?", (email,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return False, "No OTP request found for this email. Please request a new code."

    expires_at = datetime.fromisoformat(record["expires_at"]) if isinstance(record["expires_at"], str) else record["expires_at"]
    if datetime.now() > expires_at:
        conn.close()
        return False, "OTP has expired. Please request a new code."

    if record["otp_code"] != otp_code:
        conn.close()
        return False, "Invalid OTP code. Please check and re-enter."

    # Update password and clear OTP
    cursor.execute("UPDATE users SET password_hash = ? WHERE email = ?", (hash_password(new_password), email))
    cursor.execute("DELETE FROM otps WHERE email = ?", (email,))
    conn.commit()
    conn.close()

    return True, "Password reset successfully! You can now log in with your new password."


def save_user_trip(
    user_email: str,
    destination: str,
    origin: str,
    travel_dates: str,
    travelers: int,
    travel_style: str,
    total_budget: str,
    cost_per_person: str
) -> bool:
    """Save an estimated trip to the user's dashboard history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO saved_trips (user_email, destination, origin, travel_dates, travelers, travel_style, total_budget, cost_per_person)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_email.strip().lower(), destination, origin, travel_dates, travelers, travel_style, total_budget, cost_per_person))
    conn.commit()
    conn.close()
    return True


def get_user_saved_trips(user_email: str) -> List[Dict[str, Any]]:
    """Retrieve all saved trips for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, destination, origin, travel_dates, travelers, travel_style, total_budget, cost_per_person, created_at
    FROM saved_trips
    WHERE user_email = ?
    ORDER BY created_at DESC
    """, (user_email.strip().lower(),))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_user_saved_trip(trip_id: int, user_email: str) -> bool:
    """Delete a saved trip from user dashboard."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_trips WHERE id = ? AND user_email = ?", (trip_id, user_email.strip().lower()))
    conn.commit()
    conn.close()
    return True


# Run DB initialization on import
init_db()
