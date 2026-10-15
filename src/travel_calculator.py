"""
India Tourist Cities Travel Cost Calculator
Core computation engine for domestic travel planning across India.
"""

import os
from datetime import datetime, date
import pandas as pd


def get_data_dir() -> str:
    """Returns the absolute path to the data directory."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "data")


def load_india_tourist_data(csv_path: str = None) -> pd.DataFrame:
    """Load the Indian tourist cities dataset."""
    if csv_path is None:
        csv_path = os.path.join(get_data_dir(), "india_tourist_cities.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Tourist cities dataset not found at {csv_path}")
        
    df = pd.read_csv(csv_path)
    # Ensure numeric columns are properly typed
    numeric_cols = [
        "Hotel_Budget_Night", "Hotel_Standard_Night", "Hotel_Luxury_Night",
        "Food_Budget_Day", "Food_Standard_Day", "Food_Luxury_Day",
        "Local_Transit_Budget_Day", "Local_Transit_Standard_Day", "Local_Transit_Luxury_Day",
        "Sightseeing_Est_Daily"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    return df


def load_india_routes_data(csv_path: str = None) -> pd.DataFrame:
    """Load route fare estimations between major hubs and tourist spots."""
    if csv_path is None:
        csv_path = os.path.join(get_data_dir(), "india_routes.csv")
    
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return pd.DataFrame()


def get_unique_states(df: pd.DataFrame) -> list:
    """Return sorted list of Indian states present in the dataset."""
    if "State" not in df.columns:
        return []
    states = sorted(df["State"].dropna().unique().tolist())
    return states


def get_cities_by_state(df: pd.DataFrame, state: str) -> list:
    """Return list of cities for a given Indian state."""
    if "State" not in df.columns or "City" not in df.columns:
        return []
    filtered = df[df["State"].str.lower() == state.strip().lower()]
    return sorted(filtered["City"].unique().tolist())


def get_city_details(df: pd.DataFrame, city: str, state: str = None) -> dict:
    """Get complete rate & info profile for a specific destination city."""
    if state:
        match = df[(df["City"].str.lower() == city.strip().lower()) & 
                   (df["State"].str.lower() == state.strip().lower())]
    else:
        match = df[df["City"].str.lower() == city.strip().lower()]
        
    if match.empty:
        return {}
    return match.iloc[0].to_dict()


def estimate_intercity_fare(origin: str, destination: str, travel_mode: str, routes_df: pd.DataFrame = None) -> tuple:
    """
    Estimate round-trip intercity transport fare per traveler based on route and mode.
    Returns: (one_way_fare, round_trip_fare, note)
    """
    if routes_df is not None and not routes_df.empty:
        # Match origin and destination
        match = routes_df[(routes_df["Origin"].str.lower() == origin.strip().lower()) & 
                          (routes_df["Destination"].str.lower().str.contains(destination.strip().lower()))]
        if not match.empty:
            row = match.iloc[0]
            if "Flight" in travel_mode:
                ow = row.get("Flight_Fare_OneWay", 0)
                if ow > 0:
                    return float(ow), float(ow * 2), "Route-specific airline average fare"
            elif "Train 3AC" in travel_mode or "Vande Bharat" in travel_mode:
                ow = row.get("Train_3AC_Fare_OneWay", 0)
                if ow > 0:
                    return float(ow), float(ow * 2), "Route-specific 3AC/Vande Bharat fare"
            elif "Train Sleeper" in travel_mode:
                ow = row.get("Train_3AC_Fare_OneWay", 0)
                if ow > 0:
                    sl_ow = max(250.0, float(ow * 0.45))
                    return sl_ow, float(sl_ow * 2), "Route-specific Sleeper class fare"
            elif "Bus" in travel_mode:
                ow = row.get("Bus_Volvo_Fare_OneWay", 0)
                if ow > 0:
                    return float(ow), float(ow * 2), "Route-specific Volvo/AC sleeper bus fare"
            elif "Car" in travel_mode or "Cab" in travel_mode:
                total_car = row.get("Drive_Toll_Fuel_OneWay", 0)
                if total_car > 0:
                    return float(total_car), float(total_car * 2), "Round-trip driving fuel & toll cost for the vehicle"

    # Default heuristic estimates if specific route pair not in table
    defaults = {
        "Flight (Round Trip)": (4500.0, 9000.0, "Indicative domestic return airfare"),
        "Train 3AC / Vande Bharat (Round Trip)": (1400.0, 2800.0, "Indicative round-trip 3AC/Chair Car fare"),
        "Train Sleeper Class (Round Trip)": (550.0, 1100.0, "Indicative round-trip Sleeper fare"),
        "AC Volvo Bus (Round Trip)": (1100.0, 2200.0, "Indicative return interstate Volvo bus fare"),
        "Personal Car / Cab (Drive - Total Vehicle)": (4000.0, 8000.0, "Estimated vehicle fuel & highway tolls"),
        "Self-Arranged / Local Arrival (₹0)": (0.0, 0.0, "Already at destination or arranged separately")
    }
    
    for key, val in defaults.items():
        if travel_mode.split()[0] in key:
            return val
            
    return (1500.0, 3000.0, "Standard domestic transport estimate")


def format_inr(amount: float) -> str:
    """Format an amount into Indian Currency display (e.g. ₹1,25,000)."""
    if pd.isna(amount) or amount is None:
        return "₹0"
    
    amount = round(float(amount))
    sign = "-" if amount < 0 else ""
    amount_str = str(abs(amount))
    
    if len(amount_str) <= 3:
        return f"{sign}₹{amount_str}"
    
    last3 = amount_str[-3:]
    remaining = amount_str[:-3]
    
    # In Indian numbering, every 2 digits after the last 3 are grouped
    parts = []
    while len(remaining) > 2:
        parts.insert(0, remaining[-2:])
        remaining = remaining[:-2]
    if remaining:
        parts.insert(0, remaining)
        
    formatted = ",".join(parts) + "," + last3
    return f"{sign}₹{formatted}"


def calculate_trip_budget(
    start_date,
    end_date,
    num_travelers: int,
    rooms_needed: int,
    travel_style: str,
    intercity_fare_roundtrip: float,
    intercity_mode: str,
    hotel_rate_per_night: float,
    food_rate_per_day_per_person: float,
    local_transit_per_day: float,
    sightseeing_per_day_per_person: float,
    emergency_buffer_pct: float = 10.0
) -> dict:
    """
    Calculate comprehensive trip budget for Indian domestic tourism.
    """
    # Calculate days and nights
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    elif isinstance(start_date, datetime):
        start_date = start_date.date()

    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    elif isinstance(end_date, datetime):
        end_date = end_date.date()

    total_days = max(1, (end_date - start_date).days + 1)
    hotel_nights = max(1, (end_date - start_date).days) if total_days > 1 else 1

    # Intercity transport
    is_vehicle_flat = "Car" in intercity_mode or "Cab" in intercity_mode
    if is_vehicle_flat:
        intercity_total = float(intercity_fare_roundtrip)
    else:
        intercity_total = float(intercity_fare_roundtrip) * num_travelers

    # Lodging
    hotel_total = hotel_nights * max(1, rooms_needed) * float(hotel_rate_per_night)

    # Food & Dining
    food_total = total_days * num_travelers * float(food_rate_per_day_per_person)

    # Local Sightseeing & Commute
    local_transit_total = total_days * float(local_transit_per_day)

    # Monument & Activity entry charges
    sightseeing_total = total_days * num_travelers * float(sightseeing_per_day_per_person)

    # Subtotal
    subtotal = (
        intercity_total +
        hotel_total +
        food_total +
        local_transit_total +
        sightseeing_total
    )

    # Contingency buffer
    emergency_buffer = subtotal * (max(0.0, float(emergency_buffer_pct)) / 100.0)
    grand_total = subtotal + emergency_buffer

    cost_per_person = grand_total / max(1, num_travelers)
    cost_per_day = grand_total / total_days

    return {
        "total_days": total_days,
        "hotel_nights": hotel_nights,
        "num_travelers": num_travelers,
        "rooms_needed": rooms_needed,
        "travel_style": travel_style,
        "intercity_mode": intercity_mode,
        "intercity_total": intercity_total,
        "hotel_total": hotel_total,
        "food_total": food_total,
        "local_transit_total": local_transit_total,
        "sightseeing_total": sightseeing_total,
        "subtotal": subtotal,
        "emergency_buffer": emergency_buffer,
        "grand_total": grand_total,
        "cost_per_person": cost_per_person,
        "cost_per_day": cost_per_day,
        # Formatted string representations
        "fmt_intercity_total": format_inr(intercity_total),
        "fmt_hotel_total": format_inr(hotel_total),
        "fmt_food_total": format_inr(food_total),
        "fmt_local_transit_total": format_inr(local_transit_total),
        "fmt_sightseeing_total": format_inr(sightseeing_total),
        "fmt_subtotal": format_inr(subtotal),
        "fmt_emergency_buffer": format_inr(emergency_buffer),
        "fmt_grand_total": format_inr(grand_total),
        "fmt_cost_per_person": format_inr(cost_per_person),
        "fmt_cost_per_day": format_inr(cost_per_day),
    }


def generate_trip_summary_text(
    city: str,
    state: str,
    start_date: date,
    end_date: date,
    costs: dict
) -> str:
    """Generates an organized, readable text summary for copy-pasting or reporting."""
    summary = f"""======================================================
