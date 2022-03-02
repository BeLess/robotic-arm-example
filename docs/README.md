# Pickle Coding Challenge: Rationale

## Rotating base
One of the big features I decided to add was a rotating base for Gherkin, expanding its accessible space.

At default, Gherkin's dual joint arm can only reach points within a 2 dimensional, circular plane. By giving the base of the arm the ability to rotate, 
we can turn that 2d plane into a 3d sphere of influence.

### Functional Logic
So, normally spherical coordinates are denoted by "the radial distance of that point from a fixed origin, 
its polar angle measured from a fixed zenith direction, 
and the azimuthal angle of its orthogonal projection on a reference plane that passes through the origin and is orthogonal to the zenith" <sup>[wikipedia](https://en.wikipedia.org/wiki/Spherical_coordinate_system) </sup>

Unfortunately, that's not how our coordinates are represented here. And thanks to my unfamiliarity with the existing implementation of the double-jointed arm,
I was disinclined to change the measurements in the goal from planar to spherical coordinates. Instead, I added a "planar angle" to the goal coordinates.

The idea behind this is the fact that because the arm can rotate completely around the center joint, thus being able to reach behind itself, then we technically only need to concern ourselves with 180 degrees of planar angle.

Essentially, if the planar angle of the goal is 110 degrees, the arm can reach the goal if the "front" of the robot is "facing" either 110 degrees OR it's opposite angle, 290.

### Implementation
* As mentioned, I added a 3rd datapoint to the Goal object, denoting the angle of the circular plane of the goal with respect to the base
* Implemented some circular angle logic for the math
  * Increasing an angle above 359 resets the value 0 + the remaining rotation
  * Decreasing an angle below 0 resets the value to 360 - the remaining rotation
  * Added access to a simple `angle.inverse`property
* Added logic to determine the most efficient direction of rotation
* Added configuration for rotation speed of the robots base
  * `FAST_ROTATION_SPEED` for larger distances
  * `FINE_ROTATION_SPEED` for more precise movement
* The robot tracks its current angle, and the direction determination takes that into account, so subsequent goals should "just work"
* The arm joints don't begin moving until the base reaches the correct angle
  * Both movements can probably be done independently, in parallel. Might revisit

### Visualization
Representing 3 dimensional movement is already kind of a headscratcher, and I haven't worked with `pygame` before, so I had to get creative.

I implemented a section below the core arm display that shows the plane of influence as if from above the robot, the center being Gherkin and the line the reach of the arm. It's color coded to indicate "front" and back",
green being the front and red being the back

This display rotates around the center (Gherkin) until it reaches the desired angle to reach the goal angle

### The bizarre implementation of spherical coordinates
One of the core problems with trying to use standard (x,y) coordinates in rotational space is that what positive and negative refer to are <em>relative</em>. 
In this case we have issue with the x coordinate and the implementation of the rotation. I have attempted to diagram the situation below:

![gherkin_top_view.png](gherkin_top_view.png)

As mentioned above, because Gherkin can reach in a complete circle (both "in front" and "behind" itself), we don't have to rotate the base to the specific goal
angle in order to reach the desired coordinates. We can move the shortest distance, which might be the opposite angle of the goal.

Practically speaking, this means, starting from degree 0, a goal angle of 91-180 would cause Gherkin to rotate counterclockwise to reach the opposite angle (it's faster to rotate 45 degrees counterclockwise than 135 degrees clcokwise), as it's a shorter distance resulting in, essentially, facing backwards.

If we accept that a negative x values means Gherkin needs to reach "behind" itself to reach the goal, this rotation presents a problem when we have a -x and a goal angle >90. 
The robot is facing "backwards" (the correct direction), but the coordinates still want it to reach behind itself, because the negativeness of the value is relative to Gherkin's facing.

Thus the hack (`robot.py:146`): When we receive a goal that would cause us to face backwards, with a negative x value, we instead replace it with the absolute value of the coordinate,
the practical implication being that Gherkin is still facing the correct direction in regard to its goal.

The inverse is also true. If we have a positve x value (reach "forward"), but turn to face "backwards", we have to modify the x value to be negative to ensure we're still reaching to the
correct side of the sphere of influence.

## Fleet Management
One robot is nice, but many hands make light work, so I figured adding the ability to manage multiple robots at the same time would be neat

### Asynchronicity
It's pretty natural to add some multi processing when we're talking about multiple robots, and my preferred method of concurrent process is the Actor Model.

To that end, I moved all the core robot functionality into the `Robot` class, so that I could use it as an actor. Each instance of robot is self-contained and independent of other states
(the one exception is a shared `Visualizer`), allowing us to feed a robot a goal and let it do what it's built to do.

This is done through a library called [pykka](https://pykka.readthedocs.io/en/stable/). Pykka is the python implementation of a Java/Scala library called Akka, which is
a very easy to use implementation of the [actor model](https://en.wikipedia.org/wiki/Actor_model).

Each robot inherits from the `ThreadedActor` class. This gives them the ability to be started as actors waiting for work, while still allowing you to use them in a normal, synchronous, fashion.

These actors are then proxied (so we can interact with them through their existing API) and fed work through our `FleetManager`

### Managing the fleet
At base, it's pretty easy to share a queue of work between actors, but that probably wouldn't result in a very efficient pathing or ordering of work.
This lead to the `FleetManager`, a class responsible for keeping track of our Gherkins and assigning them work (slightly) more intelligently.

The optimization is pretty simple. When a goal is received, preform the following checks to determine the best robot for the goal:
* Prioritize idle robots
* Deprioritize the busiest robot
* Look at the work queues for the remaining robot
* Choose the robot whose last goal in the queue (ie, the job that would occur before this one) is "closest" to the received goal

The first two rules are to make sure there's some general load balancing (as the closeness measure is somewhat fuzzy), so one robot isn't ending up overworked or left fallow

The last two are to do a light optimization of the work distribution. A simple way to try to make sure each robot isn't moving vast distances from goal to goal.

The `FleetManager` also collects and manages all the Futures produced by the robots, tying it all together when all the work is done. Right now it simply pretty prints the results,
but it should be pretty easy to take that data and do any number of things with it. 

### Visualization
Pygame actually handles multiprocessing pretty well, as it turns out. Only a couple of changes were necessary to get it to display the status of each robot
* Scale the window (as of writing, only horizontally) for each additional robot
* Keep track of a "robot offset" 
* Only blank out portions of the screen on update

Each robot knows it's offset, and is responsible for invoking the `update_display()` method. The offset is used to calculate which portion of the screen to blank and redraw.
It's also used to offset the lines and circles from their default position, leading to everything being lined up and moving independently.