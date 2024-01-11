import sys, getopt
import signal
import urllib3.exceptions

from kubernetes import client, config
from kubernetes.client.rest import ApiException

def handler(signum, frame):
        print("")
        exit(1)

def cm_searching(val_to_search,verbosity):
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
                    if verbosity is False:
                        print(f"- Found in ConfigMap '{name}' in Namespace '{namespace}'")
                    else:
                        print(f"- Found in ConfigMap '{name}' in Namespace '{namespace}', key: '{key}', value: '{value}'")

def main(argv):
    signal.signal(signal.SIGINT, handler)

    searched_value = None
    verbose = False

    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(argv,"hs:v",["--search=","--verbose"])
        except getopt.GetoptError as e:
            print(e)
            print(f"\nUsage: searchcm -s <value to search for> [-v]\n")
            sys.exit(1)

        for opt, arg in opts:
            if opt == '-h':
                print ('searchcm -s <value to search for> [-v]')
                sys.exit()
            elif opt in ("-s", "--search"):
                searched_value = arg
                print(f"\nSearching for '{searched_value}' in ConfigMaps\n")
            elif opt in ("-v", "--verbose"):
                verbose = True
            else:
                print(f"\nWrong parameters...\nUsage: searchcm -s <value to search for> [-v]\n")

        if searched_value is not None:
            cm_searching(searched_value,verbose)
    else:
        print(f"\nERROR: Need at list a string value to search for...\nUsage: searchcm -s <value to search for> [-v]\n")


if __name__ == "__main__":
    main(sys.argv[1:])

