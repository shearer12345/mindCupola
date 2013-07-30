Mind-Cupola Visualiser Specification
=======================================


:Short name:
    mcv

:version:
    1.0

:authors:
    John Shearer
    
    Brigitta Zics    

:date:
    Wednesday April 4th 2012

Overview
--------

This document provides details on the Mind-Cupola Visualiser (given as *mcv* herein). Specifically, it provides:
    * `Overview`_
    * `Interaction Design`_
    * `Technical overview`_
    * `Technical requirements`_
    * `Aesthetic`_ demands for the implementation
    * `OSC API`_ for mcv

The Mind-Cupola Visualiser is intended to produce an immersive, flow inducing effect on people through smoothly moving, flocking boids that respond to both their eye-movements (measured outside *mcv*) and to a predicted (outside *mcv* by JS) affective state. The Mind-Cupola Visualiser itself needs only to respond to explicitly given inputs (detailed in the `OSC API`_, which are tied closely to the visualation (abstracted away from their specific sources).

We expect the implementation to occur in a number of stages. As such, some parts are marked as *stage 2*, or *stage 3*, or later. Everything without a stage marker should be assumed to be *stage 1*.

Interaction Design
------------------

From the user experience point of view itis important how we lead the user smoothly into the interaction. This connects with the aesthetic design, but also needs to support legibility of the system.

Focus on:
  Aesthetic
  Legibility
  Immersion

Interaction States
~~~~~~~~~~~~~~~~~~

Changes in Interaction State are notified to MCV through OSC messages detailed below.

1) Cupola Empty (and up) - start state
    :Visualiser: boids moving, but out of focus
    :Auralizer: low volume, subtle, atmospheric, deep
    :LEDs: perhaps random slow flashing  patterns of LED
    :Fans: off
    :Heater: off

2) Cupola Lowering
    :Visualiser: as 1) - boids moving, but out of focus
    :Auralizer: some luring in sound
    :LEDs: blank
    :Fans: off
    :Heater: off

3) Calibrating
    :Visualiser:

        blank/dark screen (boids have been faded out, so no visual distractions)

        calibration circles in appropriate places (is MiraMetrix supports external calibration), otherwise assume that the calibration will overlay the MCV



    :Auralizer: perhaps speech
    :LEDs: perhaps words
    :Fans: off
    :Heater: off

4) Starting - give feedback on calibration
    :Visualiser: TODO 
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

5) Running
    :Visualiser: quite a lot of detail. eyes not visible => defocus
    :Auralizer: predator distance increase 'suspense'
    :LEDs: 
    :Fans: 
    :Heater: 

6) Cupola Raising
    :Visualiser: TODO
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

Interaction State Transitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:1->2: on user entry
    :Visualiser:  TODO
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

:2->6: on user exit
    :Visualiser:  TODO
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

:1->3: on cupola down
    :Visualiser:  TODO
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

:3->4: finished calibration
    :Visualiser:  TODO
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

:4->3: bad calibration
    :Visualiser:  TODO
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

:4->5: good calibration
    :Visualiser:  TODO
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

:5->6: on user exit
    :Visualiser:  TODO
    :Auralizer: 
    :LEDs: 
    :Fans: 
    :Heater: 

- what is on the screen   when the cupola is not operation
- is there a text/image when the person activates the cupola

- how does the person get feedback if the eye tracking does not see them

- Calibration: We probably have to make the calibration process nicer a bit

- How is the transition happen between screens when the calibration finished

-How do we feedback the person if the system does not pick them up ( do we have a bar or something like this always on the screen?)

- what happens when the interaction finished ( particle shape something? sound probably?)

what does the PAD model control?

I am not sure that the technical description includes this but it is definitely an important task the feedback mechanism 
that user's get when the eye tracking does not see them.
This happens two times:
1. Before, during calibration process.
2. During the interaction when the system loses the user's eye.


Technical overview
------------------

