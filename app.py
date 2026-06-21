
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Carbon Footprint Estimator",
    page_icon="🌍",
    layout="wide"
)


# =========================
# API
# =========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

ai_enabled = False

if API_KEY:
    try:

        genai.configure(
            api_key=API_KEY
        )

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        ai_enabled = True

    except:
        ai_enabled = False


# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp{
background:
linear-gradient(
135deg,
#01081D,
#020B33,
#060019
);
color:white;
}


/* FIX HEADER */

header{
visibility:hidden;
}

.block-container{

max-width:100%;

padding-top:1rem;

padding-left:5rem;

padding-right:5rem;

}



/* TITLE */

.title{

text-align:center;

font-size:82px;

font-weight:900;

color:#00E7FF;

text-shadow:
0 0 20px cyan,
0 0 50px cyan;

margin-bottom:10px;

}

.subtitle{

text-align:center;

font-size:26px;

color:#D4D8FF;

margin-bottom:60px;

}



/* INPUT */

label{

color:white!important;

font-size:20px;

font-weight:700;

}


.stSelectbox div{

background:#111827;

color:white;

border-radius:18px;

}


.stSlider{

padding-top:20px;

}


textarea,
input{

background:#111827!important;

color:white!important;

}



/* BUTTON */

.stButton>button{

width:380px;

height:85px;

border:none;

border-radius:25px;

font-size:24px;

font-weight:700;

color:white;

background:
linear-gradient(
90deg,
#00D4FF,
#8B5CF6
);

box-shadow:
0 0 45px cyan;

}

.stButton>button:hover{

transform:scale(1.03);

}



/* REPORT */

.report{

background:

rgba(
12,
20,
40,
0.85
);

padding:40px;

border-radius:30px;

border:

1px solid cyan;

box-shadow:

0 0 25px cyan;

font-size:18px;

}



/* METRIC */

[data-testid="metric-container"]{

background:

rgba(
0,
0,
0,
0.35
);

padding:25px;

border-radius:20px;

border:

1px solid cyan;

}

</style>
""",
unsafe_allow_html=True)


# =========================
# HEADER
# =========================

st.markdown("""
<div class='title'>
🌍 AI Carbon Footprint Estimator
</div>

<div class='subtitle'>
Track • Analyze • Improve Sustainability
</div>
""",
unsafe_allow_html=True)


# =========================
# INPUT
# =========================

c1,c2=st.columns(2)

with c1:

    transport=st.selectbox(

        "🚗 Transport",

        [

            "Walk",

            "Cycle",

            "Bus",

            "Bike",

            "Car"

        ]

    )


    electricity=st.slider(

        "⚡ Electricity",

        1,

        10,

        5

    )



with c2:

    food=st.selectbox(

        "🍔 Food",

        [

            "Vegetarian",

            "Mixed",

            "Fast Food"

        ]

    )


    plastic=st.slider(

        "🧴 Plastic",

        1,

        10,

        5

    )


st.write("")


# =========================
# BUTTON
# =========================

if st.button(

"✨ Generate Sustainability Report"

):


    score=0


    t={

        "Walk":10,

        "Cycle":15,

        "Bus":30,

        "Bike":45,

        "Car":65

    }


    f={

        "Vegetarian":10,

        "Mixed":25,

        "Fast Food":45

    }


    score+=t[transport]

    score+=f[food]

    score+=electricity*3

    score+=plastic*2


    score=min(score,100)


    if score<35:

        impact="LOW"

    elif score<70:

        impact="MEDIUM"

    else:

        impact="HIGH"



    result=f"""

# 🌍 Carbon Score

{score}/100


---

# 🔥 Impact

{impact}


---

Transport:
{transport}


Electricity:
{electricity}


Food:
{food}


Plastic:
{plastic}


---

## 🌱 Suggestions

• Walk More

• Reduce Electricity

• Use Reusable Products

• Sustainable Food

• Weekly Tracking


Estimated Reduction:

15–30%

"""


    if ai_enabled:

        try:

            prompt=f"""

Generate sustainability advice.

Score:
{score}

Impact:
{impact}

"""

            r=model.generate_content(
                prompt
            )

            result+=f"""

---

# 🤖 AI Insights

{r.text}

"""

        except:

            result+="\nAI unavailable."


    st.markdown(

f"""

<div class='report'>

{result}

</div>

""",

unsafe_allow_html=True

)



st.write("")


a,b,c=st.columns(3)


with a:

    st.metric(

        "SDG",

        "13 🌱"

    )


with b:

    st.metric(

        "AI",

        "Gemini"

    )


with c:

    st.metric(

        "Goal",

        "Climate"

    )


st.info(

"""

Climate Action

Reduce Emissions

Build Sustainable Habits

"""

)
