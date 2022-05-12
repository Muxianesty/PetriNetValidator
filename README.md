# PetriNetValidator

<p align="left"> 
    <strong>
    This work is being done and updated accordingly 
    as a course project at HSE University (Moscow, Russia)
    </strong>
</p>

<p> 
The project allows its users to validate two Workflow Petri net models' 
(imported from .pnml-files) behaviour by checking compliance 
of the second model (typically, a multi-agent system net) with the first one
(the interface net) using property-preserving transformations 
("Fusion of Parallel Places", "Fusion of Parallel Transitions" and
"Local Transition Elimination" abstraction rules and their refinement
counterparts).
</p>
<p>
The way of rules' application to the second model in general cases 
is deduced via the difference in the amounts of transitions and places
in each respective model - it might be either strictly abstraction
(reduction) or strictly refinement (extension). In case the amounts 
are equal to each other,the program checks whether the models 
are isomorphic by using a custom hash-function, applied to the arcs 
of each respective model.
</p>
<p>
Whenever the main.py script executes, it uses two input arguments from
the terminal which represent the absolute (or relative) paths to the
.pnml-files of each respective model. In the directory relative to the script
execution the "Output"-subdirectory is created, which is going to store
subdirectories for each pair of used files - the subdirectories names have a format
"{file1}-{file2}", where "file1" and "file2" resemble the filename for each
respective .pnml-file without the extension. Initially, the subdirectory will contain 
"interface.png" and "net.png", which represent two original models, while at the end of
program's execution a file "converted.png" is also added to the subdirectory, showing
the final view of the transformed initial second model.
</p>
<p>
For each executed transformation, two .png-files are created to depict the local
transformation of the second net ("{i}-1.png" and "{i}-2.png", where "i" is the number
of the transformation starting with 1; "-1" and "-2" suffixes represent the initial and final
views on the model respectively). 
</p>
<strong> Installation (requires up to 500MB of free space): <br> </strong>
<ol>
    <li> Download a Python3 interpreter; </li>
    <li> Download (or git-clone with <code>git clone https://github.com/Muxianesty/PetriNetValidator</code>)
         and unzip this repository if needed; </li>
    <li> Download and install GraphViz-executables 
         (<a href="https://graphviz.org/download/">here</a>); </li>
    <li> Download and install a Petri net editor if needed
         (we recommend using WOLFGANG -
         <a href="https://github.com/iig-uni-freiburg/WOLFGANG">here)</a>; </li>
    <li> Setup a Python virtual environment in the downloaded repository
         by using <code>python -m venv {env_name} </code>, with "env_name" as your
         environment directory name and activate it with { </li>
    <li> Download dependencies with "pip" (from virtual environment): 
         <code>pip install -r libs.txt</code> or just <code>pip install pm4py</code> as
         pm4py-library is the only main library being used in the project </li>
</ol>

<strong> Execution: <br> </strong>
<code>{env_name}\Scripts\python3 main.py {f1} {f2}</code> for Windows <br>
<code>{env_name}/bin/python3 main.py {f1} {f2}</code> for Linux <br>
where "env_name" is the name of the virtual environment directory, 
"f1" and "f2" are absolute/relative paths to the files of the two Workflow Petri net models.

