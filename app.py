import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Gold Pattern Explorer", layout="wide")

st.title("🟠 Gold Pattern Explorer")
st.write("Historical Gold Pattern Matching & Backtesting")

st.info("النسخة الأولى: سنبدأ باستيراد البيانات واختيار العينة المستهدفة.")

st.header("1. Historical Data")
history_file = st.file_uploader(
    "Upload historical gold data (CSV)",
    type=["csv"],
    key="history"
)

if history_file is not None:
    try:
        history = pd.read_csv(history_file)
        history.columns = [c.strip().lower() for c in history.columns]

        required = ["timestamp", "open", "high", "low", "close"]
        missing = [c for c in required if c not in history.columns]

        if missing:
            st.error(f"Missing columns: {', '.join(missing)}")
        else:
            history["timestamp"] = pd.to_datetime(
                history["timestamp"], utc=True, errors="coerce"
            )

            for col in ["open", "high", "low", "close"]:
                history[col] = pd.to_numeric(history[col], errors="coerce")

            history = history.dropna(
                subset=["timestamp", "open", "high", "low", "close"]
            )
            history = history.sort_values("timestamp")
            history = history.drop_duplicates("timestamp")

            st.success(f"Loaded {len(history)} valid candles")
            st.write(
                "Historical range:",
                history["timestamp"].min(),
                "—",
                history["timestamp"].max()
            )
            st.dataframe(history.tail(10), use_container_width=True)

            st.session_state["history_data"] = history

    except Exception as e:
        st.error(f"Could not read CSV: {e}")

st.divider()
st.header("2. Target Sample")

st.write(
    "Choose a historical period to use as the target, "
    "or enter 48 candles manually in a later version."
)

if "history_data" in st.session_state:
    history = st.session_state["history_data"]

    if len(history) >= 48:
        start_index = st.number_input(
            "Starting candle index",
            min_value=0,
            max_value=len(history) - 48,
            value=max(0, len(history) - 48),
            step=1
        )

        target = history.iloc[int(start_index):int(start_index) + 48]

        st.write(
            "Target period:",
            target["timestamp"].iloc[0],
            "—",
            target["timestamp"].iloc[-1]
        )

        st.line_chart(target.set_index("timestamp")["close"])

        st.caption(
            "The selected target contains 48 consecutive rows. "
            "Hourly continuity will be checked in the matching engine."
        )
    else:
        st.warning("At least 48 valid candles are required.")

st.divider()
st.header("3. Historical Matching")
st.info("The matching engine and backtesting will be added after this initial version is saved.")
