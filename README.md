# searchcm

This tool comes without pretention, not sure if this really worth a plugin and useful for others.

Until now we were looking through our gitlab and with classical 'kubectl get cm' trials.
Decided to create a simple helper script to do this. 
Now I have experimented with kubectl plugins, so I converted the script to a pyhon plugin.

Example usage:
kubectl searchcm -s valuetosearch 
