import random

import streamlit as st


# Funzione per generare coppie di squadre
def create_pairs(teams):
    random.shuffle(teams)
    pairs = []
    while len(teams) > 0:
        team1 = teams.pop(0)
        if teams:
            team2 = teams.pop(0)
        else:
            team2 = "BYE"  # Se dispari, l'ultima squadra passa automaticamente
        pairs.append((team1, team2))
    return pairs

# Inizializzazione delle variabili di sessione
if 'teams' not in st.session_state:
    st.session_state.teams = []
if 'round' not in st.session_state:
    st.session_state.round = 1
if 'current_pairs' not in st.session_state:
    st.session_state.current_pairs = []
if 'winners' not in st.session_state:
    st.session_state.winners = []
if 'losers' not in st.session_state:
    st.session_state.losers = ""


st.title("Gestione Torneo")

# Input per aggiungere nuove squadre
if len(st.session_state.current_pairs) == 0:
    team_name = st.text_input("Inserisci il nome della squadra")
    if st.button("Aggiungi squadra") and team_name:
        st.session_state.teams.append(team_name)

# Mostra le squadre aggiunte
if len(st.session_state.current_pairs) == 0:
    st.subheader("Squadre partecipanti:")
    for team in st.session_state.teams:
        st.write(team)

# Generazione delle coppie di squadre
if len(st.session_state.current_pairs) == 0:
    if st.button("Genera coppie"):
        st.session_state.current_pairs = create_pairs(st.session_state.teams.copy())
        st.rerun()

# Mostra le coppie e consenti di selezionare i vincitori
if st.session_state.current_pairs:
    print(st.session_state.current_pairs)
    if st.session_state.losers != "":
        st.write(f" La coppi {st.session_state.losers} è stata ripescata!!!!")
        st.session_state.losers = ""

    st.subheader(f"Round {st.session_state.round} - Seleziona i vincitori:")
    winners = []
    for i, (team1, team2) in enumerate(st.session_state.current_pairs):
        st.write(f"Match {i+1}: {team1} vs {team2}")
        if team2 != "BYE":
            winner = st.radio(f"Vincitore Match {i+1}", [team1, team2], key=f"match_{i+1}")
            winners.append(winner)
        else:
            print("WEEEEEEEEEEEEEEEEEE " )
            st.write(f"{team1} passa direttamente")
            winners.append(team1)

    if st.button("Prossimo round"):
        if len(st.session_state.teams) % 2 != 0:
            losers = list(set(st.session_state.teams) - set(winners))
            random.shuffle(losers)
            winners.append(losers[0])
            st.session_state.losers = losers[0]
            st.session_state.teams = []
        st.session_state.winners = winners
        st.session_state.current_pairs = create_pairs(winners)
        st.session_state.round += 1
        st.session_state.winners = []
        st.rerun()

# Mostra il vincitore finale
if len(st.session_state.current_pairs) == 1 and st.session_state.current_pairs[0][1] == "BYE":
    st.subheader(f"Il vincitore del torneo è: {st.session_state.current_pairs[0][0]}")
