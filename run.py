#!/usr/bin/env python

from __future__ import print_function

import gym
import gym_gomoku

import click


def default_policy(env):
    ''' DEMO simplest policy implementation '''
    # sample without replacement
    action = env.action_space.sample()
    return action


def play_episode(env, policy, episode, 
                 render_step, render_win_steps, render_lose_steps, render_tie_steps, render_episode, 
                 **data):

    # reset
    env.reset()
    episode_history = []

    # callback
    if 'before_episode' in dir(policy):
        _result = policy.before_episode(env, episode, **data) 
        if _result is not None:
            data = _result

    # run
    for _i in range(env.action_space.n):
        # chose action
        action = policy.choose_action(env, **data)

        # apply action
        (observation, reward, done, info) = env.step(action)
        # after action
        episode_history.append(str(env.state))
        if 'after_action' in dir(policy):
            policy.after_action(env, observation, reward, done, info, **data) 

        # render
        if render_step:
            env.render()

        if done:
            print("Game is Over (reward: {})".format(reward))
            if reward > 0: print("You Won!!!")
            if reward < 0: print("You Lost!!!")

            break

    # after episode
    if render_episode:
        env.render()
    if render_win_steps and reward == 1.0:
        for i,board_str in enumerate(episode_history):
            print(board_str)
    if render_lose_steps and reward == -1.0:
        for i,board_str in enumerate(episode_history):
            print(board_str)

    if 'after_episode' in dir(policy):
        _result = policy.after_episode(env, observation, reward, done, info, **data) 
        if _result is not None:
            data = _result


def load_env(board_size, env_policy_name='beginner'):
    gym_name = 'Gomoku{size}x{size}-v0'.format(size=board_size) # Gomoku19x19-v0

    # load env with board_size
    if board_size not in [9, 19]:
        # register new env
        gym.envs.registration.register(
            id=gym_name,
            entry_point='gym_gomoku.envs:GomokuEnv',
            kwargs={
                'player_color': 'black',
                'opponent': 'beginner', # beginner opponent policy has defend and strike rules
                'board_size': board_size,
            },
            nondeterministic=True,
        )

    env = gym.make(gym_name)

    # reload env with policy
    if env_policy_name != 'beginner':
        env.opponent = env_policy_name
        env_module_name = 'env_policy.{}'.format(env_policy_name)
        env_policy = __import__(env_module_name, globals(), locals(), ['policy'], 0)
        env.opponent_policy = env_policy.policy

    return env


@click.command()
@click.option('--size', default=19, help='size of board [19]')
@click.option('--policy', default='random', help='name of policy [random]')
@click.option('--env-policy', default='beginner', help='name of env policy [beginner]')
@click.option('--episodes', default=1, help='number of episodes to run [1]')
@click.option('--render-steps/--no-render-steps', default=True, help='render on each step [True]')
@click.option('--render-win-steps/--no-render-win-steps', default=False, help='render all steps episodes won [False]')
@click.option('--render-lose-steps/--no-render-lose-steps', default=False, help='render all steps episodes lost [False]')
@click.option('--render-tie-steps/--no-render-tie-steps', default=False, help='render all steps episodes lost [False]')
@click.option('--render-episode/--no-render-episode', default=False, help='render on end of episode [False]')
def main(size, policy, episodes, env_policy, 
         render_steps, render_win_steps, render_lose_steps, render_tie_steps, render_episode):
    # load env
    env = load_env(size, env_policy)

    # load policy
    policy_name = 'policy.{}'.format(policy)
    policy = __import__(policy_name, globals(), locals(), ['choose_action'], 0)

    # init
    policy_has_init = 'init' in dir(policy)
    init_data = policy.init(env) if policy_has_init else {}

    # run each episodes
    for i in range(1, episodes+1):
        play_episode(env, policy, i, render_steps, render_win_steps, render_lose_steps, render_tie_steps, render_episode, data=init_data)

    # complete
    if 'complete' in dir(policy):
        policy.complete(env, data=init_data)


if __name__ == '__main__':
    main()