The Mind-Cupola Visualiser will be based on classical Reynolds-like boids (http://en.wikipedia.org/wiki/Boids), with a few small additions - speed control, predators and predator avoiding behaviour by the boids, and finally, variation of boid attributes between individual boids combined with a set of global multipliers for the boids - so that the entire flock can be adjusted as a whole.

For Discussion
~~~~~~~~~~~~~~

* Should the simulation be in 2D or 3D?

Technical requirements
----------------------

#) run both fullscreen and in a window (with a commandline switch to indicate which)
#) start from the commandline and go straight into the visualisation without any user intervention
#) consistently achieve a framerate of at least 30fps
#) run for a significant (multiple hours) without crashing
#) simulate a *minimum* of 2,000 boids
#) respond appropriately to OSC messages as defined in the `OSC API`_
#) boids should be textured and lit
#) boids need only a simple geometry mesh
#) boids *don't* need any skeletal animation (their bodies don't need to change shape)

notes:
    * the update of each boids direction does not *have* to occur every frame, but update of each boids position should be everyframe. i.e. the AI for the boids can be run slower than the simulation rate (and therefore framerate) if needs be. Optimisation of this is left up to the implementation.

Aesthetic
----------

To be sent in a separate document from Brigitta


OSC API
-------

The visualiser (mcv) should listen for OSC on a command-line defined port (default to 12345)

See http://opensoundcontrol.org/spec-1_0 for Type Tags used below.

There are a variety of incoming OSC messages that mcv should handle, detail as follows:

Interaction State
    * `Interaction State`_
    * `Calibration`_
    * `Attractor`_
    * `Flock`_
    * `BoidSpawn`_
    * `PredatorSpawn`_
    * `Internal State Output for Auralization`_
    * `Debug - by Output of Internal State`_
    * `Generic Debug`_
    * `Future - Stage to be established`_

Interaction State
~~~~~~~~~~~~~~~~~

The present state of the interaction. There are 6 possible states (defined above)

1) Cupola Empty (and up)
2) Cupola Lowering
3) Calibrating
4) Starting - give feedback on calibration
5) Running
6) Cupola Raising

state
#####
    ``/mcv/interactionstate i``

    :i: the present interaction state

Calibration
~~~~~~~~~~~

State
#################

    ``/mcv/calibration/state i``

    :i: the present calibration state. 0 = not calibrating. 1 = calibrating (prepare for start points)

Start Point
###########

    ``/mcv/calibration/startPoint i f f``

    :i: point number
    :f: the X position of the point on the screen - relative from 0 to 1 - to show now
    :f: the Y position of the point on the screen - relative from 0 to 1 - to show now

End Point
#########

    ``/mcv/calibration/endPoint i``

    :i: point number


other notes - for JS
####################

send to Eyetracker to hide the window
CALIBRATE_SHOW = FALSE  so our window doesn't show

send to Eyetracker to start the calibration process
CALIBRATE_START = TRUE so the calibration starts


Then watch for:

<CAL ID="CALIB_START_PT" PT="1" CALX="0.10000" CALY="0.08000" />

Which tells you the current point and position on the screen (pt1,
X=.1*width, Y=.08*height) and

<CAL ID="CALIB_RESULT_PT" PT="1" CALX="0.10000" CALY="0.08000" />

which tells you when the current point is finished and it is time to
move on to the next point

The object you draw should be large enough to catch the viewers
attention from their peripheral vision, with a higher contrast shape
towards the center of the calibration marker to draw the eyes towards
the true calibration point. Unfortunately at this point you cannot
change the calibration positions though.


Attractor
~~~~~~~~~

A point in space that (nearby) boids are attracted towards.

position
#########
    ``/mcv/attractor/position f f``

    :f: attractor x position in range 0-1 on screen (from left)
    :f: attractor y position in range 0-1 on screen (from bottom)

strength
########

    ``/mcv/attractorstrength f``

    :f: float representing how strong the attractor attracts, normal range -1 to 1, but any float could be sent. Negative values represent repulsion.


Flock
~~~~~

