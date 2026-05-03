import streamlit as st
import pandas as pd
import joblib


model = joblib.load("model.pkl")
model_columns = joblib.load("columns.pkl")

st.title("Car Price Prediction")
st.write("Enter car details below:")

car_names = [col.replace("Car_Name_", "") for col in model_columns if col.startswith("Car_Name_")]
car_names = sorted(car_names)
car_name = st.selectbox("Car Name", car_names)

year = st.selectbox("Year", [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])

present_price = st.number_input("Present Price (₹)", min_value=1000, max_value=100000000)
present_price_lakhs = present_price / 100000

driven_kms = st.number_input("Driven (km)", min_value=0)

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])

selling_type = st.selectbox("Selling Type", ["Individual", "Dealer"])

transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

owner_type = st.selectbox("Owner Type", ["First", "Second", "Third", "Fourth & Above"])


def get_driven_group(kms):
    if kms <= 20000:
        return "0-20k"
    if kms <= 40000:
        return "20k-40k"
    if kms <= 60000:
        return "40k-60k"
    if kms <= 80000:
        return "60k-80k"
    if kms <= 100000:
        return "80k-100k"
    if kms <= 150000:
        return "100k-150k"
    if kms <= 200000:
        return "150k-200k"
    if kms <= 300000:
        return "200k-300k"
    return "300k-400k+"

owner_map = {
    "First": 0,
    "Second": 1,
    "Third": 2,
    "Fourth & Above": 3
}

if st.button("Predict Price"):
    input_dict = {
        "Car_Name": car_name,
        "Year": year,
        "Present_Price": present_price_lakhs,
        "Driven_kms": driven_kms,
        "Owner": owner_map[owner_type],
        "Fuel_Type": fuel_type,
        "Selling_type": selling_type,
        "Transmission": transmission,
        "Driven_kms_group": get_driven_group(driven_kms)
    }
        
    

    # Convert to DataFrame
    input_df = pd.DataFrame([input_dict])

    # One-hot encoding convert data into numeric form (binary)
    input_df = pd.get_dummies(input_df)

    # Match columns
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    # Predict
    prediction = model.predict(input_df)[0]

    predicted_price = prediction * 100000

    # Output
    st.success(f"💰 Predicted Used Price: ₹ {predicted_price:,.0f}")