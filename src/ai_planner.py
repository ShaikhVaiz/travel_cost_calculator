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
    current_trip_context: Optional[Any] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Intelligent, context-aware travel copilot.
    Dynamically answers questions about the traveler's selected trip, departure hub, budget,
    attractions, food, safety, packing, and routes using live Gemini AI with rich dynamic fallback.
    """
    # Extract rich trip details if provided as dict or string
    origin = "Delhi NCR"
    city = "Jaipur"
    state = "Rajasthan"
    days = 4
    travelers = 2
    style = "Standard / Family"
    mode = "Train"
    total_cost = "₹24,800"
    cost_per_person = "₹12,400"
    city_info = {}

    if isinstance(current_trip_context, dict):
        origin = current_trip_context.get("origin", origin)
        city = current_trip_context.get("city", city)
        state = current_trip_context.get("state", state)
        days = current_trip_context.get("days", days)
        travelers = current_trip_context.get("travelers", travelers)
        style = current_trip_context.get("style", style)
        mode = current_trip_context.get("mode", mode)
        total_cost = current_trip_context.get("total_cost", total_cost)
        cost_per_person = current_trip_context.get("cost_per_person", cost_per_person)
        city_info = current_trip_context.get("city_info", {}) or {}
    elif isinstance(current_trip_context, str):
        # Fallback parse from context string if needed
        pass

    q = query.strip().lower()

    # 1. Direct Context Queries (Instant & 100% Accurate)
    if any(k in q for k in ["departure", "origin", "leaving from", "from where", "starting city", "hub"]):
        return (
            f"✈️ **Departure Details:**\n\n"
            f"- **Departure Hub:** **{origin}**\n"
            f"- **Destination:** **{city}, {state}**\n"
            f"- **Travel Mode:** {mode}\n\n"
            f"You are currently planning a journey starting from **{origin}** to **{city}**."
        )

    if any(k in q for k in ["what trip", "which trip", "selected trip", "my trip", "where am i going", "destination"]):
        return (
            f"📍 **Your Current Trip Overview:**\n\n"
            f"- **Destination:** **{city}, {state}**\n"
            f"- **Departure From:** **{origin}**\n"
            f"- **Duration:** **{days} Days**\n"
            f"- **Travelers:** **{travelers} Person(s)**\n"
            f"- **Travel Style:** {style}\n"
            f"- **Transport:** {mode}\n"
            f"- **Total Estimated Budget:** **{total_cost}** ({cost_per_person} per person)"
        )

    if any(k in q for k in ["budget", "cost", "how much", "price", "expense", "spend"]):
        return (
            f"💰 **Estimated Budget Breakdown for {city}:**\n\n"
            f"- **Total Trip Cost:** **{total_cost}**\n"
            f"- **Cost Per Person:** **{cost_per_person}** (for {travelers} travelers)\n"
            f"- **Duration:** {days} Days\n"
            f"- **Travel Style:** {style}\n"
            f"- **Intercity Transit:** {mode} from {origin}\n\n"
            f"💡 *Tip:* Check the **Trip Calculator** tab for the itemized breakdown (Hotels, Meals, Commute, Monument passes)."
        )

    if any(k in q for k in ["food", "dish", "dishes", "eat", "cuisine", "street food"]):
        foods = city_info.get("Top_Foods", "Regional Thali, Street Food Delicacies, Traditional Sweets")
        return (
            f"🍛 **Culinary Specialties in {city}, {state}:**\n\n"
            f"- **Must-Try Delicacies:** {foods}\n"
            f"- **Where to Eat:** Look for busy local family eateries with high food turnover for maximum taste and hygiene.\n"
            f"- **Hygiene Tip:** Always drink packaged mineral water (Bisleri/Kinley) and enjoy hot, freshly made street foods."
        )

    if any(k in q for k in ["attraction", "visit", "see", "monument", "places", "spot", "sightseeing"]):
        spots = city_info.get("Key_Attractions", f"Iconic monuments and heritage spots in {city}")
        tip = city_info.get("Pro_Tip", "Book tickets online in advance.")
        return (
            f"🌟 **Top Places to Visit in {city}:**\n\n"
            f"- **Key Attractions:** {spots}\n"
            f"- **Insider Tip:** {tip}\n"
            f"- Head to the **AI Smart Itinerary** tab to get a morning-to-evening day-by-day plan for all these spots!"
        )

    if any(k in q for k in ["when", "time", "month", "season", "weather"]):
        months = city_info.get("Best_Months", "October to March")
        return (
            f"🌤️ **Best Season to Visit {city}, {state}:**\n\n"
            f"- **Peak Season:** **{months}** (pleasant weather, ideal for sightseeing).\n"
            f"- **Tip:** If traveling during peak months, book trains and hotel rooms 3-4 weeks in advance to avoid surge pricing."
        )

    # 2. Try Live Gemini Generation for other questions
    client = get_gemini_client(api_key)
    if client:
        try:
            prompt = f"""
