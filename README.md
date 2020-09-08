# Testing visual graph in Actions

This repo runs a script on main.yml to extract a visual graph of the workflow. 

To generate a visual graph, paste your workflow in main.yml. On a push commit, visualizer.yml parses the yaml in main.yml, generates a visual graph, and uploads it as an artifact. The main.yml doesn't need to run for the visualizer to extract the graph.

There are a few settings that can be adjusted. However, I recommend keeping with the default options for now. In the default settings, matrix nodes are shown but grouped. Also, parallel nodes are grouped to reduce the cognitive load on the audience.  


