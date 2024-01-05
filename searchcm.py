import sys
import signal
import urllib3.exceptions

from kubernetes import client, config
from kubernetes.client.rest import ApiException

def handler(signum, frame):
        print("")
        exit(1)

def cm_searching(val_to_search):
    # Kubernetes config load from kubeconfig
    config.load_kube_config()

    # Kubernetes API instance creation
    v1 = client.CoreV1Api()

    # Get all cm from all ns
    try:
        configmaps_list = v1.list_config_map_for_all_namespaces(watch=False,pretty=True,timeout_seconds=5)
    except ApiException as e:
        print("Exception when calling CoreV1Api->list_config_map_for_all_namespaces: %s\n" % e)
    except urllib3.exceptions.MaxRetryError:
        print("Timeout Exception reaching the API server...\n")
        exit(1)

    # Search in all cm
    for configmap in configmaps_list.items:
        namespace = configmap.metadata.namespace
        name = configmap.metadata.name

        if configmap.data is not None:
            # Get data from cm
            configmap_data = configmap.data

            # check if searched value is there
            for key, value in configmap_data.items():
                if val_to_search in value:
                    print(f"=========> Found in ConfigMap '{name}' in Namespace '{namespace}', key: '{key}', value: '{value}'")

if __name__ == "__main__":

    signal.signal(signal.SIGINT, handler)

    if len(sys.argv) > 1:
        searched_value = sys.argv[1]
        print(f"\nSearching for '{searched_value}' in ConfigMaps\n\n")
        cm_searching(searched_value)
    else:
        print(f"\nERROR: Need at list a string value to search for...\n")
