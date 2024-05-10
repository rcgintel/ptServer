
# Primetime Server

this set of scripts are for enabling a sequential access to primetime server to generate primetime reports there by reducing the primetime requests and infrastructure usage
## Documentation

[Documentation](https://github.com/rcgintel/ptServer)

given the number of license and machines that gets occupied by users to check the timing of blocks 

- Number of sections/Top per project : 8
- Number of corners per project  : 8
- Number of runs per month : 10
- Number of PEO's per project : 50
- Theoritically number of license and infrastructure used is significantly high. 


#

PEO's normally use primetime just for a few minutes and later dont exit the tool or release the compute resource

#

for every section run if the PEO can access the primetime terminal?

# 

we have created a simple tool "ptServer" in python 

- Why Python?

       1. We are using a centralised database "MariaDB" for sending the commands to our PT ptServer
       2. TCL is not ideal for database interface
       3. Easy to understand can control and handle the execution efficiently
       4. Enhance the features set and implement additional reporting which need multiple report merging

- CLI Tool

        1. This is to be used by the PEO to access the primetime ptServer
        2. written in python 

Commands

    > LIST of available commands in the CLI tool
 
 <details> Commands List 
        
|SlNo| Command | Description |
|----:|-----|-----------|
|1|get_cells | same as PT command|
|2|get_pins  | same as PT command|
|3|get_lib_cells| same as PT command|
|4|get_lib_pins | same as PT command|
|5|get_attributes | same as PT command|
|6|report_timing | same as PT command|
|7|report_delay_calculation | same as PT command|
|8|set_var | this command will set a variables with data which is set once and can be used in the entire server session in all available corners|
|9|man |same as PT command|
|10|load_corner| load a corner that is available, all corners are shown in show_corner|
|11|show_corner| this command will show all the available corners that can be accessed from the current session|
|12|current_corner| this will show which corner data is getting displayed|
|13|show_report| this is a internal command that displays the report that is generated|
|14|set_app_var| list of variables that can be set by the user |
|15|get_app_var| value of the variable |
|16|list_app_var| show the list of variables that can be updated using set_app_var|
|17|set_user_location| this is the location where the reports are dumped|
|18|get_user_location| show the user location where the reports are dumped|
|19|load_work_week| link the work week that needs to be accessed |
|20|show_work_week| show all the available work week that can be accessed|
|21|current_work_week| show the current work week that is being accessed|
|22|load_block| load the block on which we need to be working|
|23|show_block| show all the available blocks which we are currently active|
|24|current_block|which is the current block on which we are running|
|25|show_info| show the block name work week and the corner which we are accessing|
|26|history| will give the list of commands that we have executed|
|27|compare_timing| we can compare 2 timing reports different work week and corner (incomplete)|
</details>

#

- Server Tool

        1. This is to be used by SPEO "Section level PT user"
        2. this is open primetime terminal depending on the spec writen in the code

- GUI

        1. GUI is enabled basic only

- Database 

        1. Database used "MariaDB"
        2. Table for taking the command
        3. Table for setting the variables
        4. Table for tracking the machines


## Authors

- Developer [@rcg](https://github.com/rcgintel)
- CoDeveloper [@Ajith Vishnu](https://github.com/vajith1999)
- All of code reviewers and users


## Contributing

Contributions are always welcome!

See `contributing.md` for ways to get started.

Please adhere to this project's `code of conduct`.


## FAQ

#### Can this be done in TCL only ?

There can be different approaches to solve this problem, we have choosen this which is explained before

#### Can we contribute to this code ?

This is split into developer and user based contribution 
for developer based contribution please contact ramapriya.c.g@intel.com 

for user based contirbution please see contributing page


## Roadmap

- Compare timing reports
- AI based reporting and NLP based data mining


## Tech Stack

**Client:** Python, rich

**Server:** Python, TCL, SQLconnector

