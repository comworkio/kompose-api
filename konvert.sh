#!/bin/bash

filename="${1}"
version="${2}"
provider="${3}"
ns="${4}"
apply="${5}"

provider_opt=""
[[ $provider && $provider != "null" ]] && provider_opt="--provider=${provider}" 

ns_k8s_opt=""
[[ $ns && $ns != "null" ]] && ns_k8s_opt="-n ${ns}"

kompose-${version} ${provider_opt} convert -f "${filename}" -o "${filename}.k8s.yml"

if [[ $apply && $apply != "null" && $ENABLE_KUBECTL_APPLY && $ENABLE_KUBECTL_APPLY != "false" ]]; then
    cat "${filename}.k8s.yml" | kubectl ${ns_k8s_opt} apply -f - > "${filename}.log" 2>&1
    cat "${filename}.log"
else 
    cat "${filename}.k8s.yml"
fi

rm -rf "${filename}" "${filename}.k8s.yml" "${filename}.log"
