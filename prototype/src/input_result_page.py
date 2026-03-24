import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from src.home_guideline import custom_css

custom_css("style.css")

def _read_csv(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        return pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read CSV file: {exc}")
        return None

# force columns to be numeric (dataframe)
def _numeric_columns(df: pd.DataFrame) -> list[str]:
    numeric_cols = []
    for col in df.columns:
        coerced = pd.to_numeric(df[col], errors="coerce")
        if coerced.notna().sum() > 0:
            numeric_cols.append(col)
    return numeric_cols


# compute evaluation metrics (rmse, mae, r^2) 
def _compute_metrics(y_true: pd.Series, y_pred: pd.Series) -> dict:
    if len(y_true) == 0:
        return {"RMSE": np.nan, "MAE": np.nan, "R^2": np.nan}

    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
    mae = float(mean_absolute_error(y_true, y_pred))
    r2 = float(r2_score(y_true, y_pred)) if len(y_true) >= 2 else np.nan
    return {"RMSE": rmse, "MAE": mae, "R^2": r2}


def page_one() -> None:
    st.markdown('<div id="Input"></div>', unsafe_allow_html=True)
    
    # Wrap back button in its own container
    st.markdown('<div class="back-button-container">', unsafe_allow_html=True)
    st.button("← Back to Home", on_click=lambda: st.session_state.update({"page": "home"}))
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.title("Precipitation Forecasting")

    source_file = st.file_uploader("Drop or choose CSV file", type=["csv"], key="source_file")
    source_df = _read_csv(source_file)
    if source_df is not None:
        st.session_state.source_df = source_df
        st.caption(f"Rows loaded: {len(source_df)}")
        st.dataframe(source_df, use_container_width=True, height=320)

        # Find precipitation column (look for PRCP or precipitation)
        precip_col = None
        for col in source_df.columns:
            col_lower = col.lower()
            if "prcp" in col_lower or "precip" in col_lower or "rain" in col_lower:
                precip_col = col
                break
        
        if precip_col:
            st.session_state.baseline_value_col = precip_col
            st.session_state.ensemble_value_col = precip_col
        else:
            st.error(f"No precipitation column found. Available columns: {', '.join(source_df.columns)}")
            st.session_state.baseline_value_col = None
            st.session_state.ensemble_value_col = None
            st.warning("Please ensure your CSV has a column with precipitation values (e.g., 'PRCP', 'Precipitation', 'Rain').")

    ready = all(
        [
            st.session_state.source_df is not None,
            st.session_state.baseline_value_col,
            st.session_state.ensemble_value_col,
        ]
    )

    if st.button("Run Comparison", use_container_width=True, disabled=not ready):
        st.session_state["page"] = "results"
        st.rerun()

    if not ready:
        st.info("Upload CSV file with a precipitation column to continue.")
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

def plot_metric_comparison(metric_name, baseline_val, ensemble_val):
    fig, ax = plt.subplots(figsize=(6,4), constrained_layout=True)

    methods = ["Baseline", "Ensemble"]
    values = [baseline_val, ensemble_val]
    colors = ["#FF6B6B", "#4ECDC4"]

    ax.bar(methods, values, color=colors)
    ax.set_ylabel(metric_name)
    ax.set_title(metric_name)
    ax.grid(axis="y", alpha=0.3)

    for i, v in enumerate(values):
        if not np.isnan(v):
            ax.text(i, v + max(values)*0.02, f"{v:.4f}", ha="center", fontweight="bold")

    return fig

def page_two() -> None:
    st.title("Precipitation Forecast - 1 Day Ahead Results")

    source_df = st.session_state.source_df

    if source_df is None:
        st.warning("Data is missing. Please return to Page 1 and upload the CSV file.")
        if st.button("Back to Page 1"):
            st.session_state["page"] = "input"
            st.rerun()
        return

    try:
        baseline_vals = pd.to_numeric(source_df[st.session_state.baseline_value_col], errors="coerce")
        ensemble_vals = pd.to_numeric(source_df[st.session_state.ensemble_value_col], errors="coerce")

        if st.session_state.date_col:
            dates = pd.to_datetime(source_df[st.session_state.date_col], errors="coerce", dayfirst=True)
            aligned = pd.DataFrame({"date": dates, "baseline": baseline_vals, "ensemble": ensemble_vals}).dropna()
            aligned = aligned.sort_values("date")
            align_note = f"Aligned by date from one CSV (used rows: {len(aligned)})"
        else:
            aligned = pd.DataFrame({"baseline": baseline_vals, "ensemble": ensemble_vals}).dropna()
            align_note = f"Aligned by row order from one CSV (used rows: {len(aligned)})"

        y_true = aligned["baseline"]
        y_pred = aligned["ensemble"]

        st.caption(align_note)
        st.caption(
            f"Valid numeric rows: baseline={baseline_vals.notna().sum()}, "
            f"ensemble={ensemble_vals.notna().sum()}, compared={len(y_true)}"
        )

        # compute evaluation metrics (aint working yet)
        baseline_eval = _compute_metrics(y_true, y_pred)
        ensemble_eval = _compute_metrics(y_pred, y_true)

        # display metrics as graphs
        st.subheader("Evaluation Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            fig = plot_metric_comparison(
                "Root Mean Squared Error",
                baseline_eval["RMSE"],
                ensemble_eval["RMSE"]
            )       
            st.pyplot(fig, use_container_width=False)
            plt.close(fig)

        with col2:
            fig = plot_metric_comparison(
                "Mean Absolute Error",
                baseline_eval["MAE"],
                ensemble_eval["MAE"]
            )
            st.pyplot(fig, use_container_width=False)
            plt.close(fig)

        with col3:
            fig = plot_metric_comparison(
                "R² Score",
                baseline_eval["R^2"],
                ensemble_eval["R^2"]
            )
            st.pyplot(fig, use_container_width=False)
            plt.close(fig)
 
        # 1-day ahead forecast
        st.subheader("1-Day Ahead Precipitation Forecast (measured in inches)")
        
        if len(aligned) > 0:
            # use the last ensemble prediction as the 1-day ahead forecast
            last_baseline = y_true.iloc[-1] if len(y_true) > 0 else 0
            last_ensemble = y_pred.iloc[-1] if len(y_pred) > 0 else 0
            
            col1_forecast, col2_forecast = st.columns(2)
            
            # placeholder
            baseline = 6.181
            target = 5.56

            with col1_forecast:
                st.metric("Last Observed Actual", f"{baseline:.4f}", delta=None)
            
            with col2_forecast:
                st.metric("1-Day Ahead Forecast", f"{target:.4f}", 
                         delta=f"{target - baseline:.4f}", delta_color="inverse")

        if len(y_true) == 0:
            st.warning("No overlapping valid numeric rows were found. Metrics are NaN.")

    except Exception as exc:
        st.error(f"Evaluation failed: {exc}")
    
    st.warning("This is a prototype. Metrics are not computed correctly yet, and the 1-day ahead forecast is just the last ensemble prediction (for demonstration).")

    if st.button("Back to Page 1", use_container_width=True):
        st.session_state["page"] = "input"
        st.rerun()