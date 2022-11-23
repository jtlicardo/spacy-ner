import streamlit as st
import spacy
from spacy import displacy

text1 = (
    "The process will begin with a user task for choosing the student's preferences."
)
text2 = "After accepting the offer, he sends the confirmation to the online shop. The online shop then receives the confirmation."
text3 = "Then, the employer evaluates the candidate. After that, he confirms the evaluation."

st.header("Task extraction")

option = st.selectbox("Examples", (text1, text2, text3))

input_text = st.text_input("Text:", option)

nlp = spacy.load("./task-extraction-model")

doc = nlp(input_text)

spans = doc.spans["sc"]

sorted_by_start = sorted(spans, key=lambda x: x.start)

detected_tasks = []

for span in sorted_by_start:
    detected_tasks.append(span.text)

lemmatize_verb = spacy.load("en_core_web_sm")

tasks_with_lemmatized_verb = []

for task in detected_tasks:
    current_task = lemmatize_verb(task)
    updated_task = ""

    for token in current_task:
        if token.pos_ == "VERB":
            updated_task += token.lemma_ + " "
        else:
            updated_task += token.text_with_ws

    tasks_with_lemmatized_verb.append(updated_task)

st.header("Detected tasks")

ent_html = displacy.render(doc, style="span", jupyter=False)

st.markdown(ent_html, unsafe_allow_html=True)

st.subheader("Tasks")

list = ""

for task in tasks_with_lemmatized_verb:
    list += "- " + task + "\n"

st.markdown(list)
