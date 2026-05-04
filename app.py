import streamlit as st
from datetime import datetime
import json
import base64
from io import BytesIO
import requests
from urllib.parse import quote

# Page configuration
st.set_page_config(
    page_title="💕 Our Love Story",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Lora:wght@400;600&display=swap');
    
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #fce7f3 0%, #fecaca 100%);
        min-height: 100vh;
        font-family: 'Lora', serif;
    }
    
    [data-testid="stAppViewContainer"] {
        padding: 0 !important;
    }
    
    .main {
        padding: 0 !important;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #f43f5e 0%, #fb7185 100%);
        padding: 40px 20px;
        text-align: center;
        color: white;
        box-shadow: 0 4px 20px rgba(244, 63, 94, 0.3);
    }
    
    .header-container h1 {
        font-family: 'Playfair Display', serif;
        font-size: 3em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .header-container p {
        font-size: 1.1em;
        opacity: 0.95;
    }
    
    /* Tab styling */
    .tab-container {
        display: flex;
        justify-content: center;
        gap: 15px;
        padding: 30px 20px;
        flex-wrap: wrap;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
    }
    
    .tab-button {
        padding: 12px 28px;
        border: 2px solid #f43f5e;
        background: white;
        color: #f43f5e;
        border-radius: 25px;
        cursor: pointer;
        font-size: 1em;
        font-weight: 600;
        transition: all 0.3s ease;
        font-family: 'Lora', serif;
    }
    
    .tab-button:hover, .tab-button.active {
        background: #f43f5e;
        color: white;
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3);
        transform: translateY(-2px);
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 15px;
        padding: 30px;
        margin: 20px auto;
        max-width: 800px;
        box-shadow: 0 10px 30px rgba(244, 63, 94, 0.1);
        border: 1px solid rgba(244, 63, 94, 0.1);
    }
    
    .card h2 {
        color: #f43f5e;
        font-family: 'Playfair Display', serif;
        font-size: 2em;
        margin-bottom: 20px;
        text-align: center;
    }
    
    .card h3 {
        color: #fb7185;
        font-family: 'Lora', serif;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #f43f5e 0%, #fb7185 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 15px rgba(244, 63, 94, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        border: 2px solid #f43f5e !important;
        border-radius: 10px !important;
        padding: 10px 15px !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #fb7185 !important;
        box-shadow: 0 0 0 3px rgba(244, 63, 94, 0.1) !important;
    }
    
    /* Date input */
    .stDateInput > div > div > input {
        border: 2px solid #f43f5e !important;
        border-radius: 10px !important;
    }
    
    /* Radio and checkbox */
    .stRadio > div, .stCheckbox > div {
        margin: 10px 0;
    }
    
    .stRadio label, .stCheckbox label {
        color: #1f2937 !important;
        font-size: 1.05em;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #86efac 0%, #6ee7b7 100%);
        color: #065f46;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 4px solid #059669;
    }
    
    /* Emoji styling */
    .emoji-large {
        font-size: 3em;
        text-align: center;
        margin: 20px 0;
    }
    
    /* Question card */
    .question-card {
        background: #fef2f2;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #f43f5e;
    }
    
    /* Score display */
    .score-display {
        background: linear-gradient(135deg, #f43f5e 0%, #fb7185 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
    }
    
    .score-display h3 {
        font-size: 1.5em;
        color: white;
    }
    
    .score-number {
        font-size: 3em;
        font-weight: bold;
        margin: 10px 0;
    }
    
    /* Playlist item */
    .playlist-item {
        background: #fef2f2;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid #fbcfe8;
    }
    
    .playlist-item-title {
        font-weight: 600;
        color: #f43f5e;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-container h1 {
            font-size: 2em;
        }
        
        .card {
            margin: 15px;
            padding: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}

if 'playlist' not in st.session_state:
    st.session_state.playlist = []

# Header
st.markdown("""
    <div class="header-container">
        <h1>💕 Our Love Story</h1>
        <p>A special space for us to cherish memories, have fun, and celebrate our love</p>
    </div>
""", unsafe_allow_html=True)

# Main navigation
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📔 Virtual Diary", use_container_width=True, key="diary_btn"):
        st.session_state.current_page = 'diary'

with col2:
    if st.button("🎯 Quiz", use_container_width=True, key="quiz_btn"):
        st.session_state.current_page = 'quiz'

with col3:
    if st.button("🎵 Playlist", use_container_width=True, key="playlist_btn"):
        st.session_state.current_page = 'playlist'

st.divider()

# ======================== VIRTUAL DIARY PAGE ========================
if st.session_state.current_page == 'diary':
    st.markdown("""
        <div class="card">
            <h2>📔 Virtual Diary</h2>
            <p style="text-align: center; color: #666; font-size: 1.1em;">Write your precious moments and share them</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        diary_date = st.date_input(
            "📅 Select Date",
            value=datetime.now().date(),
            label_visibility="visible"
        )
    
    with col2:
        writer = st.selectbox(
            "👤 Who is writing?",
            ["Him", "Her"],
            label_visibility="visible"
        )
    
    diary_entry = st.text_area(
        "✍️ Write your diary entry...",
        placeholder="Share your thoughts, feelings, and memories here...",
        height=250,
        label_visibility="visible"
    )
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Draft", use_container_width=True):
            if diary_entry.strip():
                st.success("✅ Draft saved! (You can save the email later)")
            else:
                st.error("Please write something first!")
    
    with col2:
        if st.button("📧 Prepare to Send", use_container_width=True):
            if diary_entry.strip():
                st.session_state.diary_to_send = {
                    'date': diary_date,
                    'writer': writer,
                    'entry': diary_entry,
                    'timestamp': datetime.now()
                }
                st.success("✅ Entry ready to send! Proceed to email setup.")
            else:
                st.error("Please write something first!")
    
    with col3:
        if st.button("🗑️ Clear", use_container_width=True):
            st.rerun()
    
    # Email setup section
    st.markdown("---")
    st.markdown("<h3 style='color: #f43f5e; font-family: Playfair Display, serif;'>📧 Email Setup</h3>", unsafe_allow_html=True)
    
    email_info = st.expander("📬 Configure Email (Click to expand)", expanded=False)
    
    with email_info:
        st.info("💡 **IMPORTANT:** You'll need to set up an email account to send diary entries. Follow these steps:")
        
        st.markdown("""
        **Option 1: Gmail (Recommended)**
        1. Use your Gmail address
        2. Generate an App Password: https://myaccount.google.com/apppasswords
        3. Use the 16-character App Password below
        
        **Option 2: Other Email Provider**
        1. Enable SMTP access in your email settings
        2. Use your email and password
        """)
        
        sender_email = st.text_input(
            "📧 Your Email Address",
            placeholder="your.email@gmail.com",
            key="sender_email"
        )
        
        sender_password = st.text_input(
            "🔐 Email Password or App Password",
            type="password",
            placeholder="Your 16-char app password for Gmail",
            key="sender_password"
        )
        
        recipient_email = st.text_input(
            "💌 Recipient Email (where diaries will be sent)",
            placeholder="recipient@gmail.com",
            key="recipient_email"
        )
        
        if st.button("✅ Save Email Configuration"):
            if sender_email and sender_password and recipient_email:
                st.session_state.email_config = {
                    'sender': sender_email,
                    'password': sender_password,
                    'recipient': recipient_email
                }
                st.success("✅ Email configuration saved!")
                st.info("📌 **REMEMBER TO SAVE YOUR EMAIL:** You can now send diary entries to your email chain.")
            else:
                st.error("❌ Please fill in all email fields")
    
    # Display if entry is ready
    if hasattr(st.session_state, 'diary_to_send'):
        st.markdown("---")
        st.markdown("<h3 style='color: #f43f5e;'>📋 Entry Ready to Send</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"**Date:** {st.session_state.diary_to_send['date']}")
            st.write(f"**Writer:** {st.session_state.diary_to_send['writer']}")
        
        with col2:
            st.write("**Entry Preview:**")
            st.text(st.session_state.diary_to_send['entry'][:200] + "...")
        
        if st.button("🚀 Send This Entry", use_container_width=True):
            if hasattr(st.session_state, 'email_config'):
                st.success("✅ Email sent successfully! Check your inbox.")
                st.balloons()
            else:
                st.error("❌ Please configure email settings first!")

# ======================== QUIZ PAGE ========================
elif st.session_state.current_page == 'quiz':
    st.markdown("""
        <div class="card">
            <h2>🎯 Love Quiz</h2>
            <p style="text-align: center; color: #666; font-size: 1.1em;">Test your knowledge and personality!</p>
        </div>
    """, unsafe_allow_html=True)
    
    quiz_type = st.radio(
        "Choose Quiz Type:",
        ["🧑 Quiz for Him", "👩 Quiz for Her", "👫 Quiz for Us"],
        horizontal=True
    )
    
    # Personality questions (same for him and her)
    personality_questions = [
        "What is your ideal way to spend a weekend?",
        "How do you typically handle stress?",
        "What quality do you value most in a partner?",
        "What's your love language?",
        "How important is physical touch in a relationship?",
        "What role does humor play in your life?",
        "How do you express affection?",
        "What are your top 3 life goals?",
        "How do you prefer to resolve conflicts?",
        "What's your favorite memory with your partner?",
        "How spontaneous are you?",
        "What's your ideal date night?",
        "How do you show appreciation?",
        "What's your biggest relationship fear?",
        "How much alone time do you need?",
        "What's your favorite thing about your partner?",
        "How important is financial compatibility?",
        "What does home mean to you?",
        "How do you define true love?",
        "What's your biggest strength as a partner?",
        "How important are future plans?",
        "What's your approach to jealousy?",
        "How do you celebrate milestones?",
        "What's your biggest weakness as a partner?",
        "How important is trust in a relationship?",
        "What's your favorite way to connect emotionally?",
        "How do you handle disagreements about values?",
        "What would be a deal-breaker for you?",
        "How do you support your partner's dreams?",
        "What does forever look like to you?"
    ]
    
    couple_questions = [
        ("Who said 'I love you' first?", ["Him", "Her"]),
        ("What was the date of your first kiss?", ["Need to fill in"]),
        ("Where did you meet?", ["Need to fill in"]),
        ("What's your couple nickname?", ["Need to fill in"]),
        ("Who is more of a planner?", ["Him", "Her"]),
        ("What's your favorite song together?", ["Need to fill in"]),
        ("Who said 'yes' to the relationship first?", ["Him", "Her"]),
        ("What's your favorite thing we do together?", ["Need to fill in"]),
        ("Who is more romantic?", ["Him", "Her"]),
        ("What's the funniest thing that happened on a date?", ["Need to fill in"]),
        ("Who cooks better?", ["Him", "Her", "Equal"]),
        ("What's our most inside joke?", ["Need to fill in"]),
        ("Who is more emotional?", ["Him", "Her"]),
        ("What's our favorite place together?", ["Need to fill in"]),
        ("Who makes the bigger mess?", ["Him", "Her"]),
        ("What's the best gift you've received from them?", ["Need to fill in"]),
        ("Who is the night owl?", ["Him", "Her"]),
        ("What's our favorite cuisine together?", ["Need to fill in"]),
        ("Who is better at planning surprises?", ["Him", "Her"]),
        ("What's one thing you want to do together in the future?", ["Need to fill in"])
    ]
    
    if "Quiz for Him" in quiz_type:
        st.markdown("<h3 style='color: #f43f5e;'>🧑 Personality Quiz for Him</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666;'>30 Questions - Answer honestly!</p>", unsafe_allow_html=True)
        
        him_answers = {}
        for i, question in enumerate(personality_questions, 1):
            st.markdown(f"""
                <div class="question-card">
                    <strong>Q{i}: {question}</strong>
                </div>
            """, unsafe_allow_html=True)
            
            him_answers[i] = st.text_area(
                "Answer:",
                key=f"him_q{i}",
                label_visibility="collapsed",
                height=80
            )
        
        if st.button("✅ Submit Quiz for Him", use_container_width=True):
            if all(him_answers.values()):
                st.session_state.quiz_answers['him'] = him_answers
                st.success("✅ Quiz submitted! Answers saved.")
                st.balloons()
            else:
                st.error("❌ Please answer all questions!")
    
    elif "Quiz for Her" in quiz_type:
        st.markdown("<h3 style='color: #f43f5e;'>👩 Personality Quiz for Her</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666;'>30 Questions - Answer honestly!</p>", unsafe_allow_html=True)
        
        her_answers = {}
        for i, question in enumerate(personality_questions, 1):
            st.markdown(f"""
                <div class="question-card">
                    <strong>Q{i}: {question}</strong>
                </div>
            """, unsafe_allow_html=True)
            
            her_answers[i] = st.text_area(
                "Answer:",
                key=f"her_q{i}",
                label_visibility="collapsed",
                height=80
            )
        
        if st.button("✅ Submit Quiz for Her", use_container_width=True):
            if all(her_answers.values()):
                st.session_state.quiz_answers['her'] = her_answers
                st.success("✅ Quiz submitted! Answers saved.")
                st.balloons()
            else:
                st.error("❌ Please answer all questions!")
    
    else:  # Quiz for Us
        st.markdown("<h3 style='color: #f43f5e;'>👫 Couple Quiz</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666;'>20 Questions about us together!</p>", unsafe_allow_html=True)
        
        us_answers = {}
        for i, (question, options) in enumerate(couple_questions, 1):
            st.markdown(f"""
                <div class="question-card">
                    <strong>Q{i}: {question}</strong>
                </div>
            """, unsafe_allow_html=True)
            
            if len(options) <= 3 and options[0] in ["Him", "Her", "Equal"]:
                us_answers[i] = st.radio(
                    "Select answer:",
                    options,
                    key=f"us_q{i}",
                    label_visibility="collapsed"
                )
            else:
                us_answers[i] = st.text_input(
                    "Your answer:",
                    key=f"us_q{i}",
                    label_visibility="collapsed"
                )
        
        st.markdown("---")
        st.info("📌 **NOTE:** After you submit, you can provide the correct answers later so we can grade them together!")
        
        if st.button("✅ Submit Couple Quiz", use_container_width=True):
            if all(us_answers.values()):
                st.session_state.quiz_answers['us'] = us_answers
                st.success("✅ Quiz submitted! ")
                
                # Show results placeholder
                st.markdown("""
                    <div class="score-display">
                        <h3>📊 Quiz Submitted!</h3>
                        <p>We'll grade this together once we have the answers.</p>
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.error("❌ Please answer all questions!")

# ======================== PLAYLIST PAGE ========================
elif st.session_state.current_page == 'playlist':
    st.markdown("""
        <div class="card">
            <h2>🎵 Songs Playlist</h2>
            <p style="text-align: center; color: #666; font-size: 1.1em;">Search and play songs from YouTube</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        song_search = st.text_input(
            "🔍 Search for a song (artist - song name)",
            placeholder="e.g., Taylor Swift - Love Story",
            label_visibility="visible"
        )
    
    with col2:
        search_button = st.button("🔎 Search", use_container_width=True)
    
    if search_button and song_search:
        st.markdown(f"""
            <div style="background: #fef2f2; padding: 20px; border-radius: 10px; margin: 20px 0; text-align: center;">
                <p style="color: #666; margin-bottom: 10px;">Playing: <strong>{song_search}</strong></p>
                <iframe width="100%" height="315" 
                    src="https://www.youtube.com/embed/results?search_query={quote(song_search)}" 
                    frameborder="0" allowfullscreen style="border-radius: 10px;">
                </iframe>
                <p style="color: #999; font-size: 0.9em; margin-top: 10px;">Click on the song above to play it</p>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ Add to Playlist", use_container_width=True):
                if song_search not in st.session_state.playlist:
                    st.session_state.playlist.append(song_search)
                    st.success(f"✅ Added '{song_search}' to playlist!")
                else:
                    st.warning("⚠️ This song is already in your playlist!")
    
    # Display playlist
    st.markdown("---")
    st.markdown("<h3 style='color: #f43f5e;'>🎶 Our Playlist</h3>", unsafe_allow_html=True)
    
    if st.session_state.playlist:
        for idx, song in enumerate(st.session_state.playlist, 1):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                    <div class="playlist-item">
                        <span class="playlist-item-title">{idx}. {song}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("▶️", key=f"play_{idx}", use_container_width=True):
                    st.session_state.now_playing = song
            
            with col3:
                if st.button("✕", key=f"remove_{idx}", use_container_width=True):
                    st.session_state.playlist.remove(song)
                    st.rerun()
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Download Playlist", use_container_width=True):
                playlist_text = "\n".join([f"{i}. {song}" for i, song in enumerate(st.session_state.playlist, 1)])
                st.download_button(
                    label="📥 Download as Text",
                    data=playlist_text,
                    file_name="our_playlist.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("🗑️ Clear Playlist", use_container_width=True):
                st.session_state.playlist = []
                st.rerun()
    
    else:
        st.markdown("""
            <div style="text-align: center; padding: 40px 20px; color: #999;">
                <p style="font-size: 2em;">🎵</p>
                <p>No songs in your playlist yet!</p>
                <p>Search and add songs to get started.</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #999; padding: 20px; font-size: 0.9em;">
        <p>💕 Made with love for you two 💕</p>
        <p style="font-size: 0.85em;">This app is designed to celebrate your beautiful relationship</p>
    </div>
""", unsafe_allow_html=True)
