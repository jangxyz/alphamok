
# Gym-omok Testbed

Play with default options


```bash
$ python run.py
```

## Contents

* [#Options](#user-content-options)
  * [--size: set board size](#user-content---size-set-board-size)
  * [#--policy: set agent action policy](#user-content---policy-set-agent-action-policy)
  * [#--env-policy: set environment policy](#user-content---env-policy-set-environment-policy)
  * [#--episodes: number of episodes to run](#user-content---episodes-number-of-episodes-to-run)
  * [#Render options](#user-content-render-options)
* [#Policy Specification](#user-content-policy-specification)
* [#Examples](#user-content-examples)



## Options

```bash
$ python run.py --help
Usage: run.py [OPTIONS]


Options:
  --size INTEGER                  size of board [19]
  --policy TEXT                   name of policy [random]
  --env-policy TEXT               name of env policy [beginner]
  --episodes INTEGER              number of episodes to run [1]
  --render-steps / --no-render-steps
                                  render on each step [True]
  --render-win-steps / --no-render-win-steps
                                  render all steps episodes won [False]
  --render-lose-steps / --no-render-lose-steps
                                  render all steps episodes lost [False]
  --render-tie-steps / --no-render-tie-steps
                                  render all steps episodes lost [False]
  --render-episode / --no-render-episode
                                  render on end of episode [False]
  --help                          Show this message and exit.
```

### --size: set board size

Either one of 9 or 19 (default 19)


### --policy: set agent action policy

By default the agent selects a random action from the action space.

To add a new policy, add a python file under `policy/` and pass the name to `--policy` option.

        python run.py --size=9 --episodes=1 --policy=random

By default there are two policies provided, [random](https://github.com/jangxyz/alphamok/blob/master/policy/random.py) and [beginner](https://github.com/jangxyz/alphamok/blob/master/policy/beginner.py) from the gym-gomoku package.

To build a policy, see [#Policy Specification](#user-content-policy-specification) below.


### --env-policy: set environment policy

You can set custom environment policy. By default it behaves as [beginner](https://github.com/jangxyz/alphamok/blob/master/source/gym-gomoku/gym_gomoku/envs/util.py).

For example you can run your agent with the `beginner` policy, and environment with `dull4` policy, which just blocks at 4-in-a-row and else random. This already lets the agent win!

        python run.py --size=9 --env-policy=dull4 --policy=beginner

Some pre-defined env-policies:
- dull4: play at random position, except when it finds a 4-in-a-row situation.
- dull3: play at random position, except when it finds a 3-in-a-row situation.


### --episodes: number of episodes to run

To let the agent run, you can run episode multiple times.

        python run.py --episodes=1000 --no-render-steps


### Render options

Multiple render options.

* `--render-steps`: render on each step. default `True`
* `--render-win-steps` : render every step only if game is won by agent. default `False`
* `--render-lose-steps`: render every step only if game is lost by agent. default `False`
* `--render-tie-steps` : render every step only if game is complete but no one won. default `False`
* `--render-episode` : render after each episode. default `False`

If you want to add more specific conditions on rendering, use callbacks inside a policy.


## Policy Specification

Minimum specification required for a policy is to have a function `choose_action(env, **data)`,
which returns an action given the environment variable `env`.

There could be additional callbacks, called upon init, complete, before/after each episode, and after an action.
If the policy module contains the corresponding functions, it will be called ith proper arguments.

* `init(env)`

    Called before any of the episode is run.

    NOTE return value of the `init` function will be passed to every other callbacks as `**data` argument.

* `before_episode(env, episode_num, **data)`

    Called before each episode is run.

    NOTE if the callback has any return value that is not `None`, it will replace the `data` object.

* `after_action(env, observation, reward, done, info, **data)`

    Called after each action is applied to the environment.
    The response of the environment `(observation, reward, done, info)` is passed along with `**data`.

    You can use this callback to save any 'previous state' variables for the policy. See `policy/beginner.py` for an example.


* `after_episode(env, observation, reward, done, info, **data)`

    Called after each action is applied to the environment.
    The response of the environment `(observation, reward, done, info)` is passed along with `**data`.

    NOTE if the callback has any return value that is not `None`, it will replace the `data` object.

* `complete(env, **data)`

    Called after the whole iteration is done.


For instance, the simplest implementation [policy/random.py](https://github.com/jangxyz/alphamok/blob/master/policy/random.py) looks like this:

```python
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

#def after_action(env, observation, reward, done, info, **data):
#    pass

#def after_episode(env, observation, reward, done, info, **data):
#    pass
```

Checkout [policy/beginner.py](https://github.com/jangxyz/alphamok/blob/master/policy/beginner.py) for another example.


