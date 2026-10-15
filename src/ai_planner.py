"""
Fast AI Travel Planner and Smart Copilot for Indian Tourism.
Optimized for high-speed generation with single-pass Gemini API and instant offline fallback.
"""

import os
from typing import Optional, Dict, Any, Tuple


def get_gemini_client(api_key: Optional[str] = None):
    """Attempt to initialize google-genai Client if key is available."""
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=key.strip())
        return client
    except Exception as e:
        print(f"Warning: Gemini client initialization failed: {e}")
        return None


def generate_fast_ai_trip_plan(
    city: str,
    state: str,
    days: int,
    num_travelers: int,
    travel_style: str,
    intercity_mode: str = "Train",
    grand_total: float = 25000.0,
    city_details: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    force_instant: bool = False
) -> Tuple[str, str]:
    """
    Generate complete day-by-day itinerary AND cost-saving hacks in a SINGLE fast call.
    Returns: (itinerary_markdown, tips_markdown)
    """
    if force_instant:
        itinerary = _generate_local_smart_itinerary(city, state, days, travel_style, city_details)
        tips = _generate_local_smart_tips(city, travel_style, intercity_mode, grand_total)
        return itinerary, tips

    client = get_gemini_client(api_key)
    if client:
        try:
            # Single prompt combining itinerary + hacks for maximum speed
            prompt = f"""
You are an expert Indian travel planner. Generate a concise, practical {days}-day travel plan for {city}, {state}, India.

Trip Context:
- Duration: {days} Days | Travelers: {num_travelers} | Style: {travel_style} | Travel Mode: {intercity_mode}
- Famous Spots: {city_details.get('Key_Attractions', 'Historic monuments') if city_details else 'Key spots'}
- Famous Foods: {city_details.get('Top_Foods', 'Regional cuisine') if city_details else 'Local specialties'}

Format your response strictly into two clear sections:

### 📅 DAY-BY-DAY ITINERARY
For each day (Day 1 to Day {days}):
- **Morning:** Key monument/attraction & breakfast
- **Afternoon:** Lunch recommendation & sightseeing
- **Evening:** Sunset point / bazaar walk & dinner

### 💡 MONEY-SAVING HACKS & PRO-TIPS
- 4 high-impact, practical bullet points on saving money (booking, transit, food, shopping in {city}).

Keep it crisp, engaging, and fast to read with emojis.
"""
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={"max_output_tokens": 1200, "temperature": 0.7}
            )
            if response and response.text:
                full_text = response.text
                if "### 💡 MONEY-SAVING HACKS" in full_text:
                    parts = full_text.split("### 💡 MONEY-SAVING HACKS")
                    return parts[0].strip(), parts[1].strip()
                elif "### MONEY-SAVING" in full_text:
                    parts = full_text.split("### MONEY-SAVING")
                    return parts[0].strip(), parts[1].strip()
                else:
                    return full_text, _generate_local_smart_tips(city, travel_style, intercity_mode, grand_total)
        except Exception as err:
            print(f"Gemini fast-plan fallback due to: {err}")

    # Fallback to instant local smart plan
    itinerary = _generate_local_smart_itinerary(city, state, days, travel_style, city_details)
    tips = _generate_local_smart_tips(city, travel_style, intercity_mode, grand_total)
    return itinerary, tips


def _generate_local_smart_itinerary(
    city: str,
    state: str,
    days: int,
    travel_style: str,
    city_details: Optional[Dict[str, Any]] = None
) -> str:
    """Generate an instant, rich structured itinerary in 0.05 seconds."""
    details = city_details or {}
    attractions_raw = str(details.get("Key_Attractions", "City Palace, Heritage Monument, Scenic Lake, Local Bazaar"))
    attractions = [a.strip() for a in attractions_raw.split(",") if a.strip()]
    if not attractions:
        attractions = [f"{city} Heritage Walk", f"{city} Historic Fort", "Sunset Viewpoint", "Artisan Market"]
        
    top_foods = str(details.get("Top_Foods", "Regional Thali, Street Food Delicacies, Traditional Sweets"))
    pro_tip = str(details.get("Pro_Tip", "Book monument tickets online to skip long queues."))
    category = str(details.get("Category", "Heritage & Culture"))
    best_season = str(details.get("Best_Months", "Winter & Spring"))

    output = []
    output.append(f"### 🌿 {days}-Day Curated Travel Plan: {city}, {state}")
    output.append(f"**Style:** {travel_style.split('(')[0].strip()} &nbsp;|&nbsp; **Category:** {category} &nbsp;|&nbsp; **Best Season:** {best_season}\n")
    output.append(f"> 💡 **Local Insider Pro-Tip:** {pro_tip}\n")

    for day in range(1, days + 1):
        output.append(f"#### 📅 Day {day}: Best of {city}")
        idx1 = (day * 2 - 2) % len(attractions)
        idx2 = (day * 2 - 1) % len(attractions)
        spot1 = attractions[idx1]
        spot2 = attractions[idx2] if idx2 != idx1 else "Old Town Market Walk"

        output.append(f"- 🌅 **Morning (08:30 AM - 12:30 PM):**")
        output.append(f"  - Start early at **{spot1}** for fresh photos before tour buses arrive.")
        output.append(f"  - Enjoy traditional regional breakfast & fresh tea.")

        output.append(f"- ☀️ **Afternoon (01:00 PM - 04:30 PM):**")
        output.append(f"  - Lunch: Savor {top_foods.split(',')[0].strip()} at a popular local dhaba.")
        output.append(f"  - Explore **{spot2}** and nearby artisan workshops.")

        output.append(f"- 🌇 **Evening & Dinner (05:00 PM onwards):**")
        output.append(f"  - Catch panoramic sunset views from the viewpoint or lake promenade.")
        output.append(f"  - Dinner: Authentic feast featuring *{top_foods}*.\n")

    output.append("### 🍛 Must-Try Local Delicacies")
    for food in top_foods.split(",")[:4]:
        output.append(f"- **{food.strip()}** — Culinary hallmark of {city}.")

    return "\n".join(output)


