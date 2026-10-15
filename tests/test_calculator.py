import pytest
from datetime import date, timedelta
import sys
import os

# Add src to python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from travel_calculator import (
    load_india_tourist_data,
    load_india_routes_data,
    get_unique_states,
    get_cities_by_state,
    get_city_details,
    estimate_intercity_fare,
    calculate_trip_budget,
    format_inr,
    generate_trip_summary_text
)
from ai_planner import (
    generate_ai_itinerary,
    generate_ai_budget_tips,
    ask_ai_travel_copilot
)


def test_load_india_tourist_data():
    df = load_india_tourist_data()
    assert not df.empty, "Tourist dataset should not be empty"
    assert "City" in df.columns
    assert "State" in df.columns
    assert "Hotel_Budget_Night" in df.columns
    assert len(df) >= 20, "Should have at least 20 top tourist destinations"


def test_get_unique_states_and_cities():
    df = load_india_tourist_data()
    states = get_unique_states(df)
    assert "Rajasthan" in states
    assert "Goa" in states
    assert "Himachal Pradesh" in states

    rajasthan_cities = get_cities_by_state(df, "Rajasthan")
    assert "Jaipur" in rajasthan_cities
    assert "Udaipur" in rajasthan_cities


def test_get_city_details():
    df = load_india_tourist_data()
    details = get_city_details(df, "Jaipur", "Rajasthan")
    assert details["City"] == "Jaipur"
    assert details["Hotel_Standard_Night"] > 0
    assert "Amber Fort" in details["Key_Attractions"]
    assert "Dal Baati" in details["Top_Foods"]


def test_estimate_intercity_fare():
    routes_df = load_india_routes_data()
    ow, rt, note = estimate_intercity_fare("Delhi", "Jaipur", "Train 3AC / Vande Bharat (Round Trip)", routes_df)
    assert ow > 0
    assert rt == ow * 2
    assert "3AC" in note or "train" in note.lower() or "indicative" in note.lower()


def test_format_inr():
    assert format_inr(500) == "₹500"
    assert format_inr(1500) == "₹1,500"
    assert format_inr(25000) == "₹25,000"
    assert format_inr(125000) == "₹1,25,000"
    assert format_inr(10000000) == "₹1,00,00,000"


def test_calculate_trip_budget():
    start = date(2026, 11, 1)
    end = date(2026, 11, 5) # 5 days, 4 nights
    num_travelers = 2
    rooms_needed = 1
    
    result = calculate_trip_budget(
        start_date=start,
        end_date=end,
        num_travelers=num_travelers,
        rooms_needed=rooms_needed,
        travel_style="Standard / Family",
        intercity_fare_roundtrip=2000.0, # per person
        intercity_mode="Train 3AC",
        hotel_rate_per_night=3000.0, # per room
        food_rate_per_day_per_person=1000.0,
        local_transit_per_day=800.0,
        sightseeing_per_day_per_person=500.0,
        emergency_buffer_pct=10.0
    )

    assert result["total_days"] == 5
    assert result["hotel_nights"] == 4
    # Intercity: 2000 * 2 = 4000
    assert result["intercity_total"] == 4000.0
    # Hotel: 4 nights * 1 room * 3000 = 12000
    assert result["hotel_total"] == 12000.0
    # Food: 5 days * 2 pax * 1000 = 10000
    assert result["food_total"] == 10000.0
    # Local transit: 5 days * 800 = 4000
    assert result["local_transit_total"] == 4000.0
    # Sightseeing: 5 days * 2 pax * 500 = 5000
    assert result["sightseeing_total"] == 5000.0
    # Subtotal: 4000 + 12000 + 10000 + 4000 + 5000 = 35000
    assert result["subtotal"] == 35000.0
    # Buffer (10%): 3500
    assert result["emergency_buffer"] == 3500.0
    # Grand Total: 38500
    assert result["grand_total"] == 38500.0
    assert result["cost_per_person"] == 19250.0


def test_generate_trip_summary_text():
    start = date(2026, 11, 1)
    end = date(2026, 11, 4)
    res = calculate_trip_budget(
        start, end, 2, 1, "Standard", 1500, "Train", 2500, 800, 500, 300, 10
    )
    summary = generate_trip_summary_text("Jaipur", "Rajasthan", start, end, res)
    assert "Jaipur, Rajasthan" in summary
    assert "ITEMIZED ESTIMATE BREAKDOWN" in summary
    assert "TOTAL ESTIMATED BUDGET" in summary


def test_ai_itinerary_offline_fallback():
    city_details = {
        "Key_Attractions": "Amber Fort, Hawa Mahal, City Palace",
        "Top_Foods": "Dal Baati Churma, Pyaaz Kachori",
        "Pro_Tip": "Book composite tickets at Amber Fort",
        "Category": "Heritage",
        "Best_Months": "Oct - Mar"
    }
    itinerary = generate_ai_itinerary(
        city="Jaipur",
        state="Rajasthan",
        days=3,
        num_travelers=2,
        travel_style="Standard",
        city_details=city_details,
        api_key=None # Ensures fallback testing
    )
    assert "Day 1:" in itinerary
    assert "Day 2:" in itinerary
    assert "Day 3:" in itinerary
    assert "Amber Fort" in itinerary
    assert "Dal Baati Churma" in itinerary


def test_ai_copilot_offline():
    reply_safety = ask_ai_travel_copilot("Is it safe for solo travelers?", api_key=None)
    assert "Safety Tips" in reply_safety or "112" in reply_safety

    reply_packing = ask_ai_travel_copilot("What to pack?", api_key=None)
    assert "Packing Checklist" in reply_packing or "clothing" in reply_packing.lower()


if __name__ == "__main__":
    pytest.main(["-v"])
