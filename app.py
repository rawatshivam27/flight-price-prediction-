import streamlit as st
import joblib
from datetime import datetime

# Load the model and dictionaries (moved from Flask app)
model = joblib.load(open(r'model.pkl', 'rb'))

# Dictionaries for categorical variables
airline_dict = {'AirAsia': 0, "Indigo": 1, "GO_FIRST": 2, "SpiceJet": 3, "Air_India": 4, "Vistara": 5}
source_dict = {'Delhi': 0, "Hyderabad": 1, "Bangalore": 2, "Mumbai": 3, "Kolkata": 4, "Chennai": 5}
departure_dict = {'Early_Morning': 0, "Morning": 1, "Afternoon": 2, "Evening": 3, "Night": 4, "Late_Night": 5}
stops_dict = {'zero': 0, "one": 1, "two_or_more": 2}
arrival_dict = {'Early_Morning': 0, "Morning": 1, "Afternoon": 2, "Evening": 3, "Night": 4, "Late_Night": 5}
destination_dict = {'Delhi': 0, "Hyderabad": 1, "Mumbai": 2, "Bangalore": 3, "Chennai": 4, "Kolkata": 5}
class_dict = {'Economy': 0, 'Business': 1}

def predict_flight_price(form_data):
    """Direct prediction function without HTTP requests"""
    try:
        airline = airline_dict[form_data['airline']]
        source_city = source_dict[form_data['source_city']]
        departure_time = departure_dict[form_data['departure_time']]
        stops = stops_dict[form_data['stops']]
        arrival_time = arrival_dict[form_data['arrival_time']]
        destination_city = destination_dict[form_data['destination_city']]
        travel_class = class_dict[form_data['class']]
        
        # Calculate date difference
        departure_date = datetime.strptime(form_data['departure_date'], '%Y-%m-%d')
        date_diff = (departure_date - datetime.today()).days + 1

        # Prepare features for prediction
        features = [airline, source_city, departure_time, stops, arrival_time, 
                   destination_city, travel_class, date_diff]
        prediction = model.predict([features])[0]

        return round(prediction, 2)
    except KeyError as e:
        raise ValueError(f'Missing data for: {e}')
    except Exception as e:
        raise ValueError(str(e))

def flight_price_predictor():
    st.title("Flight Price Prediction")
    
    with st.form("prediction_form"):
        # Airline Field
        airline = st.selectbox(
            "Airline",
            ["", "SpiceJet", "AirAsia", "Vistara", "GO_FIRST", "Indigo", "Air_India"]
        )
        
        # Source City Field
        source_city = st.selectbox(
            "Source City",
            ["", "Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"]
        )
        
        # Departure Time Field
        departure_time = st.selectbox(
            "Departure Time",
            ["", "Evening", "Early_Morning", "Morning", "Afternoon", "Night", "Late_Night"]
        )
        
        # Stops Field
        stops = st.selectbox(
            "Stops",
            ["", "zero", "one", "two_or_more"]
        )
        
        # Arrival Time Field
        arrival_time = st.selectbox(
            "Arrival Time",
            ["", "Night", "Morning", "Early_Morning", "Afternoon", "Evening", "Late_Night"]
        )
        
        # Destination City Field
        destination_city = st.selectbox(
            "Destination City",
            ["", "Delhi", "Mumbai", "Bangalore", "Kolkata", "Hyderabad", "Chennai"]
        )
        
        # Class Field
        flight_class = st.selectbox(
            "Class",
            ["", "Economy", "Business"]
        )
        
        # Departure Date Field
        departure_date = st.date_input(
            "Departure Date",
            min_value=datetime.today()
        )
        
        submitted = st.form_submit_button("Predict")
        
        if submitted:
            # Validate all fields are selected
            if "" in [airline, source_city, departure_time, stops, 
                      arrival_time, destination_city, flight_class]:
                st.error("Please fill in all fields")
                return
                
            form_data = {
                "airline": airline,
                "source_city": source_city,
                "departure_time": departure_time,
                "stops": stops,
                "arrival_time": arrival_time,
                "destination_city": destination_city,
                "class": flight_class,
                "departure_date": departure_date.strftime("%Y-%m-%d")
            }
            
            try:
                prediction = predict_flight_price(form_data)
                st.success(f"Your Flight Price: ₹{prediction}")
            except ValueError as e:
                st.error(f"Error: {e}")

if __name__ == "__main__":
    flight_price_predictor()