Parameters that apply to the whole flock.

Separation
##########

    ``/mcv/flock/separation f``

    :f: the tendency of the flock to avoid crowding local flockmates (multiplier on each boid)

Alignment
#########

    ``/mcv/flock/alignment f``

    :f: the tendency of the flock to steer towards the average heading of flock mates (multiplier on each boid)

Cohesion
########

    ``/mcv/flock/cohesion f``

    :f: the tendency of the flock to move toward the centre of flock mass (multiplier on each boid)

Speed
#####

    ``/mcv/flock/speed f``

    :f: multiplier on the speed on each member of the flock

Fear
####

    **stage 2**

    ``/mcv/flock/fear f``

    :f: multiplier on the fear factor (of predators by boids) - tendency to move away from predators

MigrateShape
####

    ``/mcv/flock/migrateShapeNumber i``

    :i: migrateShape selector. 0=> no migrate to shape (i.e. normal eye following mode), others will attempt to use a shape in the boids run directory called shapeXX, where XX is the number

Override Boid Population Size
#############################

    ``/mcv/flock/overrideboidpopulationsize i``

    :i: force the population of boids to a certain size

        default to 0

Override Predator Population Size
#################################

    **stage 2**

    ``/mcv/flock/overridepredatorpopulationsize i``

    :i: force the population of predators to a certain size

        default to 0

BoidSpawn
~~~~~~~~~

**stage 2** - individual parameters does not need to be implemented initially

Boid spawn parameters. These should be a distribution centred on the mean (parameter 1) and distributed according to the standard deviation (approximately) (parameter 2)




Spawn Rate
##########

    **stage 3**

    ``/mcv/boidspawn/rate f``

    :f: 
        how frequently (on average) boids should spawn (in boids per second)
        default to zero (so boids are only created on ``overrideboidpopulationsize()``)

            i.e. initially (and at stage 1 and 2) boids should only spawn at load-time, and on ``overrideboidpopulationsize()``

            so they won't be spawning or dying initially (or in stages 1 or 2)
        
Separation
##########

    **stage 2**

    ``/mcv/boidspawn/separation f f``

    :f: mean tendency to avoid local flockmates of spawned boids
    :f: std dev

Alignment
#########

    **stage 2**

    ``/mcv/boidspawn/alignment f f``

    :f: mean tendency to steer towards the average heading of flockmates
    :f: std dev

Cohesion
########

    **stage 2**

    ``/mcv/boidspawn/cohesion f f``

    :f: mean tendency to steer towards the centre of flock mass
    :f: std dev

Speed
#####

    **stage 2**

    ``/mcv/boidspawn/speed f f``

    :f: mean speed
    :f: std dev

Fear
####

    **stage 3**

    ``/mcv/boidspawn/fear f f``

    :f: fear factor (of predators) - tendency to move away from predators
    :f: std dev

PredatorSpawn
~~~~~~~~~~~~~

**stage 2 and 3**


Predator spawn parameters. These should be a distribution centred on the mean (parameter 1) and distributed according to the standard deviation (approximately) (parameter 2)

Spawn Rate
##########

    **stage 3**

    ``/mcv/predatorspawn/rate f``

    :f: 
        how frequently (on average) predators should spawn (in predators per second)

        default to zero (so predators are only created on 
        ``overridepredatorpopulationsize()``)

Speed
#####

    **stage 2**

    ``/mcv/predatorspawn/speed f f``

    :f: mean speed
    :f: std dev

Fear
####

    **stage 2**

    ``/mcv/predatorspawn/fear f f``

    :f: fear factor that the predators creates in boids
    :f: std dev


Internal State Output for Auralization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The visualiser should send be able to send some or all of its internal state out over OSC, for position Auralization/Sonification purposes.

**Send in an OSC bundle**