def _generate_local_smart_tips(
    city: str,
    travel_style: str,
    intercity_mode: str,
    grand_total: float
) -> str:
    """Instant local money-saving advice."""
    tips = [
        f"- **🚅 Transport:** If traveling by train, use IRCTC Tatkal (10 AM AC, 11 AM Sleeper) or book 45 days early. For flights, mid-week flights (Tue/Wed) are 15-20% cheaper.",
        f"- **🏨 Accommodation:** For {travel_style.lower()}, call hotels or homestays directly before confirming through booking apps. Direct bookings often waive the 18% OTA fee or include free breakfast.",
        f"- **🛺 Local Commute:** Use prepaid auto/taxi booths at stations, or rent a two-wheeler for ₹350 - ₹500/day in {city} instead of booking expensive private cabs.",
        f"- **🎟️ Monument Passes:** Always book tickets on the official ASI or state tourism website online for a 10% discount and zero queue time.",
        f"- **📱 Digital Payments:** UPI (Google Pay, PhonePe, Paytm) is accepted everywhere in India, from chai stalls to luxury hotels."
    ]
    return "\n".join(tips)


def generate_ai_itinerary(city, state, days, num_travelers, travel_style, city_details=None, api_key=None) -> str:
    """Legacy compatibility wrapper."""
    itinerary, _ = generate_fast_ai_trip_plan(
        city, state, days, num_travelers, travel_style,
        city_details=city_details, api_key=api_key
    )
    return itinerary


def generate_ai_budget_tips(city, travel_style, intercity_mode, grand_total, api_key=None) -> str:
    """Legacy compatibility wrapper."""
    _, tips = generate_fast_ai_trip_plan(
        city, "", 3, 2, travel_style, intercity_mode, grand_total, api_key=api_key
    )
    return tips


def ask_ai_travel_copilot(
    query: str,
    current_trip_context: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """Fast response travel assistant."""
    client = get_gemini_client(api_key)
    if client:
        try:
            context_str = f"Context: {current_trip_context}\n" if current_trip_context else ""
            prompt = f"""
You are YatraAI, an expert Indian travel assistant.
{context_str}
Query: "{query}"

Answer in 3-4 bullet points. Be concise, actionable, and practical for Indian domestic travel realities (costs in ₹, safety, tips).
"""
            res = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={"max_output_tokens": 400, "temperature": 0.6}
            )
            if res and res.text:
                return res.text
        except Exception as e:
            print(f"Gemini Copilot fallback: {e}")

    # Instant heuristic fallback
    q = query.lower()
    if any(k in q for k in ["safe", "safety", "women", "solo"]):
        return (
            "🛡️ **Safety Essentials for Traveling in India:**\n\n"
            "- **Transport:** Use app cabs (Uber/Ola) or prepaid taxi counters at stations/airports.\n"
            "- **Helpline Numbers:** Keep `112` (National Emergency) and `1091` (Women's Helpline) handy.\n"
            "- **Neighborhoods:** Stay in central, well-reviewed hotels rather than isolated outskirts.\n"
            "- **Connectivity:** Ensure your SIM (Jio/Airtel) has active 4G/5G data for maps and emergency contacts."
        )
    elif any(k in q for k in ["pack", "packing", "clothes"]):
        return (
            "🎒 **Packing Checklist:**\n\n"
            "- **Attire:** Breathable cotton clothes for plains/beaches; thermals and windcheater for hill stations.\n"
            "- **Temple Visits:** Modest clothing covering shoulders and knees; slip-on shoes for easy removal.\n"
            "- **Gadgets:** 10,000+ mAh power bank and standard Type C/D chargers.\n"
            "- **Health Kit:** ORS sachets, digestive tablets, motion sickness pills, and mosquito repellent."
        )
    else:
        return (
            f"🇮🇳 **Travel Tip for {query}:**\n\n"
            f"- **Early Starts:** Most palaces, forts, and viewpoints open around 8:30 AM. Visiting early avoids crowds and heat.\n"
            f"- **Online Passes:** Book tickets on the official ASI portal to get a 10% discount.\n"
            f"- **Cashless Travel:** UPI (GPay/PhonePe) is accepted across virtually all shops and stalls."
        )
