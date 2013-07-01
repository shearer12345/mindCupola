MindCupola Auralizer Specification
=======================================

:Short name:
    mca

:version:
    1.0

:authors:
    John Shearer
    
    Brigitta Zics    

:date:
    Friday February 22nd 2013

OSC messages Auralization
-------------------------

The Auralizer should respond to OSC messages from the Visualiser about the state of the visualisation. You can choose what port you want to listen on - as long as it's not port 7000 or 4242 (as they are already being used).


boid type
~~~~~~~~~
  ``/mca/boidType s``

:s: boidType - selected from

  * ``amoeba`` - slow, drifting. emotion == apathy
  * ``fish`` - spiral. emotion == boredom
  * ``insect`` - random motion, fast. emotion == anxiety
  * ``bird`` - best state, active state, directed. emotion == flow/balance

interaction state
~~~~~~~~~~~~~~~~~

  ``/mca/interactionState s``

:s: string representing the interaction state selected from below

  * ``ambient`` - no user, trigger leaving sound effect 
  * ``entering`` - user present, cupola is lowering, trigger big entry sound effect
  * ``waitingForEyes`` - user present, (re)trigger waiting sound effect
  * ``calibrating`` - user present, trigger calibration sound effect
  * ``running`` - user present, trigger big explode sound effect

calibration point
~~~~~~~~~~~~~~~~~

  ``/mca/calibrationTarget i``
  
:i: int representing which calibration point is presently being calibrated. In range [0,9] inclusive

  *should ping or equiv when the calibration target changes (which should be the only time you get this message)*

calibration result
~~~~~~~~~~~~~~~~~~

  ``/mca/calibrationResult i``
  
:i: int representing whether the calibration just finished was successful or not, where 0==notSuccessful and 1==successful

  *should drive a sound effect when notSuccessful*

pupilVisibility
~~~~~~~~~~~~~~~

  ``/mca/pupilsVisible i``

:i: int representing if both pupils are visible where 0==False (not visible) and 1==True (both visible)


fan state
~~~~~~~~~

  ``/mca/fanState i``

:i: int representing the fan state where 0==off and 1==on


heater state
~~~~~~~~~~~~

  ``/mca/heaterState i``

:i: int representing the fan state where 0==off and 1==on

predators
~~~~~~~~~

  ``/mca/predatorCount i``

:i: int representing the number of predators in the system

special effect triggered
~~~~~~~~~~~~~~~~~~~~~~~~

  ``/mca/specialEffectTriggered s``

:s: string representing a special (visual) effect that has just been triggered, selected from below, will send 'None' when effect stops, but timer-based audio effect is fine

  * ``none`` - no effect active
  * ``matrixEffect`` - freezes the particle system
  * ``blurLookAtLocation`` 
  * ``boidsFormingShape``

expect the audio effects to continue for some amount of time (say 20seconds) and then revert to normal

flock speed
~~~~~~~~~~~

  ``/mca/flock/speed f``

:f: float representing the flock speed, in range [0,1] - 0 is stopped, 1 is maximum speed

flock attractor location
~~~~~~~~~~~~~~~~~~~~~~~~

  ``/mca/flock/attractorLocation f f``

:f: float representing the X component of the attractor location (which is also the eye-look location), in range [-1,1], so [0,0] is center of screen

:f: float representing the Y component of the attractor location (which is also the eye-look location), in range [-1,1], so [0,0] is center of screen
