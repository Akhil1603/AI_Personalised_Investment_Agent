import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini

st.set_page_config(
    page_title="🤑 AI Investment Agent",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 2rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #f0f4ff, #d0e1ff);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3.5em;
        font-weight: bold;
        background-color: #0052cc;
        color: white;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #003d99;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e6ffed;
        border: 1px solid #6fcf97;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff6e6;
        border: 1px solid #f0b429;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.2rem;
        font-weight: 700;
        color: #004080;
    }
    .sidebar .stTextInput>div>input {
        border-radius: 8px;
        border: 1px solid #004080;
        padding: 0.4em;
    }
    </style>
""", unsafe_allow_html=True)

def display_investment_plan(plan_content):
    with st.expander("📈 Your Personalized Investment Plan", expanded=True):
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 🎯 Why this plan is a money magnet")
            st.success(plan_content.get("why_this_plan_works", "Our AI says it's solid!"))
            st.markdown("### 💼 Investment Strategy")
            st.write(plan_content.get("strategy", "Strategy coming soon..."))

        with col2:
            st.markdown("### ⚠️ Investor’s fine print")
            considerations = plan_content.get("important_considerations", "").split('\n')
            for consideration in considerations:
                if consideration.strip():
                    st.warning(consideration)

def main():
    if 'investment_plan' not in st.session_state:
        st.session_state.investment_plan = {}
        st.session_state.qa_pairs = []
        st.session_state.plan_generated = False

    st.title("💸 AI Investment Agent")
    st.markdown("""
        <div style='background-color: #004080; color: white; padding: 1rem; border-radius: 0.75rem; margin-bottom: 2rem;'>
        Ready to make your money work as hard as you do? Tell me about your financial dreams and fears,
        and I’ll craft an investment plan with a pinch of AI magic and a splash of humor. Let's grow those bucks! 💰✨
        </div>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.header("🔑 API Setup")
        gemini_api_key = st.text_input(
            "Enter your Gemini API Key",
            type="password",
            help="Get your Gemini API key from https://aistudio.google.com/apikey"
        )
        if not gemini_api_key:
            st.warning("Please enter your Gemini API Key to proceed")
            return
        st.success("API key loaded — ready to roll!")

    if gemini_api_key:
        try:
            gemini_model = Gemini(id="gemini-1.5-flash", api_key=gemini_api_key)
        except Exception as e:
            st.error(f"❌ Failed to initialize Gemini model: {e}")
            return

        with st.form(key="investment_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input(
                    "Your Age 🎂", min_value=18, max_value=100, step=1,
                    help="Age matters — we’re not investing in dinosaur bones!"
                )
                investment_amount = st.number_input(
                    "Investment Amount (USD) 💰", min_value=100.0, max_value=1_000_000.0, step=100.0,
                    help="How much dough are we working with?"
                )
                risk_tolerance = st.selectbox(
                    "Risk Tolerance 🎢",
                    options=["Low (I’m a cautious turtle 🐢)", "Moderate (Balanced owl 🦉)", "High (Fearless lion 🦁)"],
                    help="How brave are you feeling about investments?"
                )
                investment_horizon = st.selectbox(
                    "Investment Horizon ⏳",
                    options=["Short-term (0-3 years) ⏰", "Medium-term (3-7 years) 📅", "Long-term (7+ years) 🌳"],
                    help="How long can your money chill in the market?"
                )
            with col2:
                financial_goals = st.text_area(
                    "Financial Goals 🎯",
                    placeholder="e.g., Buy a spaceship, retire early, become a crypto whale...",
                    help="Dream big or small, I’m listening!"
                )
                experience_level = st.selectbox(
                    "Investment Experience Level 📚",
                    options=["Beginner (Baby steps 👶)", "Intermediate (Steady swimmer 🏊)", "Experienced (Market shark 🦈)"],
                    help="Your investing street cred"
                )
                preferred_investment_types = st.multiselect(
                    "Preferred Investment Types 🧺",
                    options=["Stocks 📈", "Bonds 💵", "Mutual Funds 🎯", "ETFs 🧩", "Real Estate 🏠", "Cryptocurrency 🪙", "Other 🤷"],
                    help="Pick your favorites, or all if you’re a daredevil!"
                )

            submit_button = st.form_submit_button(label="💥 Show me the money plan!")

        if submit_button:
            with st.spinner("Crunching numbers and brewing your investment potion..."):
                try:
                    investment_agent = Agent(
                        name="Investment Guru",
                        role="Creates personalized investment plans",
                        model=gemini_model,
                        instructions=[
                            "Use the user's profile and preferences to create a detailed investment plan.",
                            "Explain why the plan fits the user's risk tolerance, goals, and horizon.",
                            "Make the explanation fun but informative and clear.",
                        ]
                    )

                    user_profile = f"""
                    Age: {age}
                    Investment Amount: ${investment_amount:,.2f}
                    Risk Tolerance: {risk_tolerance}
                    Investment Horizon: {investment_horizon}
                    Financial Goals: {financial_goals}
                    Experience Level: {experience_level}
                    Preferred Investment Types: {', '.join(preferred_investment_types) if preferred_investment_types else 'None specified'}
                    """

                    plan_response = investment_agent.run(user_profile)

                    investment_plan = {
                        "why_this_plan_works": "Tailored to your profile to maximize returns while keeping risks in check!",
                        "strategy": plan_response.content,
                        "important_considerations": """
                        - Markets can be unpredictable — always diversify!
                        - Past performance is not a crystal ball.
                        - Keep calm and invest on, even when the market rumbles.
                        - Review your portfolio at least once a year.
                        """
                    }

                    st.session_state.investment_plan = investment_plan
                    st.session_state.plan_generated = True
                    st.session_state.qa_pairs = []

                    display_investment_plan(investment_plan)

                except Exception as e:
                    st.error(f"😵‍💫 Uh-oh, something broke: {e}")

        if st.session_state.plan_generated:
            st.header("❓ Got questions about your plan? Ask away!")
            question_input = st.text_input("What’s puzzling you about your money moves?")

            if st.button("Get Answer"):
                if question_input:
                    with st.spinner("Consulting the wise investment oracle..."):
                        context = st.session_state.investment_plan.get("strategy", "")
                        full_context = f"Investment Plan: {context}\nUser Question: {question_input}"
                        try:
                            agent = Agent(model=gemini_model, show_tool_calls=True, markdown=True)
                            run_response = agent.run(full_context)

                            answer = getattr(run_response, 'content', "Hmm, I got no answer for that right now.")
                            st.session_state.qa_pairs.append((question_input, answer))
                        except Exception as e:
                            st.error(f"⚠️ Oops, couldn't fetch answer: {e}")

            if st.session_state.qa_pairs:
                st.header("💬 Your Q&A History")
                for q, a in st.session_state.qa_pairs:
                    st.markdown(f"**Q:** {q}")
                    st.markdown(f"**A:** {a}")

if __name__ == "__main__":
    main()
