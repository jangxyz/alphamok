#!/usr/bin/env python

from __future__ import print_function

import gym
import gym_gomoku

import click


def play_episode(env, policy, episode, **data):
    env.reset()
    for _i in range(20):
        # chose action
        action = policy.choose_action(env, **data)

        # apply action
        (observation, reward, done, info) = env.step(action)

        #
        policy_has_after_action = 'after_action' in dir(policy)
        policy.after_action((observation, reward, done, info), **data) if policy_has_after_action else None

        # render
        env.render()
        if done:
            print("Game is Over")
            break

def default_policy(env):
    ''' simplest policy implementation '''
    # sample without replacement
    action = env.action_space.sample()
    return action


@click.command()
@click.option('--size', default=19, help='size of board [19]')
@click.option('--policy', default='random', help='name of policy [random]')
@click.option('--episodes', default=1000, help='number of episodes to run [1000]')
def main(size, policy, episodes):
    # load env
    gym_name = 'Gomoku{size}x{size}-v0'.format(size=size)
    env = gym.make(gym_name) # default 'beginner' level opponent policy

    # load policy
    policy_name = 'policy.{}'.format(policy)
    policy = __import__(policy_name, globals(), locals(), ['choose_action'], -1)

    # init
    policy_has_init = 'init' in dir(policy)
    init_data = policy.init(env) if policy_has_init else None

    # run each episodes
    for i in range(1, episodes+1):
        play_episode(env, policy, i, data=init_data)

    # end
    policy_has_done = 'done' in dir(policy)
    policy.complete(env, data=init_data) if policy_has_done else None


if __name__ == '__main__':
    main()

