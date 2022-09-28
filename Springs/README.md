This is a physics simulation of a general 1-dimensional chain, of N point like masses connected with springs. I wrote this simulation, before giving it as the final project assignment for the python course I was the TA.
The repository is pretty messy at the moment. Sorry :)

An animation using pygame module can be shown by running Animation.py . It is done after running a simulation, which is writing coordinates text file. The animation code reads it and makes a peroidic animation.

The simulation itself is N_oscillators.py file! 
There are also some other versions of it..

The configuration of the simulation is set by number of parameters, which are being read from a given structured pair of files:
input_initState.json, input_parameters.json
where the first includes the given initial state of each spring oscilator, and the second includes global constant variables, that defines the setup.

I'm running this code by given an integer number from 1-8, which chooses the pair of json files I want to use. So for example, running:
python N_oscillators.py 2
will use input_initState2.json, input_parameters2.json pair files.

A detailed description, can be found in "Springs Oscillators Project.pdf" and "Oscillators and waves theory.pdf".