:String: flock type (bees, birds, fish) - send on change
:Float: flock position (mean)
:Float: flock velocity (mean)
:Float: flock density
:Float: flock turn rate? (curvature?) use http://en.wikipedia.org/wiki/Sinuosity
:String: camera mode - send on change
:Float: focus
:String: interaction state (no user, calibrating, starting, running, stopping) - send on change
:Float: calibration quality
:Int: number of predators present
:Float: predator to flock distance

OSC format to be established.

Internal state output for Auralization toggle
#############################################
    
    ``/mcv/auralizationoutput/internalstateoutputtoggle i``
    
    :0: no internal state output (default)

    :1: internal state output enabled

Internal state output address
#############################

    ``/mcv/auralizationoutput/internalstateoutputaddress s``

    :s: address to send state output to as a string. e.g. "127.0.0.1"

Internal state output port
##########################

    ``/mcv/auralizationoutput/internalstateoutputport i``

    :i: port to send state output to as an int. e.g. 12345
 

Debug - by Output of Internal State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    **stage 2**

The visualiser should send be able to send its internal state out over OSC, for debug purposes

Output all the internal state for Auralization, plus:
 * position of all boids
 * velocity of all boids

OSC output format to be established

Internal state output toggle
############################
    
    ``/mcv/debugoutput/internalstatetoggle i``
    
    :0: no internal state output (default)

    :1: internal state output enabled

Internal state output address
#############################

    ``/mcv/debugoutput/internalstateaddress s``

    :s: address to send state output to as a string. e.g. "127.0.0.1"

Internal state output port
##########################

    ``/mcv/debugoutput/internalstateport i``

    :i: port to send state output to as an int. e.g. 12345

Generic Debug
~~~~~~~~~~~~~~~~~~~

These messages give arbitrary float values that should be visualised when in debug mode

visual toggle
#############

    **stage 2**

    ``/mcv/debug/visualtoggle i``
    
    :i: * 0 => no debug visual
        * 1 => debug visual enabled

        should create some kind of representation of 3 floating point attributes, each in the range -1 to 1.
            For example:
                :attribute 1: sphere colour
                :attribute 2: sphere blink/flash rate
                :attribute 3: sphere size

    ``/mcv/debug/visualvalues f f f``

    :f: arbitrary float attribute 1
    :f: arbitrary float attribute 2
    :f: arbitrary float attribute 3


Future - Stage to be established
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Aesthetic settings
##################

To be established in detail at a later date

Set a relative or absolute path to indicate a source for textures to be used for the visual (mcv should be able to reload textures at runtime).

This may be extended to boid models (i.e. mesh data)




Eye Tracker
###########

*Screen coordinate system is x and y in the range 0-1 with 0,0 at bottom, left*

Point of Gaze:

    ``/mcv/eyetrack/pog/left f f i``

    :f: x coordinate of point of gaze of left eye
    :f: y coordinate of point of gaze of left eye
    :i: boolean flag is this point of gaze is valid

    ``/mcv/eyetrack/pog/right f f i``

    :f: x coordinate of point of gaze of right eye
    :f: y coordinate of point of gaze of right eye
    :i: boolean flag - this point of gaze is valid

Fixation:

    ``/mcv/eyetrack/fixation f f f f i i``

    :f: x coordinate of fixation 
    :f: y coordinate of fixation
    :f: fixation start time (seconds from start of tracker)
    :f: fixation duration (so far) (seconds)
    :i: fixation ID
    :i: boolean flag - fixation is valid

Distance:

    ``/mcv/eyetrack/distance/left f i``

    :f: pupil distance of left eye (unitless, from calibration position)
    :i: boolean flag - distance is valid

    ``/mcv/eyetrack/distance/right f i``

    :f: pupil distance of right eye (unitless, from calibration position)
    :i: boolean flag - distance is valid

Debug:

    ``/mcv/eyetrack/debug i``

    :i: boolean flag of whether to visualise eyetrack data (for debug)

Further stages
--------------

Illusions / Tricks
~~~~~~~~~~~~~~~~~~

We could subtle modify parts of the scene where the user is not looking.

We could less subtly modify large parts of the scene when the user in blinking.

