

def choose_action(env, **data):
    # sample without replacement
    action = env.action_space.sample()
    return action

#def init(init, **data):
#    pass

#def after_action((observation, reward, done, info), **data):
#    pass

#def complete(env, **data):
#    pass

