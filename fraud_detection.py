import streamlit as st
import pandas as pd
import joblib

# Load trained pipeline/model
model = joblib.load("fraud_detection_pipeline.pkl")

st.title("Fraud Detection Prediction App")
st.markdown("Enter transaction details below and press **Predict** to check for possible fraud.")
st.divider()

# ---- User Inputs ----
transaction_type = st.selectbox("Transaction Type", ["PAYMENT", "TRANSFER", "CASH_OUT", "CASH_IN", "DEBIT"])
amount = st.number_input("Amount", min_value=0.0, value=1000.0)
oldbalanceOrg = st.number_input("Old balance (Sender)", min_value=0.0, value=10000.0)
newbalanceOrig = st.number_input("New balance (Sender)", min_value=0.0, value=9000.0)
oldbalanceDest = st.number_input("Old balance (Receiver)", min_value=0.0, value=0.0)
newbalanceDest = st.number_input("New balance (Receiver)", min_value=0.0, value=0.0)

# ---- Create DataFrame ----
input_data = pd.DataFrame([{
    "type": transaction_type,
    "amount": amount,
    "oldbalanceOrg": oldbalanceOrg,
    "newbalanceOrig": newbalanceOrig,
    "oldbalanceDest": oldbalanceDest,
    "newbalanceDest": newbalanceDest,
}])

# ---- Predict Button ----
if st.button("Predict"):
    try:
        # Predict class
        prediction = model.predict(input_data)[0]
        
        # Predict probabilities (if supported)
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(input_data)[0][1]  # Probability of fraud (class 1)
        else:
            proba = None

        # ---- Display Results ----
        st.subheader(f"Prediction: {'Fraudulent' if prediction == 1 else 'Safe'} Transaction")

        if proba is not None:
            st.markdown(f"**Fraud Probability:** {proba:.2%}")
            st.progress(float(min(max(proba, 0.0), 1.0)))  # clamp between 0 and 1

            if proba > 0.8:
                st.error("⚠️ Very High Risk of Fraud!")
            elif proba > 0.5:
                st.warning("⚠️ Moderate Risk — Review Recommended.")
            else:
                st.success("✅ Low Risk — Transaction seems safe.")
        else:
            # fallback if model doesn't support predict_proba
            if prediction == 1:
                st.error("⚠️ This transaction can be **fraudulent**.")
            else:
                st.success("✅ This transaction seems **safe**.")
    except Exception as e:
        st.error(f"Error making prediction: {e}")
