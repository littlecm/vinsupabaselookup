import os
import streamlit as st
from supabase import create_client, Client

# Initialize Supabase client
supabase_url = os.environ["SUPABASE_URL"]
supabase_key = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(supabase_url, supabase_key)

def query_inventory(vin_or_stock):
    """
    Query the database for a specific VIN or Stock number.
    Adjust the query as needed based on your database schema and requirements.
    """
    query = supabase.table("homenet7bbf18e26ccf4__83fbe7a3dbd89ef4a_csv").select("*").or_("vin.eq.{0},stock.eq.{0}".format(vin_or_stock))
    data = query.execute()
    return data.data

# Streamlit app layout
st.title("Inventory Lookup")
with st.form("input_form"):
    vin_or_stock = st.text_input("Enter Stock # or VIN #:")
    submitted = st.form_submit_button("Submit")
    if submitted:
        results = query_inventory(vin_or_stock)
        if results:
            for result in results:
                # Formatted display of results with additional fields
                st.subheader(f"{result.get('Year', 'Unknown Year')} {result.get('make', 'Unknown Make')} {result.get('model', 'Unknown Model')}")
                st.write(f"**VIN:** {result.get('vin', 'N/A')}")
                st.write(f"**Stock Number:** {result.get('stock', 'N/A')}")
                st.write(f"**Link:** [View]({result.get('Link', '#')})")
                st.write(f"**Type:** {result.get('Type', 'N/A')}")
                if result.get('images'):
                    images = result.get('images').split(',')  # Assuming images are comma-separated
                    if images:
                        st.image(images[0], caption="Vehicle Image", use_column_width=True)  # Display the first image
                st.write(f"**Book Value:** ${result.get('bookvalue', 'N/A')}")
                st.write(f"**Dealership:** {result.get('dealership', 'N/A')}")
                st.write(f"**Misc Price 1:** ${result.get('miscprice1', 'N/A')}")
                st.write(f"**Misc Price 2:** ${result.get('miscprice2', 'N/A')}")
                st.write(f"**Misc Price 3:** ${result.get('miscprice3', 'N/A')}")
                st.write(f"**Date in Stock:** {result.get('dateinstock', 'N/A')}")
                st.write(f"**Selling Price:** ${result.get('sellingprice', 'N/A')}")
                # Add more fields as desired
        else:
            st.write("No results found.")
