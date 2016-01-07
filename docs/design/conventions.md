
This document outlines the code conventions that all programmers must follow while working on this project.



## Code 

* Wx GUI

    * All WX gui elements are coded using MVC conventions.
    
        * View File - contains **only** the logic necessary for displaying the GUI element or form
        * Controller File - contains **all** backend logic for the forms defined in the view
        * Model - currently not being used

* File Naming (MVC)

    - controller files 
        - *ShortDescription* + **Ctrl**
        - e.g. `ConsoleCtrl`, `DirectoryCtrl`
        
    - view files
        - *ShortDescription* + **View**
        - e.g. `ConsoleView`, `DirectoryView`

* Class Naming
    - camelCased with the first letter always lowercase
    - `myClass`

* Function Naming
    
    - public `myFunction`
        - camelCased with the first letter always lowercase
    
    - private function `_myFunction`
        - camelCased with the first letter always lowercase
        - preceded by an underscore ( `_` )
        
* Variable Naming

    - private variables:  `self.__my_private_var`
        - consist of a short description, underscore separated ( `_` )
        - preceded by a double underscore ( `_ _` )
        - can only be defined at the **class level**
        
    - public variable `my_public_var`
        - consist of a short description, underscore separated ( `_` )
        
* GIT
    * Commits
        - Always include issue number in commit message, e.g. [#123] (if applicable)
        - Commits should only contain files pertaining to a single issue 
        - Incremental commits are always better
        
    * Branches
        - Branch naming follows the version naming convention `major_minor_sprint`, e.g. `0.1.5`
        - New branches are created for **every** sprint
        - New branches are created for temporary/testing development
        - Branches are merged via pull requests
        
    * NEVER USE THE FOLLOWING COMMANDS
        - `git push --force`
        
* Logging 
    
    * Anything that breaks the application must be entered into the log
    
    * All errors must be prefixed by the class and function names, and include an exception messeage if applicable
        - `elog.error("Error myClass.testfunction: Something broke %s" % e)` 
        - `elog.critical("Error myClass.testfunction: Something broke %s" % e)` 
        - `elog.warning("Error myClass.testfunction: Something broke %s" % e)` 
    
    
    
    
    
    
    
    
    
    
    
    
    
  