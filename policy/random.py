

def choose_action(env, **data):
    # sample without replacement
    action = env.action_space.sample()
    return action

#def init(env):
#    return {}

#def complete(env, **data):
#    pass

#def before_episode(env, episode_num, **data):
#    return data

#def after_action(observation, reward, done, info, **data):
#    pass

#def after_episode(observation, reward, done, info, **data):
#    pass

