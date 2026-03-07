import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

st.set_page_config(page_title="Thesis", layout="wide")


def _init_state() -> None:
    defaults = {
        "page": 1,
        "source_df": None,
        "baseline_value_col": None,
        "ensemble_value_col": None,
        "date_col": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _read_csv(uploaded_file):
    if uploaded_file is None:
        return None
    try:
        return pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read CSV file: {exc}")
        return None

# force columns to be numeric
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
    st.title("CSV Input for Baseline vs Ensemble Approach")
    st.write("Upload CSV, then choose baseline and ensemble columns from that file. (precipitation)")

    source_file = st.file_uploader("Drop or choose CSV file", type=["csv"], key="source_file")
    source_df = _read_csv(source_file)
    if source_df is not None:
        st.session_state.source_df = source_df
        st.caption(f"Rows loaded: {len(source_df)}")
        st.dataframe(source_df, use_container_width=True, height=320)

        num_cols = _numeric_columns(source_df)
        if not num_cols:
            st.error("No numeric-like column found in the CSV.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.session_state.baseline_value_col = st.selectbox(
                    "Baseline value column",
                    options=num_cols,
                    key="baseline_value_select",
                )
            with c2:
                st.session_state.ensemble_value_col = st.selectbox(
                    "Ensemble Approach value column",
                    options=num_cols,
                    key="ensemble_value_select",
                )


    ready = all(
        [
            st.session_state.source_df is not None,
            st.session_state.baseline_value_col,
            st.session_state.ensemble_value_col,
        ]
    )

    if st.button("Run Comparison", use_container_width=True, disabled=not ready):
        st.session_state.page = 2
        st.rerun()

    if not ready:
        st.info("Upload CSV file and select both value columns to continue.")


def page_two() -> None:
    st.title("RMSE, MAE, and R^2 Evaluation")

    source_df = st.session_state.source_df

    if source_df is None:
        st.warning("Data is missing. Please return to Page 1 and upload the CSV file.")
        if st.button("Back to Page 1"):
            st.session_state.page = 1
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

        # separate evaluations (directional for R^2), then a combined comparison section.
        baseline_eval = _compute_metrics(y_true, y_pred)
        ensemble_eval = _compute_metrics(y_pred, y_true)

        # dataframes for evaluation (rmse, mae, r2)
        baseline_eval_df = pd.DataFrame(
            {
                "Study": ["Baseline Study"],
                "RMSE": [baseline_eval["RMSE"]],
                "MAE": [baseline_eval["MAE"]],
                "R^2": [baseline_eval["R^2"]],
            }
        )
        ensemble_eval_df = pd.DataFrame(
            {
                "Study": ["Ensemble Approach"],
                "RMSE": [ensemble_eval["RMSE"]],
                "MAE": [ensemble_eval["MAE"]],
                "R^2": [ensemble_eval["R^2"]],
            }
        )
        comparison_df = pd.DataFrame(
            {
                "Comparison": ["Baseline vs Ensemble Approach"],
                "RMSE": [baseline_eval["RMSE"]],
                "MAE": [baseline_eval["MAE"]],
                "R^2 (Baseline as Actual)": [baseline_eval["R^2"]],
                "R^2 (Ensemble Approach as Actual)": [ensemble_eval["R^2"]],
            }
        )

        st.subheader("Baseline Evaluation")
        st.dataframe(baseline_eval_df, use_container_width=True)

        st.subheader("Ensemble Approach Evaluation")
        st.dataframe(ensemble_eval_df, use_container_width=True)

        st.subheader("Comparison")
        st.dataframe(comparison_df, use_container_width=True)

        if len(y_true) == 0:
            st.warning("No overlapping valid numeric rows were found. Metrics are NaN.")

    except Exception as exc:
        st.error(f"Evaluation failed: {exc}")

    if st.button("Back to Page 1", use_container_width=True):
        st.session_state.page = 1
        st.rerun()


_init_state()

if st.session_state.page == 1:
    page_one()
else:
    page_two()