🇮🇳 INDIA TRIP BUDGET PLANNER SUMMARY
======================================================
Destination   : {city}, {state}
Travel Period : {start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')} ({costs['total_days']} Days / {costs['hotel_nights']} Nights)
Travelers     : {costs['num_travelers']} Person(s) | {costs['rooms_needed']} Room(s)
Trip Style    : {costs['travel_style']}
Travel Mode   : {costs['intercity_mode']}

------------------------------------------------------
💰 ITEMIZED ESTIMATE BREAKDOWN:
------------------------------------------------------
1. Inter-city Travel (Round Trip) : {costs['fmt_intercity_total']}
2. Accommodation ({costs['hotel_nights']} Nights)      : {costs['fmt_hotel_total']}
3. Meals & Dining ({costs['total_days']} Days)         : {costs['fmt_food_total']}
4. Local Sightseeing & Commute    : {costs['fmt_local_transit_total']}
5. Activities & Monument Passes   : {costs['fmt_sightseeing_total']}
------------------------------------------------------
Subtotal Cost                     : {costs['fmt_subtotal']}
Contingency & Emergency Buffer    : {costs['fmt_emergency_buffer']}
======================================================
TOTAL ESTIMATED BUDGET            : {costs['fmt_grand_total']}
Cost Per Person                   : {costs['fmt_cost_per_person']}
Daily Average Spend               : {costs['fmt_cost_per_day']}
======================================================
* Generated with India Tourist City Travel Calculator & AI Planner
"""
    return summary
