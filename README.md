# searchcm

### About
This tool comes without pretention, not sure if this really worth a plugin and useful for others.

Until now we were looking through our gitlab and with classical 'kubectl get cm' trials.
Decided to create a simple helper script to do this. 
Now I have experimented with kubectl plugins, so I converted the script to a pyhon plugin.

Example usage:
kubectl searchcm -s valuetosearch 

### Installation
version=v0.0.1 ;wget -qO- https://github.com/pbletard/searchcm/releases/download/$version/searchcm.tar.gz | sudo  tar -xzv -C /usr/local/bin/ ;sudo mv /usr/local/bin/searchcm /usr/local/bin/kubectl-searchcm
