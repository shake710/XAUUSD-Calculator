import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards

def calculate_xauusd_pips(entry_price, exit_price, lot_size, pip_size=0.01):
    if not (isinstance(entry_price, (int, float)) and entry_price > 0):
        return "Invalid entry price. Must be a positive number."
    
    if not (isinstance(exit_price, (int, float)) and exit_price > 0):
        return "Invalid exit price. Must be a positive number."
    
    if not (isinstance(pip_size, (int, float)) and pip_size > 0):
        return "Invalid pip size. Must be a positive number."

    price_movement = exit_price - entry_price
    pips = round(price_movement / pip_size, 2)
    profit_loss = pips * lot_size

    direction = "BUY" if exit_price > entry_price else "SELL"

    return {
        'pips': pips,
        'profit_loss': profit_loss,
        'direction': direction
    }

def calculate_risk_management(entry_price, stop_loss, take_profit, lot_size, pip_size=0.01):
    risk_pips = round((entry_price - stop_loss) / pip_size, 2) if stop_loss else 0
    reward_pips = round((take_profit - entry_price) / pip_size, 2) if take_profit else 0

    risk_reward_ratio = round(abs(reward_pips / risk_pips), 2) if risk_pips != 0 else None

    risk_amount = risk_pips * lot_size
    reward_amount = reward_pips * lot_size

    return {
        'risk_pips': risk_pips,
        'reward_pips': reward_pips,
        'risk_reward_ratio': risk_reward_ratio,
        'risk_amount': risk_amount,
        'reward_amount': reward_amount
    }

st.title("📊 XAUUSD Calculator")

col1, col2 = st.columns(2)

with col1:
    st.header("⚙️ Trade Details")
    entry_price = st.number_input("Entry Price", min_value=0.0, format="%.2f")
    exit_price = st.number_input("Exit Price", min_value=0.0, format="%.2f")
    stop_loss = st.number_input("Stop Loss Price", min_value=0.0, format="%.2f")
    take_profit = st.number_input("Take Profit Price", min_value=0.0, format="%.2f")

    lot_size_choice = st.selectbox("Lot Size Type", ['Fixed (Standard/Mini/Micro)', 'Custom'])

    if lot_size_choice == 'Fixed (Standard/Mini/Micro)':
        lot_size_mapping = {'standard': 1, 'mini': 0.1, 'micro': 0.01}
        fixed_lot_size = st.selectbox("Select Lot Size", list(lot_size_mapping.keys()))
        lot_size = lot_size_mapping[fixed_lot_size]
    else:
        lot_size = st.number_input("Custom Lot Size", min_value=0.01, format="%.2f")

with col2:
    st.header("📊 Results")
    result = calculate_xauusd_pips(entry_price, exit_price, lot_size)
    risk_result = calculate_risk_management(entry_price, stop_loss, take_profit, lot_size)

    if isinstance(result, dict) and isinstance(risk_result, dict):
        st.text_input("Amount at Risk ($)", value=f"{risk_result['risk_amount']:.2f}", disabled=True)
        st.text_input("Take Profit (Pips)", value=f"{risk_result['reward_pips']}", disabled=True)
        st.text_input("Stop Loss (Pips)", value=f"{risk_result['risk_pips']}", disabled=True)
        st.text_input("Potential Profit ($)", value=f"{risk_result['reward_amount']:.2f}", disabled=True)
        st.text_input("Risk/Reward Ratio", value=f"{risk_result['risk_reward_ratio']}", disabled=True)

st.subheader("⚠️ Disclaimer")
st.write("The results from this calculator are for informational purposes only and may differ from actual outcomes due to market conditions. Please use caution and consider professional advice before making trading decisions.")


