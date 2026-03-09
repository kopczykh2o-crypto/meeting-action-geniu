import streamlit as st
from openai import OpenAI

# Konfiguracja strony
st.set_page_config(page_title="Meeting Action Genius", page_icon="🧠")

st.title("Meeting Action Genius 🧠")
st.write("Wklej transkrypcję ze spotkania, a sztuczna inteligencja wyciągnie z niej konkretną listę zadań do zrobienia.")

# Pole do wklejenia transkrypcji
transcript = st.text_area("Wklej tekst transkrypcji tutaj:", height=250)

# Przycisk uruchamiający AI
if st.button("Generuj listę zadań", type="primary"):
    if not transcript:
        st.warning("Proszę, wklej najpierw tekst ze spotkania!")
    else:
        try:
            # Pobieranie klucza API z bezpiecznych ustawień Streamlit
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
            
            with st.spinner('AI analizuje spotkanie... to potrwa kilka sekund.'):
                response = client.chat.completions.create(
                    model="gpt-4o-mini", # Szybki i tani model
                    messages=[
                        {"role": "system", "content": "Jesteś asystentem biurowym. Przeczytaj poniższą transkrypcję ze spotkania i wyciągnij z niej tylko konkretne zadania (To-Do). Zignoruj luźne rozmowy. Zwróć wynik w postaci prostej listy: [Osoba odpowiedzialna] - [Zadanie] - [Termin]. Jeśli brakuje terminu, napisz 'Brak'."},
                        {"role": "user", "content": transcript}
                    ],
                    temperature=0.2
                )
            
            st.success("Oto Twoje zadania:")
            st.info(response.choices[0].message.content)
            
        except Exception as e:
            st.error("Wystąpił błąd. Upewnij się, że wpisałeś poprawny klucz API OpenAI w ustawieniach (Secrets).")
