import streamlit as st
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
import time
import plotly.graph_objects as go
import pandas as pd

# --- RSA Key Generation ---
def generate_rsa_keys(bits=1024):
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = inverse(e, phi)
    return {'public_key': (e, n), 'private_key': (d, n)}

# --- RSA Encryption & Decryption ---
def rsa_encrypt(message, public_key):
    e, n = public_key
    m = bytes_to_long(message.encode())
    c = pow(m, e, n)
    return c

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext, d, n)
    return long_to_bytes(m).decode()

# --- Measure Performance for Different Key Sizes ---
def measure_times(message):
    key_sizes = [512, 1024, 2048]  
    key_gen_times = []
    enc_times = []
    dec_times = []

    for bits in key_sizes:
        # Key Generation
        start = time.time() #measure how long it takes to generate the keys for each size
        keys = generate_rsa_keys(bits)
        key_gen_time = time.time() - start
        key_gen_times.append(key_gen_time)

        # Encryption
        start = time.time()
        ciphertext = rsa_encrypt(message, keys['public_key'])
        enc_time = time.time() - start
        enc_times.append(enc_time)

        # Decryption
        start = time.time()
        decrypted = rsa_decrypt(ciphertext, keys['private_key'])
        dec_time = time.time() - start
        dec_times.append(dec_time)

    return key_sizes, key_gen_times, enc_times, dec_times

# --- Streamlit UI ---
st.title(" RSA Encryption & Execution Time Analysis")

st.subheader("1. Enter a Message to Encrypt:")
message = st.text_input("Your message:")

if 'keys' not in st.session_state:
    st.session_state['keys'] = generate_rsa_keys()

if st.button("Encrypt"):
    st.session_state['keys'] = generate_rsa_keys()
    ciphertext = rsa_encrypt(message, st.session_state['keys']['public_key'])
    decrypted = rsa_decrypt(ciphertext, st.session_state['keys']['private_key'])

    st.success(" Encryption Complete")
    st.write(" Ciphertext:", ciphertext)
    st.write(" Decrypted Message:", decrypted)

# --- RSA Key Size vs Execution Time ---
st.subheader("2. RSA Key Size vs. Execution Time")
st.markdown(
    "This chart compares how long it takes to generate keys, encrypt, and decrypt your message "
    "with different RSA key sizes. Bigger keys give better security but also take longer."
)

if st.button("Run Timing Comparison"):
    sizes, gen_times, enc_times, dec_times = measure_times(message) #generate RSA keys of 512, 1024, 2048 bit size

    # Show data in a table
    data = {
        'Key Size (bits)': sizes,
        'Key Generation Time (s)': [round(t, 6) for t in gen_times],
        'Encryption Time (s)': [round(t, 6) for t in enc_times],
        'Decryption Time (s)': [round(t, 6) for t in dec_times],
    }
    st.subheader(" Comparison Table")
    st.table(pd.DataFrame(data))

    # Bar chart visualization
    fig = go.Figure()
    fig.add_trace(go.Bar(x=sizes, y=gen_times, name='Key Generation Time', marker_color='mediumseagreen'))
    fig.add_trace(go.Bar(x=sizes, y=enc_times, name='Encryption Time', marker_color='dodgerblue'))
    fig.add_trace(go.Bar(x=sizes, y=dec_times, name='Decryption Time', marker_color='tomato'))

    fig.update_layout(
        barmode='group',
        title='RSA Performance by Key Size',
        xaxis_title='Key Size (bits)',
        yaxis_title='Time (seconds)',
        legend_title='Operation',
        template='plotly_white',
        yaxis=dict(rangemode='tozero')  # Ensures small values are visible
    )

    st.plotly_chart(fig)
