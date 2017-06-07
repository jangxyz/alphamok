# from gym_gomoku.envs.util

from gym.utils import seeding
from gym_gomoku.envs.util import gomoku_util

np_random, _ = seeding.np_random()

###
### make_beginner_policy
###

def defend_policy(curr_state):
    '''Return the action Id, if defend situation is needed
    '''
    b = curr_state.board
    player_color = curr_state.color
    opponent_color = gomoku_util.other_color(player_color)
    #lines, start, next_move = None, None, None # initialization
    
    # List all the defend patterns
    pattern_four_a = [0] + [gomoku_util.color_dict[opponent_color]] * 4         #[0,1,1,1,1]
    pattern_four_b = [gomoku_util.color_dict[opponent_color]] * 4 + [0]         #[1,1,1,1,0]
    pattern_three_a = [0] + [gomoku_util.color_dict[opponent_color]] * 3 + [0]  #[0,1,1,1,0]
    pattern_three_b = [gomoku_util.color_dict[opponent_color]] * 2 + [0] + [gomoku_util.color_dict[opponent_color]] * 1  #[1,1,0,1]
    pattern_three_c = [gomoku_util.color_dict[opponent_color]] * 1 + [0] + [gomoku_util.color_dict[opponent_color]] * 2  #[1,0,1,1]
    patterns = [pattern_four_a, pattern_four_b, pattern_three_a, pattern_three_b, pattern_three_c]
    
    for p in patterns:
        action = connect_line(b, p)
        if (action): # Action is not none, pattern is found, place stone
            return action
    
    # No defend pattern found
    return None

def fill_box(board, coord):
    ''' check the box area around the previous coord, if there is empty place in the empty area
        Return: 
            action for within the box if there is empty
            random action if the box if full
    '''
    all_legal_moves = board.get_legal_move()
    if (coord[0] >=0): # last move coord should be within the board
        box = [(i,j) for i in range(coord[0]-1, coord[0]+ 2) for j in range(coord[1]-1, coord[1] + 2)] # 3x3 box
        legal_moves = []
        for c in box:
            if (c in all_legal_moves):
                legal_moves.append(c)
        if (len(legal_moves) == 0):
            # all the box is full
            next_move = all_legal_moves[np_random.choice(len(all_legal_moves))]
            return board.coord_to_action(next_move[0], next_move[1])
        else :
            next_move = legal_moves[np_random.choice(len(legal_moves))]
            return board.coord_to_action(next_move[0], next_move[1])
    else:
        next_move = all_legal_moves[np_random.choice(len(all_legal_moves))]
        return board.coord_to_action(next_move[0], next_move[1])

def connect_line(board, pattern):
    ''' Check if pattern exist in board_state, Fill one empty space to connect the dots to a line
        Return: Action ID
    '''
    start_idx = 0
    empty_idx = []
    for id, val in enumerate(pattern):
        if (val == 0):
            empty_idx.append(id)
    
    lines, starts = gomoku_util.check_pattern_index(board.board_state, pattern)
    if (len(starts)>= 1): # At least 1 found
        line_id = np_random.choice(len(lines)) # randomly choose one line
        line = lines[line_id] # [(x1,y1), (x2,y2), ...]
        start_idx = starts[line_id]
        # Choose next_move among all the available the empty space in the pattern
        next_idx = start_idx + empty_idx[np_random.choice(len(empty_idx))]
        next_move = line[next_idx]
        return board.coord_to_action(next_move[0], next_move[1])
    else:
        return None

def strike_policy(curr_state, prev_state, prev_action):
    b = curr_state.board
    #all_legal_moves = b.get_legal_move()
    
    # last action taken by the oppenent
    #last_action = prev_state.board.last_action
    last_coord = prev_state.board.last_coord
    player_color = curr_state.color
    
    # List all the strike patterns
    pattern_four_a = [0] + [gomoku_util.color_dict[player_color]] * 4         #[0,1,1,1,1]
    pattern_four_b = [gomoku_util.color_dict[player_color]] * 4 + [0]         #[1,1,1,1,0]
    pattern_three_a = [0] + [gomoku_util.color_dict[player_color]] * 3 + [0]  #[0,1,1,1,0]
    pattern_three_b = [gomoku_util.color_dict[player_color]] * 2 + [0] + [gomoku_util.color_dict[player_color]] * 1  #[1,1,0,1]
    pattern_three_c = [gomoku_util.color_dict[player_color]] * 1 + [0] + [gomoku_util.color_dict[player_color]] * 2  #[1,0,1,1]
    pattern_two = [0] + [gomoku_util.color_dict[player_color]] * 2 + [0]      #[0,1,1,0]
    patterns = [pattern_four_a, pattern_four_b, pattern_three_a, pattern_three_b, pattern_three_c, pattern_two]
    
    for p in patterns:
        action = connect_line(b, p)
        if (action): # Action is not none, pattern is found
            return action
    
    # no other strike pattern found, place around the box within previous move
    action = fill_box(b, last_coord)
    return action

def beginner_policy(curr_state, prev_state, prev_action):
    b = curr_state.board
    #player_color = curr_state.color
    #opponent_color = gomoku_util.other_color(player_color)
    next_move = None # initialization, (x1, y1)
    
    # If defend needed
    action_defend = defend_policy(curr_state)
    if action_defend is not None:
        return action_defend
    
    # No Defend Strategy Met, Use Strike policy B to connect a line
    action_strike = strike_policy(curr_state, prev_state, prev_action)
    if action_strike is not None:
        return action_strike
    
    # random choose legal actions
    legal_moves = b.get_legal_move()
    next_move = legal_moves[np_random.choice(len(legal_moves))]
    return b.coord_to_action(next_move[0], next_move[1])
    
###
###
###


_prev_state = None

def choose_action(env, **data):
    prev_state = _prev_state or env.state
    action = beginner_policy(env.state, prev_state=prev_state, prev_action=None)
    return action

def after_action(env, observation, reward, done, info, **data):
    global _prev_state

    # keep state to _prev_state
    _prev_state = env.state

#def init(env):
#    return {}

#def complete(env, **data):
#    pass

#def before_episode(env, episode_num, **data):
#    return data

#def after_episode(env, observation, reward, done, info, **data):
#    pass

