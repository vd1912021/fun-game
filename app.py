import streamlit as st
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Page config
st.set_page_config(page_title="Our Love Story", page_icon="💕", layout="wide")

st.markdown("<h1 style='text-align: center; color: #f43f5e;'>💕 Our Love Story 💕</h1>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if 'diary_entries' not in st.session_state:
    st.session_state.diary_entries = []

if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = []

if 'playlist' not in st.session_state:
    st.session_state.playlist = []

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📔 Diary", "🎯 Quiz", "🎵 Playlist", "⚙️ Settings"])

# ==================== DIARY TAB ====================
with tab1:
    st.header("💝 Couple's Diary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entry_date = st.date_input("Select date")
    
    with col2:
        who_writing = st.selectbox("Who is writing?", ["Me", "My Love", "Both"])
    
    entry_text = st.text_area("Write your memory...", height=200, key="diary_text")
    
    if st.button("📝 Save Entry", use_container_width=True):
        if entry_text.strip():
            entry = {
                'date': str(entry_date),
                'who': who_writing,
                'text': entry_text,
                'time': datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.diary_entries.append(entry)
            st.success("✅ Entry saved!")
        else:
            st.warning("Please write something!")
    
    # Display entries
    if st.session_state.diary_entries:
        st.subheader("📚 Past Memories")
        for i, entry in enumerate(reversed(st.session_state.diary_entries)):
            with st.expander(f"📅 {entry['date']} - {entry['who']}"):
                st.write(entry['text'])
                
                # Email button for each entry
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button(f"📧 Email", key=f"email_{i}"):
                        st.session_state.selected_entry = entry
                        st.session_state.show_email_form = True

    # Email form
    st.markdown("---")
    st.subheader("📬 Send Diary via Email")
    
    with st.form("email_config_form"):
        st.info("⚠️ IMPORTANT: Use Gmail App Password, NOT your regular password!")
        st.markdown("""
        **Steps to get App Password:**
        1. Go to https://myaccount.google.com/apppasswords
        2. Select Mail → Windows Device
        3. Copy the 16-character password
        4. Paste it below
        """)
        
        sender_email = st.text_input("Your Gmail address", placeholder="example@gmail.com")
        app_password = st.text_input("16-char App Password", type="password", placeholder="xxxx xxxx xxxx xxxx")
        recipient_email = st.text_input("Recipient email", placeholder="boyfriend@example.com")
        
        submit_button = st.form_submit_button("📧 Send Latest Diary Entry")
        
        if submit_button:
            if not sender_email or not app_password or not recipient_email:
                st.error("Please fill in all fields!")
            elif not st.session_state.diary_entries:
                st.error("No diary entries to send!")
            else:
                try:
                    latest_entry = st.session_state.diary_entries[-1]
                    
                    # Create email
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = recipient_email
                    msg['Subject'] = f"💕 Our Love Story - Diary Entry ({latest_entry['date']})"
                    
                    body = f"""
Dear Love,

I want to share this special memory with you:

📅 Date: {latest_entry['date']}
✍️ From: {latest_entry['who']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{latest_entry['text']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

With all my love,
Your Forever Partner 💕
                    """
                    
                    msg.attach(MIMEText(body, 'plain'))
                    
                    # Send via Gmail
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, app_password)
                    server.send_message(msg)
                    server.quit()
                    
                    st.success("✅ Email sent successfully! Check your inbox!")
                    
                except smtplib.SMTPAuthenticationError:
                    st.error("❌ Wrong email or app password! Check your Gmail credentials.")
                except smtplib.SMTPException as e:
                    st.error(f"❌ Email error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ==================== QUIZ TAB ====================
with tab2:
    st.header("🎯 Love Quiz")
    
    quiz_type = st.selectbox("Choose quiz", ["About Him", "About Her", "About Us"])
    
    quizzes = {
        "About Him": [
            {"q": "Favorite food?", "opts": ["Pizza", "Sushi", "Burger", "Pasta"]},
            {"q": "Dream vacation?", "opts": ["Beach", "Mountains", "City", "Countryside"]},
            {"q": "Favorite color?", "opts": ["Blue", "Black", "Red", "Green"]},
            {"q": "Favorite sport?", "opts": ["Football", "Basketball", "Cricket", "Tennis"]},
            {"q": "Movie genre?", "opts": ["Action", "Comedy", "Romance", "Drama"]},
        ],
        "About Her": [
            {"q": "Favorite food?", "opts": ["Pizza", "Sushi", "Burger", "Pasta"]},
            {"q": "Dream vacation?", "opts": ["Beach", "Mountains", "City", "Countryside"]},
            {"q": "Favorite color?", "opts": ["Blue", "Pink", "Red", "Green"]},
            {"q": "Hobby?", "opts": ["Reading", "Painting", "Dancing", "Singing"]},
            {"q": "Movie genre?", "opts": ["Action", "Comedy", "Romance", "Drama"]},
        ],
        "About Us": [
            {"q": "Where did we meet?", "opts": ["School", "College", "Work", "Online"]},
            {"q": "Our favorite activity?", "opts": ["Travel", "Movies", "Cooking", "Hiking"]},
            {"q": "Our song?", "opts": ["Romantic", "Upbeat", "Slow", "Popular"]},
            {"q": "When is anniversary?", "opts": ["January", "March", "July", "November"]},
            {"q": "Favorite restaurant?", "opts": ["Italian", "Indian", "Chinese", "Thai"]},
        ]
    }
    
    st.markdown("---")
    
    answers = []
    for i, item in enumerate(quizzes[quiz_type], 1):
        st.write(f"**Q{i}: {item['q']}**")
        ans = st.radio("Select", item['opts'], key=f"q_{quiz_type}_{i}")
        answers.append(ans)
    
    if st.button("🎯 Submit Quiz", use_container_width=True):
        score = len(answers)
        result = {
            'type': quiz_type,
            'score': score,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        st.session_state.quiz_scores.append(result)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Score", f"{score}/{len(answers)}")
        with col2:
            st.metric("Percentage", f"{(score/len(answers))*100:.0f}%")
        with col3:
            st.metric("Quiz", quiz_type)

# ==================== PLAYLIST TAB ====================
with tab3:
    st.header("🎵 Our Playlist")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        song = st.text_input("Song name (Artist - Song)")
    
    with col2:
        if st.button("➕ Add"):
            if song.strip():
                st.session_state.playlist.append({
                    'name': song,
                    'date': datetime.now().strftime("%Y-%m-%d")
                })
                st.success("Added!")
            else:
                st.warning("Enter song!")
    
    st.markdown("---")
    
    if st.session_state.playlist:
        st.subheader(f"🎶 Songs ({len(st.session_state.playlist)})")
        for i, s in enumerate(st.session_state.playlist, 1):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{i}. {s['name']}")
            with col2:
                if st.button("❌", key=f"del_{i}"):
                    st.session_state.playlist.pop(i-1)
                    st.rerun()
    else:
        st.info("No songs yet! Add your favorites 🎵")

# ==================== SETTINGS TAB ====================
with tab4:
    st.header("⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Stats")
        st.metric("Diary Entries", len(st.session_state.diary_entries))
        st.metric("Quizzes", len(st.session_state.quiz_scores))
        st.metric("Playlist Songs", len(st.session_state.playlist))
    
    with col2:
        st.subheader("Data")
        if st.button("🗑️ Clear All"):
            st.session_state.diary_entries = []
            st.session_state.quiz_scores = []
            st.session_state.playlist = []
            st.success("Cleared!")
    
    st.markdown("---")
    st.markdown("""
    **Our Love Story App**
    
    A beautiful app for couples to:
    - 📔 Keep a shared diary
    - 🎯 Take fun quizzes about each other
    - 🎵 Build a couple's playlist
    - 💌 Send diary entries via email
    
    Made with love 💕
    """)
