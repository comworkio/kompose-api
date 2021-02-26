#!/bin/bash

filename="${1}"
provider="${2}"

cat "${filename}"
rm -rf "${filename}"