You are YatraAI, an expert Indian travel copilot.
Context:
- User is planning a {days}-day trip to {city}, {state} from {origin}.
- Travelers: {travelers} | Style: {style} | Travel Mode: {mode} | Budget: {total_cost}

User Question: "{query}"

Answer directly, accurately, and concisely in 2-4 bullet points tailored specifically to {city} and India travel realities.
"""
            res = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={"max_output_tokens": 400, "temperature": 0.6}
            )
            if res and res.text:
                return res.text
        except Exception as e:
            print(f"Gemini Copilot API call notice: {e}")

    # 3. Dynamic Fallbacks for General Topics
    if any(k in q for k in ["safe", "safety", "women", "solo"]):
        return (
            f"🛡️ **Safety Guidelines for {city}, {state}:**\n\n"
            f"- **Transit:** Use verified app cabs (Uber/Ola) or prepaid taxi counters when arriving from {origin}.\n"
            f"- **Helpline:** National Emergency is `112` and Women's Helpline is `1091`.\n"
            f"- **Accommodations:** Choose centrally located hotels in well-lit areas with verified reviews.\n"
            f"- **Data Connectivity:** Ensure active 4G/5G data (Jio/Airtel) for real-time maps and navigation."
        )
    elif any(k in q for k in ["pack", "packing", "clothes"]):
        is_hills = any(h in state.lower() or h in city.lower() for h in ["himachal", "uttarakhand", "kashmir", "ladakh", "shimla", "manali", "ooty", "darjeeling"])
        clothing_tip = "Warm thermals, jacket, and comfortable walking shoes" if is_hills else "Breathable cotton clothes and comfortable footwear"
        return (
            f"🎒 **Packing Essentials for {city}:**\n\n"
            f"- **Clothing:** {clothing_tip}.\n"
            f"- **Temple Etiquette:** Modest attire covering shoulders and knees; easy slip-on shoes.\n"
            f"- **Tech & Power:** A reliable 10,000+ mAh power bank for photos and navigation on the go.\n"
            f"- **Medical Kit:** Antacids, ORS hydration sachets, and motion-sickness tablets if traversing winding mountain routes."
        )
    elif any(k in q for k in ["bargain", "shopping", "price", "market"]):
        return (
            f"🛍️ **Bargaining & Shopping Tips in {city}:**\n\n"
            f"- **Local Bazaars:** Politely start your counter-offer around 50-60% of the initial vendor quote.\n"
            f"- **Fixed Price Options:** For certified silk, tea, or handicrafts, visit state-run government emporiums.\n"
            f"- **Cashless:** UPI (PhonePe, GPay, Paytm) is widely accepted in {city} across shops and street stalls."
        )

    return (
        f"🌿 **YatraAI Travel Insights for {city}, {state}:**\n\n"
        f"- Regarding **\"{query}\"**: For your {days}-day trip to {city} from {origin}, plan your morning outings between 8:30 AM – 11:30 AM to beat afternoon heat and peak crowds.\n"
        f"- **Monument Passes:** Book official tickets online on the ASI portal for instant entry and a 10% discount.\n"
        f"- Check the **AI Smart Itinerary** tab above to see your customized day-by-day sightseeing plan!"
    )
