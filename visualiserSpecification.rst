Mind-Cupola Visualiser Specification
=======================================


:Short name:
    mcv

:version:
    1.1

:authors:
    John Shearer

:date:
    Tuesday July 30th 2013

Overview
--------

This document provides details on the mindCupolaVisualiser (given as *mcv* herein). Specifically, it provides:
    * `Overview`_
    * `Interaction Design`_
    * `Technical overview`_
    * `Technical requirements`_
    * `Aesthetic`_ demands for the implementation
    * `OSC API`_ for mcv

The mindCupolaVisualiser is intended to produce an immersive, flow inducing effect on people through smoothly moving, flocking boids that respond to both their eye-movements (measured outside *mcv*) and to a predicted (outside *mcv*) affective state.
The mindCupolaVisualiser itself needs only to respond to explicitly given inputs (detailed in the `OSC API`_, which are tied closely to the visualisation (abstracted away from their specific sources).

Interaction Design
------------------

From the user experience point of view it is important how we lead the user smoothly into the interaction. This connects with the aesthetic design, but also needs to support legibility of the system.

Focus on:
  Aesthetic
  Legibility
  Immersion

Interaction States
~~~~~~~~~~~~~~~~~~

Changes in Interaction State are notified to MCV through OSC messages ('/mcv/state') detailed below.

1) Cupola Empty (and up) - start state
    :Visualiser: boids moving, but out of focus
    
2) Cupola Lowering/Raising
    :Visualiser: as 1)
    
3) Waiting for Eyes
    :Visualiser: 	blank/dark screen (boids somewhat faded out)
    				highlighted to provide a pair of eyes,
    				to indicate to the user that the system is looking for their eyes

4) Calibrating
    :Visualiser: Show progressive calibration points - made up of all the boids together - zoom the camera out etc

5) Running
    :Visualiser: quite a lot of detail. eyes not visible => defocus

Technical overview
------------------

The mindCupolaVisualiser will be based on classical Reynolds-like boids (http://en.wikipedia.org/wiki/Boids)
  with a few variety of preset for different 'types' of boids
  and different overall behaviours

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

The mindCupolaVisualiser should listen for OSC on port 7000

See http://opensoundcontrol.org/spec-1_0 for Type Tags used below.

There are a variety of incoming OSC messages that mcv should handle, detail as follows:

``/mcv/fullscreen i``

  :i: whether the visualisation should be fullscreen. 0=No, 1=Yes
    
``/mcv/paused i``

  :i: whether the visualisation should be paused. 0=No, 1=Yes
    
``/mcv/sixteenByNine i``

  :i: whether the visualisation should be sixteenByNine or not (4by3). 0=No, 1=Yes
    
``/mcv/debug i``

  :i: whether the visualisation should dump debug information. 0=No, 1=Yes
    
``/mcv/blur f``

  :f: how blurred the scene should be. in range(0:1)
    
``/mcv/boidType i``

  :i: the boidType to use in the visualisation. Controls both their behaviour and look.

``/mcv/state i``

  :i: the present interaction state

``/mcv/attractorPosition f``

  :f: the x, y position of the attractor
    
``/mcv/calibrationTarget i``

    :i: which calibrationTarget is presently active - to drive the visual presentation of calibration points

``/mcv/predatorCount i``

    :i: how many predators should presently be active

``/mcv/pupilsVisible i``

    :i: whether the user's pupils are presently visible.  0=No, 1=Yes

``/mcv/migrateShapeNumber i``

    :i: which migrateShape to use. 0=>no migrate to shape

``/mcv/cohesiveDistance f``

    :f: tendency for boids to stay together. Smaller => Stronger

    