import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(page_title="💕 Love Quiz Challenge", page_icon="💕", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stage-header { text-align: center; color: #f43f5e; font-size: 2em; margin: 1em 0; }
    .question-box { background: #f0f2f6; padding: 1.5em; border-radius: 10px; margin: 1em 0; }
    .correct { color: #28a745; font-weight: bold; }
    .incorrect { color: #dc3545; font-weight: bold; }
    .surprise-box { background: #fff3cd; padding: 2em; border-radius: 10px; text-align: center; margin: 2em 0; }
    .celebration { text-align: center; font-size: 3em; margin: 1em 0; }
    .love-you { text-align: center; color: #f43f5e; font-size: 3em; margin: 2em 0; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 1
if 'stage_answers' not in st.session_state:
    st.session_state.stage_answers = {}
if 'show_results' not in st.session_state:
    st.session_state.show_results = False
if 'show_surprise' not in st.session_state:
    st.session_state.show_surprise = False

# Quiz Questions with MCQ options (30 total - 5 per stage)
questions = [
    # Stage 1
    {
        "q": "What's her go-to comfort food when she's sad?",
        "options": ["Chocolates", "Ice Cream", "Pizza", "Cake"],
        "ans": "Chocolates"
    },
    {
        "q": "Which movie/show has she watched the most times?",
        "options": ["Saiyara", "Darlings", "Badhaai Do", "Queen"],
        "ans": "Saiyara"
    },
    {
        "q": "What does she do first thing in the morning?",
        "options": ["Morning Prayer", "Check Phone", "Drink Water", "Exercise"],
        "ans": "Morning Prayer"
    },
    {
        "q": "Her most used emoji?",
        "options": ["Laughing", "Heart", "Thinking", "Wink"],
        "ans": "Laughing"
    },
    {
        "q": "What's her favorite way to spend time with family?",
        "options": ["Gossiping", "Cooking", "Movies", "Shopping"],
        "ans": "Gossiping"
    },
    
    # Stage 2
    {
        "q": "What's her dream job/career?",
        "options": ["Financial Analyst", "Doctor", "Teacher", "Engineer"],
        "ans": "Financial Analyst"
    },
    {
        "q": "Which celebrity does she have a crush on?",
        "options": ["Abhishek Sharma", "Ranbir Kapoor", "Aditya Roy Kapur", "Hrithik Roshan"],
        "ans": "Abhishek Sharma"
    },
    {
        "q": "What's her biggest insecurity?",
        "options": ["Weight", "Appearance", "Intelligence", "Social Skills"],
        "ans": "Weight"
    },
    {
        "q": "What does she spend most time on her phone doing?",
        "options": ["Scrolling", "Gaming", "Chatting", "Watching Videos"],
        "ans": "Scrolling"
    },
    {
        "q": "Her favorite thing about herself?",
        "options": ["Knowledge", "Humor", "Kindness", "Creativity"],
        "ans": "Knowledge"
    },
    
    # Stage 3
    {
        "q": "What was her childhood dream?",
        "options": ["Travel", "Become a Doctor", "Write a Book", "Become a Singer"],
        "ans": "Travel"
    },
    {
        "q": "Her favorite memory with you?",
        "options": ["Noida", "First Date", "First Kiss", "Vacation"],
        "ans": "Noida"
    },
    {
        "q": "What makes her cry (emotionally)?",
        "options": ["Sad Movies", "Emotional Moments", "Family Issues", "Subjective"],
        "ans": "Subjective"
    },
    {
        "q": "Her most embarrassing habit?",
        "options": ["Burp", "Snoring", "Talking to Self", "Laughing Loudly"],
        "ans": "Burp"
    },
    {
        "q": "What's one thing she always nags you about?",
        "options": ["Cleanliness", "Time Management", "Money Spending", "Phone Usage"],
        "ans": "Cleanliness"
    },
    
    # Stage 4
    {
        "q": "What's the first thing she noticed about you?",
        "options": ["Nothing", "Smile", "Eyes", "Personality"],
        "ans": "Nothing"
    },
    {
        "q": "Her biggest relationship fear?",
        "options": ["Breakup", "Cheating", "Distance", "Misunderstanding"],
        "ans": "Breakup"
    },
    {
        "q": "What song reminds her of you?",
        "options": ["Sang Rahiyo", "Tum Hi Ho", "Aashiquui", "Agar Tum Saath Ho"],
        "ans": "Sang Rahiyo"
    },
    {
        "q": "Her secret talent nobody knows?",
        "options": ["Dancing", "Singing", "Drawing", "Subjective"],
        "ans": "Subjective"
    },
    {
        "q": "What's her love language?",
        "options": ["Physical and Emotional", "Words of Affirmation", "Quality Time", "Gifts"],
        "ans": "Physical and Emotional"
    },
    
    # Stage 5
    {
        "q": "What did she say the first time she realized she loved you?",
        "options": ["Nothing", "I Love You", "You Mean Everything", "Forever"],
        "ans": "Nothing"
    },
    {
        "q": "Her biggest dream for your future together?",
        "options": ["House, Car, Travel and Money", "Just Be Together", "Get Married", "Have Kids"],
        "ans": "House, Car, Travel and Money"
    },
    {
        "q": "What's the sweetest thing you've done for her?",
        "options": ["Caring Me", "Surprise Gift", "Special Date", "Love Letter"],
        "ans": "Caring Me"
    },
    {
        "q": "Her favorite nickname for you?",
        "options": ["V", "Baby", "Jaan", "Love"],
        "ans": "V"
    },
    {
        "q": "What does she value most in your relationship?",
        "options": ["Love", "Trust", "Respect", "Honesty"],
        "ans": "Love"
    },
    
    # Stage 6
    {
        "q": "What's her biggest fear about losing you?",
        "options": ["Living Without You", "Being Alone", "Finding Someone Else", "Starting Over"],
        "ans": "Living Without You"
    },
    {
        "q": "The exact date of your first kiss?",
        "options": ["May", "June", "July", "August"],
        "ans": "May"
    },
    {
        "q": "What's the most romantic thing you've said to her?",
        "options": ["I Want To Have Family With You", "I Love You", "You're My Everything", "Forever Mine"],
        "ans": "I Want To Have Family With You"
    },
    {
        "q": "Her favorite position to cuddle with you?",
        "options": ["Spoon", "Face to Face", "Spooning Reverse", "Hugging"],
        "ans": "Spoon"
    },
    {
        "q": "What's the one promise you made to her that you always keep?",
        "options": ["Always Be There For Her", "Never Lie", "Always Support", "Always Love"],
        "ans": "Always Be There For Her"
    },
]

# Surprises for each stage
surprises = {
    1: "🎤 I'll sing a song for you",
    2: "🎁 I'll buy you one thing you say",
    3: "👑 I'll obey one thing you say",
    4: "✨ I'll wear something special you've always wanted",
    5: "✈️ I'll take you on a surprise trip",
    6: "🌟 I'll do anything you want right now"
}

# Header
st.markdown("<h1 style='text-align: center; color: #f43f5e;'>💕 Love Quiz Challenge 💕</h1>", unsafe_allow_html=True)
st.markdown("---")

# Get current stage questions
stage_start = (st.session_state.current_stage - 1) * 5
stage_end = stage_start + 5
stage_questions = questions[stage_start:stage_end]

# Display stage header
st.markdown(f"<div class='stage-header'>⭐ STAGE {st.session_state.current_stage} / 6</div>", unsafe_allow_html=True)

if not st.session_state.show_results:
    st.markdown(f"<h3 style='text-align: center;'>Answer all 5 questions correctly to unlock Stage {st.session_state.current_stage} Surprise! 🎉</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Display MCQ questions
    user_answers = {}
    for i, question in enumerate(stage_questions, 1):
        st.markdown(f"<div class='question-box'><b>Q{stage_start + i}: {question['q']}</b></div>", unsafe_allow_html=True)
        
        # Radio button for MCQ
        selected = st.radio(
            label=f"Select answer for Q{stage_start + i}:",
            options=question['options'],
            key=f"answer_{stage_start + i}",
            label_visibility="collapsed"
        )
        user_answers[stage_start + i] = selected
        st.write("")  # Spacing
    
    # Submit button
    if st.button("🎯 Submit Stage Answers", use_container_width=True):
        # Calculate score
        correct_count = 0
        results = []
        
        for i, question in enumerate(stage_questions, 1):
            user_ans = user_answers.get(stage_start + i, "")
            is_correct = user_ans == question['ans']
            if is_correct:
                correct_count += 1
            results.append({
                'question': question['q'],
                'correct': question['ans'],
                'user': user_ans,
                'is_correct': is_correct
            })
        
        # Store results
        st.session_state.stage_answers[st.session_state.current_stage] = {
            'correct': correct_count,
            'total': 5,
            'results': results
        }
        st.session_state.show_results = True
        st.rerun()

else:
    # Show results
    stage_data = st.session_state.stage_answers[st.session_state.current_stage]
    correct = stage_data['correct']
    total = stage_data['total']
    percentage = (correct / total) * 100
    
    st.markdown("---")
    st.markdown("<h2 style='text-align: center;'>📊 Stage Results</h2>", unsafe_allow_html=True)
    
    # Score display
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{correct}/{total}")
    with col2:
        st.metric("Percentage", f"{percentage:.0f}%")
    with col3:
        if percentage >= 60:
            st.metric("Status", "✅ PASSED")
        else:
            st.metric("Status", "❌ FAILED")
    
    st.markdown("---")
    
    # Show each answer
    st.markdown("<h3>Answer Review:</h3>", unsafe_allow_html=True)
    for i, result in enumerate(stage_data['results'], 1):
        with st.expander(f"Q{stage_start + i}: {result['question']}"):
            st.write(f"**Correct Answer:** {result['correct']}")
            st.write(f"**Your Answer:** {result['user']}")
            if result['is_correct']:
                st.markdown("<p class='correct'>✅ Correct!</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='incorrect'>❌ Incorrect</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Surprise unlock
    if percentage >= 60:
        st.markdown(f"<div class='celebration'>🎉 🎉 🎉</div>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: #28a745;'>🎊 YOU PASSED STAGE {st.session_state.current_stage}! 🎊</h2>", unsafe_allow_html=True)
        st.markdown(f"<div class='celebration'>✨ ✨ ✨</div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        if not st.session_state.show_surprise:
            if st.button(f"🎁 Tap to Reveal Your Surprise!", use_container_width=True, key="reveal_surprise"):
                st.session_state.show_surprise = True
                st.rerun()
        else:
            st.markdown(f"<div class='surprise-box'><h1>{surprises[st.session_state.current_stage]}</h1></div>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Next stage button
        if st.session_state.current_stage < 6:
            if st.button(f"➡️ Go to Stage {st.session_state.current_stage + 1}", use_container_width=True):
                st.session_state.current_stage += 1
                st.session_state.show_results = False
                st.session_state.show_surprise = False
                st.rerun()
        else:
            # Final stage - show I Love You
            st.markdown("<div class='love-you'>💕 I LOVE YOU 💕</div>", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: #f43f5e;'>🏆 YOU COMPLETED ALL 6 STAGES! 🏆</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 1.5em; color: #f43f5e;'>You're an absolute legend! 💕</p>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 1.2em;'>This quiz proves how much you know me... and how much you love me! ❤️</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='text-align: center; color: #dc3545;'>😢 You got {correct}/5 ({percentage:.0f}%)</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>You need 60% (3 out of 5) to unlock the surprise and move to the next stage!</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        if st.button(f"🔄 Retry Stage {st.session_state.current_stage}", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.show_surprise = False
            st.rerun()

st.markdown("---")
st.markdown("<p style='text-align: center; color: #999;'>Made with love 💕</p>", unsafe_allow_html=True)
