# Pickle Coding Challenge
Gotta put something in here for the commit


## Introduction
Help Gherkin. 

Gherkin is a two-link robot arm trying to reach a randomized goal. Help Gherkin
by adding features and improving the existing sandbox.

Choose and implement one or more of the projects in the backlog below, or pick one of your own invention. This is your chance to impress us, so choose something that will demonstrate your full programming abilities. For each project, the Gherkin should continue to reach the goal after implementation.

The implementation can leverage Python library functions, helper functions you author, or data stored in .py files or other files in your submission.

If you write any files or functions which test the implementation, please include them in your repository as well.

**Please submit your changes as a pull request to the repository.**

## Setup and Run

Note: While we expect the environment and sandbox to work across different platforms, we have not done extensive testing.

### Known Good Platforms

| OS     | Versions |
|--------|----------|
| Ubuntu | 18.04    |


### Setup the Development Environment

```
$ ./scripts/bootstrap
```

### Enter the virtual environment

```
$ source ./scripts/init
```

### Run

```
$ python challenge.py
```


## Backlog

* Add borders and wall to the world
  * Bonus: make a more easily configurable representation
* Add a third link to the arm
* Make a moving goal
* Improve the visualization implementation
* Visualize Paths, Velocities, Accelerations, over time in the sandbox window
  * Note: Not as good to render several separate visualizations
* "Cloudify" gherkin's configuration
* Use [py-trees](https://py-trees.readthedocs.io/en/devel/) to make complex behaviors
* Add unit tests and clean up the code (note: don't just do this item!)
* Change system from top down to on the wall - add gravity!
  * This will require changing Gherkin to use torque control
* Replace the controller with a learned policy
