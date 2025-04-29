import streamlit as st
import hashlib
import time

# Function to create a block
def create_block(index, data, previous_hash):
    return {
        'index': index,
        'data': data,
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
        'previous_hash': previous_hash
    }

# Function to generate hash
def generate_hash(block):
    block_string = f"{block['index']}{block['data']}{block['timestamp']}{block['previous_hash']}"
    return hashlib.sha256(block_string.encode()).hexdigest()

# Initialize session state for blockchain
if 'blockchain' not in st.session_state:
    genesis_block = create_block(0, "Genesis Block", "0")
    st.session_state.blockchain = [genesis_block]

# Function to add a new membership
def add_membership(name, contact, month, time_slot):
    previous_block = st.session_state.blockchain[-1]
    new_index = previous_block['index'] + 1
    new_hash = generate_hash(previous_block)

    data = {
        "name": name,
        "contact": contact,
        "month": month,
        "time": time_slot
    }

    new_block = create_block(new_index, data, new_hash)
    st.session_state.blockchain.append(new_block)

# Streamlit UI
st.title("🏋️ Gym Membership Blockchain")

with st.form("membership_form"):
    name = st.text_input("Name")
    contact = st.text_input("Contact")
    month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June",
                                   "July", "August", "September", "October", "November", "December"])
    time_slot = st.time_input("Preferred Time Slot")

    submitted = st.form_submit_button("Add Membership")
    if submitted:
        if name and contact:
            add_membership(name, contact, month, time_slot.strftime("%I:%M %p"))
            st.success("✅ Membership added to the blockchain.")
        else:
            st.warning("Please enter both name and contact.")

# Display the blockchain
st.subheader("📜 Gym Membership Blockchain")
for block in st.session_state.blockchain:
    st.markdown(f"**Block Index:** {block['index']}")
    st.json(block['data'])
    st.markdown(f"**Timestamp:** {block['timestamp']}")
    st.markdown(f"**Previous Hash:** `{block['previous_hash']}`")
    st.markdown("---")
