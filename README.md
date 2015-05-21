EMIT
====

Environmental Model Integration Project (EMIT)

**Goals of this project**

1. Data as a model

> Technology for building coupled models within the water resource domain has been advancing at a rapid pace.  Many modeling framworks have been developed (e.g. OpenMI, CSDMS, OMS, etc) that control the flow of data between model components during a simulation.  These efforts have largely focused on establishing software interfaces for *componentizing* scientific calculations such that they can receive input data and supply output data during a simulation.  However, there has been a lack of emphasis on closing the gap between observed and simulated data, and component simulations.  One objective of this project is to investigate how observed and simulation data can be integrated seamlessly into component-based model simulations.  

2. Coupled modeling workflow

> Coupled modeling platforms typically rely upon a single data passing workflow which is defined by a coordination mechanism.  Some utilize a feed-forward approach (e.g. OMS, CSDMS) while others use a pull driven approach (e.g. OpenMI).  Each offers its own benefits, however rarely do we ever encounter a set of models for which a single workflow is ideal. For instance, closed-source models can be coupled with other computations via reading and writing input/output files, but are unable to interact with others at individual time-steps (unless specifically designed to).  Similarly, sometimes model are coupled along shared boundary conditions which require time-step iterations to converge on a solution.  Therefore, a second objective of this work is to investigate methods for utilizing multiple workflows within a single coupling framework as well as within a single simulation. 

3. Platform and Language Compatibility

> 
