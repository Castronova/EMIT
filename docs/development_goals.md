
# Development Goals

**Title:** Release 1.1 
**Release Date:** January 1, 201
**Key functionality:**

---

***Summary***
Release 1.1 will serve to clean up the graphical user interface, specifically the functionality pertaining to coupled model creation and execution.  Tools for creating and modifying links will clearly display all the information that the user will need to establish linkages between models.  In addition, remote time series data previewing will be made available via dynamic plot generation.  This functionality will also extend to provide visualization of simulation outputs.  Finally, time-step model simulation control will be added to the EMIT engine.  This will enhance the existing feed-forward simulation control and it will be demonstrated using Caleb's SWMM model.  In order to accomplish this, spatial and temporal interpolation classes must be finished.

***GUI***
1.) Clean drawing artifacts in the composition window (e.g. arrow and box drawing errors).

2.) Remove all unnecessary (and not fully implemented) gui elements, e.g. the navigation toolbar.

3.) Fix composition saving and loading

4.) Provide basic time series and simulation results plotting.

5.) Implement database connection storage in a secure manner.

***Backend***
1.) Implement time-stepping simulation control.  This is necessary to incorporate Caleb's SWMM model into the EMIT framework.  It is anticipated that this will be useful for iUTAH model integration as well.  EMIT will have two distinct simulation control mechanisms, feed forward and time-step.  These exist as separate control options that cannot be combined together in a single simulation. Right now the control mechanism is determined by the interface implemented by the model.

2.) Implement spatial nearest neighbor interpolation 

3.) Implement temporal nearest neighbor interpolation

4.) Tie spatial and temporal interpolations into both of the run control mechanisms (i.e. feed forward, time-step)

5.) Implement Caleb's coupled SWMM model as an example of how the time-stepping control works.

6.) Add a wrapper interface to support CSV data files

7.) Clean all wrappers, i.e. remove abandoned code, make simulation execution standard.

---

## Use-cases

### Comprehensive storage of simulation calculations
**Goal:**  

Coupled model systems enable disparate software code to be integrated into a single simulation by sharing output calculations during the run phase of a simulation.  A common issue among model coupling software is storing simulation calculations in an archivable and coherent manner.  Typically, calculations are stored in proprietary formats, in which a single coupled model may contain a variety of model output files consisting of a variety of formats.  As a community we need a general purpose system for storing the calculations of coupled model systems.  

**To Achieve Success** 

* Develop storage system capable of representing many different types.  To do this, it must be designed in a generic manner. 
 
* Develop software to provide a mechanism for analyzing data post simulation.  This should provide the functionality for discovering, analyzing, and sharing datasets based on simulation instance.

* Develop a coupled modeling tool that leverages this data storage system for archiving results and calculations during model simulations.  This modeling system should also be used to read data calculations and feed them into coupled models.