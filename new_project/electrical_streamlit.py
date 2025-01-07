# # Streamlit application
# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import mean_squared_error, r2_score

# # Set the page configuration
# st.set_page_config(page_title="EV Sales Prediction", layout="wide")

# # Title of the app
# st.title("Electric Vehicle (EV) Sales Prediction Dashboard")

# # Step 1: Upload the dataset
# st.sidebar.header("Upload Dataset")
# uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

# if uploaded_file:
#     # Load the dataset
#     df = pd.read_csv(uploaded_file)

#     # Display the first few rows of the dataset
#     st.subheader("Dataset Preview")
#     st.dataframe(df.head())

#     # Step 2: Data Preprocessing
#     st.sidebar.subheader("Data Preprocessing")
#     with st.spinner("Processing the data..."):
#         # Converting 'Date' to datetime
#         df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
#         df.dropna(subset=['Date'], inplace=True)

#         # Extracting features from 'Date'
#         df['Year'] = df['Date'].dt.year
#         df['Month'] = df['Date'].dt.month

#         # Encoding categorical variables
#         df = pd.get_dummies(df, columns=['State', 'Vehicle_Class', 'Vehicle_Category', 'Vehicle_Type'], drop_first=True)

#         # Dropping unnecessary columns
#         if 'Month_Name' in df.columns:
#             df.drop(['Date', 'Month_Name'], axis=1, inplace=True)
#         else:
#             df.drop(['Date'], axis=1, inplace=True)

#         # Display processed dataset
#         st.subheader("Processed Dataset")
#         st.dataframe(df.head())

#     # Step 3: Feature and Target Variables
#     X = df.drop('EV_Sales_Quantity', axis=1)
#     y = df['EV_Sales_Quantity']

#     # Splitting into training and testing datasets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#     # Step 4: Model Training
#     st.sidebar.subheader("Model Parameters")
#     n_estimators = st.sidebar.slider("Number of Trees (n_estimators)", 10, 200, 100, step=10)
#     random_state = st.sidebar.number_input("Random State", value=42, step=1)

#     with st.spinner("Training the model..."):
#         model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
#         model.fit(X_train, y_train)

#     # Step 5: Predictions
#     y_pred = model.predict(X_test)

#     # Step 6: Model Evaluation
#     mse = mean_squared_error(y_test, y_pred)
#     rmse = np.sqrt(mse)
#     r2 = r2_score(y_test, y_pred)

#     st.subheader("Model Evaluation")
#     st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
#     st.write(f"R-squared (R²): {r2:.2f}")

#     # Step 7: Visualizations
#     st.subheader("Visualizations")

#     # Actual vs Predicted Plot
#     st.write("### Actual vs Predicted EV Sales")
#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.scatter(y_test, y_pred, alpha=0.6)
#     ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
#     ax.set_title('Actual vs Predicted EV Sales')
#     ax.set_xlabel('Actual EV Sales')
#     ax.set_ylabel('Predicted EV Sales')
#     st.pyplot(fig)

#     # Feature Importance
#     st.write("### Feature Importance")
#     importances = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
#     fig, ax = plt.subplots(figsize=(10, 6))
#     importances.plot(kind='bar', ax=ax)
#     ax.set_title('Feature Importance')
#     st.pyplot(fig)

# else:
#     st.write("Please upload a CSV file to proceed.")










# Streamlit application
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Set the page configuration
st.set_page_config(page_title="EV Sales Prediction Dashboard", layout="wide")

# Title of the app
st.title("Electric Vehicle (EV) Sales Prediction Dashboard")

# Step 1: Upload the dataset
st.sidebar.header("Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load the dataset
    df = pd.read_csv(uploaded_file)

    # Display the first few rows of the dataset
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # Step 2: Data Preprocessing
    st.sidebar.subheader("Data Preprocessing")
    with st.spinner("Processing the data..."):
        # Converting 'Date' to datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            # Extracting features from 'Date'
            df['Year'] = df['Date'].dt.year
            df['Month'] = df['Date'].dt.month
        else:
            st.warning("No 'Date' column found. Skipping date preprocessing.")

        # Encoding categorical variables
        categorical_columns = ['State', 'Vehicle_Class', 'Vehicle_Category', 'Vehicle_Type']
        for col in categorical_columns:
            if col in df.columns:
                df = pd.get_dummies(df, columns=[col], drop_first=True)

        # Dropping unnecessary columns
        if 'Month_Name' in df.columns:
            df.drop(['Month_Name'], axis=1, inplace=True)

        if 'Date' in df.columns:
            df.drop(['Date'], axis=1, inplace=True)

        # Display processed dataset
        st.subheader("Processed Dataset")
        st.dataframe(df.head())

    # Step 3: Feature and Target Variables
    if 'EV_Sales_Quantity' not in df.columns:
        st.error("The dataset must contain the 'EV_Sales_Quantity' column.")
        st.stop()

    X = df.drop('EV_Sales_Quantity', axis=1)
    y = df['EV_Sales_Quantity']

    # Splitting into training and testing datasets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 4: Model Training
    st.sidebar.subheader("Model Parameters")
    n_estimators = st.sidebar.slider("Number of Trees (n_estimators)", 10, 200, 100, step=10)
    random_state = st.sidebar.number_input("Random State", value=42, step=1)

    with st.spinner("Training the model..."):
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        model.fit(X_train, y_train)

    # Step 5: Predictions
    y_pred = model.predict(X_test)

    # Step 6: Model Evaluation
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    st.subheader("Model Evaluation")
    st.write(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    st.write(f"R-squared (R²): {r2:.2f}")

    # Step 7: Visualizations
    st.subheader("Visualizations")

    # Actual vs Predicted Plot
    st.write("### Actual vs Predicted EV Sales")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_test, y_pred, alpha=0.6)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=2)
    ax.set_title('Actual vs Predicted EV Sales')
    ax.set_xlabel('Actual EV Sales')
    ax.set_ylabel('Predicted EV Sales')
    st.pyplot(fig)

    # Feature Importance
    st.write("### Feature Importance")
    importances = pd.Series(model.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))
    importances.plot(kind='bar', ax=ax)
    ax.set_title('Feature Importance')
    st.pyplot(fig)

else:
    st.write("Please upload a CSV file to proceed.")
