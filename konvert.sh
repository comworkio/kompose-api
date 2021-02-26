#!/bin/bash

filename="${1}"
version="${2}"
provider="${3}"

provider_opt=""
[[ $provider ]] && provider_opt="--provider ${provider}" 

kompose-${version} ${provider_opt} convert -f "${filename}" -o "${filename}.k8s.yml"

cat "${filename}.k8s.yml"

rm -rf "${filename}" "${filename}.k8s.yml"
