def viterbi(obs, states, start_p, trans_p, emit_p):
    """
    Viterbi algorithm for finding the most likely sequence of hidden states given observed data.

    Parameters:
        obs (list): A list of observed emissions.
        states (list): A list of possible hidden states.
        start_p (dict): Initial probabilities of each state.
        trans_p (dict): Transition probabilities between states.
        emit_p (dict): Emission probabilities of each state for each observation.

    Returns:
        list: A list of dictionaries representing the Viterbi matrix, containing the highest probability and previous state for each state at each time step.
    """
    V = [{}]
    for st in states:
        # Calculate maximum transition probability to state 'st' at time t
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            #If probability of transitioning to state 'st' at time t from previous state 'prev_st' is maximum
            max_tr_prob = max(V[t-1][prev_st]["prob"]*trans_p[prev_st][st] for prev_st in states)
            # Iterate over previous states to find the one with maximum probability
            for prev_st in states:
                # If probability of transitioning to state 'st' at time t from previous state 'prev_st' is maximum
                if V[t-1][prev_st]["prob"]*trans_p[prev_st][st] == max_tr_prob:
                    max_prob = max_tr_prob * emit_p[st][obs[t]]
                    V[t][st] = {"prob": max_prob, "prev": prev_st}
                    break
    return V

def main():
    # Define observed data, states, initial probabilities, transition probabilities, and emission probabilities
    obs = ['normal', 'cold', 'dizzy']
    states = ['Healthy', 'Fever']
    start_p = {'Healthy': 0.6, 'Fever': 0.4}
    trans_p = {'Healthy': {'Healthy': 0.7, 'Fever': 0.3}, 'Fever': {'Healthy': 0.4, 'Fever': 0.6}}
    emit_p = {'Healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1}, 'Fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}}

    # Execute Viterbi algorithm and print result
    result = viterbi(obs, states, start_p, trans_p, emit_p)
    print(result)

if __name__ == "__main__":
    main()