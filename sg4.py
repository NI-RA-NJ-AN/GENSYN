import streamlit as st
import pandas as pd
import io
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAcUybVnEh95L57EMN5ToEMNjFsal2O3MA")  

def generate_synthetic_data(prompt, num_rows, num_columns):
    """
    Generate synthetic data based on a user prompt using the Gemini API.

    Args:
        prompt (str): The user prompt describing the dataset.
        num_rows (int): Number of rows to generate.
        num_columns (int): Number of columns to generate.

    Returns:
        pd.DataFrame: A DataFrame containing the synthetic data.
    """
    # Construct the API prompt
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    complete_prompt = f"""
    Generate a realistic and professional medical dataset based on the following description. Ensure compliance with HIPAA and GDPR privacy laws.
    {prompt}

    The dataset should contain {num_rows} rows and {num_columns} columns. Provide the data in CSV format, ensuring all entries are professional, consistent, and realistic.
    """

    response = model.generate_content(complete_prompt)

    try:
        # Get raw response
        response_text = response.text.strip()

        # Debug: Show raw response
        st.text_area("Raw Response from Generator:", response_text, height=300)

        # Split the response into lines
        lines = response_text.splitlines()

        # Filter valid lines based on the expected number of columns
        valid_lines = [
            line for line in lines
            if line.count(",") == (num_columns - 1)  # Ensure the line has the correct number of commas
        ]

        # Check if enough valid rows are available
        if len(valid_lines) < num_rows:
            st.warning("Model did not generate enough valid rows. Using placeholder data to fill the gap.")
            valid_lines += [
                ",".join([f"Placeholder_{i}_{j}" for j in range(1, num_columns + 1)])
                for i in range(len(valid_lines) + 1, num_rows + 1)
            ]

        # Limit to the exact number of rows
        valid_lines = valid_lines[:num_rows]

        # Join valid lines and parse as CSV
        cleaned_csv = "\n".join(valid_lines)
        csv_data = io.StringIO(cleaned_csv)
        df = pd.read_csv(csv_data, header=None)

        # Rename columns for better usability
        df.columns = [f"Column {i+1}" for i in range(num_columns)]

        return df

    except Exception as e:
        st.error(f"Error processing generated data: {e}")
        return pd.DataFrame(
            [[f"Sample {i+1}-{j+1}" for j in range(num_columns)] for i in range(num_rows)],
            columns=[f"Column {i+1}" for i in range(num_columns)]
        )

def main():
    st.title("Advanced Synthetic Data Generator")

    # Input Table Name
    table_name = st.text_input("Enter Table Name:", "Synthetic Data")

    # Description of the Table
    table_description = st.text_area("Enter a description for the table:", "This table is for synthetic data generation.")

    # Number of Rows and Columns
    col1, col2 = st.columns(2)
    with col1:
        num_rows = st.number_input("Number of Rows:", min_value=1, value=50)
    with col2:
        num_columns = st.number_input("Number of Columns:", min_value=1, value=4)

    # User Prompt
    user_prompt = st.text_area(
        "Enter your prompt for generating data:",
        "Generate synthetic medical insurance data for 100 policyholders, including name, age, gender, policy ID, and insurance plan details."
    )

    # Generate Data Button
    if st.button("Generate Data"):
        if not user_prompt.strip():
            st.error("Please enter a valid prompt.")
        else:
            st.info("Generating data. Please wait...")
            try:
                # Generate the data
                data = generate_synthetic_data(user_prompt, num_rows, num_columns)

                if not data.empty:
                    st.success("Data generated successfully!")

                    # Preview the data
                    st.write("### Preview of Generated Data")
                    st.dataframe(data.head(10))

                    # Prepare CSV for download
                    csv_buffer = io.StringIO()
                    data.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)

                    st.download_button(
                        label="Download Data as CSV",
                        data=csv_buffer.getvalue(),
                        file_name=f"{table_name.replace(' ', '_').lower()}.csv",
                        mime="text/csv"
                    )
                else:
                    st.error("The generated data is empty.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

app=main    
