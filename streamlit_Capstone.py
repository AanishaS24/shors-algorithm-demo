import streamlit as st
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
import random
import plotly.graph_objects as go
import plotly.subplots as sp

# RSA Key Generation
def generate_rsa_keys(bits=1024):
    p = getPrime(bits // 2)
    q = getPrime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = inverse(e, phi)
    return {'public_key': (e, n), 'private_key': (d, n)}

# RSA Encryption & Decryption
def rsa_encrypt(message, public_key):
    e, n = public_key
    m = bytes_to_long(message.encode())
    c = pow(m, e, n)
    return c

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    m = pow(ciphertext, d, n)
    return long_to_bytes(m).decode()

# GCD
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Shor’s Algorithm Simulation
def shor_classical_sim(N):
    if N % 2 == 0:
        return [2, N // 2]
    a = random.randint(2, N - 2)
    d = gcd(a, N)
    if d > 1:
        return [d, N // d]
    r = None
    for i in range(1, N):
        if pow(a, i, N) == 1:
            r = i
            break
    if r is None or r % 2 != 0:
        return None
    x = pow(a, r // 2, N)
    if x == 1 or x == N - 1:
        return None
    factor1 = gcd(x - 1, N)
    factor2 = gcd(x + 1, N)
    if factor1 * factor2 == N:
        return [factor1, factor2]
    else:
        return None

# For visualization
def simulate_multiple_Ns(N_values, runs):
    result_dict = {}
    for N in N_values:
        attempts = []
        for _ in range(runs):
            for i in range(1, 100):  # Max 100 tries
                result = shor_classical_sim(N)
                if result:
                    attempts.append(i)
                    break
        result_dict[N] = attempts
    return result_dict

# Streamlit UI
st.set_page_config(page_title="Quantum vs RSA Demo", layout="centered")
st.title("RSA Encryption & Shor's Algorithm")

# RSA Encryption/Decryption Section
st.header("🔏 RSA Encryption & Decryption")
message = st.text_input("Enter a message for encryption:")
if message:
    keys = generate_rsa_keys(1024)
    public_key = keys['public_key']
    private_key = keys['private_key']

    ciphertext = rsa_encrypt(message, public_key)
    decrypted_message = rsa_decrypt(ciphertext, private_key)

    st.write("### RSA Keys")
    st.write(f"Public Key: {public_key}")
    st.write(f"Private Key: {private_key}")
    st.write(f"Encrypted (Ciphertext): {ciphertext}")
    st.write(f"Decrypted Message: {decrypted_message}")

# Shor’s Algorithm Section
st.header("Shor's Algorithm (Classical Simulation)")

st.markdown(
    "Simulate factoring a number `N` (like an RSA modulus) using a simplified classical version "
    "of **Shor’s Algorithm**. This shows how quantum computers could one day break RSA."
)

N = st.number_input("Enter a number (N) to factor:", min_value=3, step=1)

if st.button("Simulate Shor’s Algorithm"):
    with st.spinner("Factoring..."):
        factors = shor_classical_sim(N)
        if factors:
            st.success(f"Factors of {N} found: {factors}")
            st.markdown(" This means the RSA modulus could be broken if N = p × q!")
        else:
            st.error(" Failed to find factors using this simulation. Try another number.")

# Visualization Section
st.header("📊 Shor's Algorithm: Compare Factoring Across Multiple N")

st.markdown(
    "Run the Shor's simulation on multiple numbers and see how many attempts it typically takes to factor each."
)

N_values_str = st.text_input("Enter comma-separated values of N (e.g., 15, 21, 33):", value="15,21,33")
runs = st.slider("Number of simulations per N:", 10, 300, 100)

if st.button("Generate Side-by-Side Plots"):
    try:
        N_list = [int(n.strip()) for n in N_values_str.split(",") if int(n.strip()) >= 3]
        with st.spinner("Running simulations..."):
            result_data = simulate_multiple_Ns(N_list, runs)

        cols = 2
        rows = (len(N_list) + 1) // cols
        fig = sp.make_subplots(rows=rows, cols=cols, subplot_titles=[f"N = {n}" for n in N_list])

        for idx, N in enumerate(N_list):
            row = (idx // cols) + 1
            col = (idx % cols) + 1
            attempt_counts = {}
            for attempt in result_data[N]:
                attempt_counts[attempt] = attempt_counts.get(attempt, 0) + 1

            fig.add_trace(
                go.Bar(x=list(attempt_counts.keys()), y=list(attempt_counts.values()), name=f"N = {N}"),
                row=row, col=col
            )

        fig.update_layout(
            height=350 * rows,
            width=900,
            title_text=f"Shor’s Algorithm: Attempts to Factor Each N (over {runs} simulations)",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

        for N in N_list:
            avg_attempts = round(sum(result_data[N]) / len(result_data[N]), 2) if result_data[N] else "N/A"
            st.markdown(f"**N = {N}:** Avg attempts to factor = `{avg_attempts}` out of {runs} runs")


            # Explanation of average attempts based on results
            if avg_attempts != "N/A":
                if avg_attempts < 10:
                    st.markdown(
                        f"""
                        ### Analysis for N = {N}
                        The **average attempts** of `{avg_attempts}` indicate that Shor's algorithm (or its classical approximation) was able to factor `N` relatively quickly in most simulations. 
                        This suggests that the number `N` is less complex to factor, and in a quantum computing environment, Shor's algorithm could efficiently break it with fewer resources.
                        """
                    )
                elif avg_attempts < 50:
                    st.markdown(
                        f"""
                        ### Insights for N = {N}
                        The **average attempts** of `{avg_attempts}` indicates that it took a moderate number of tries to successfully factor `N`. 
                        This suggests that the number `N` is moderately complex and might require more computational effort to factor with Shor's algorithm.
                        """
                    )
                else:
                    st.markdown(
                        f"""
                        ### Insights for N = {N}
                        The **average attempts** of `{avg_attempts}` suggests that `N` is challenging to factor in most runs. 
                        This means `N` is likely a difficult number for Shor's algorithm, and it would require a significant amount of computational resources to break in a quantum setting.
                        """
                    )

    except ValueError:
        st.error("Please enter valid integers separated by commas.")
