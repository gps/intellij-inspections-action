#!/bin/sh

/opt/idea/bin/inspect.sh ${GITHUB_WORKSPACE}/build.gradle ${GITHUB_WORKSPACE}/Project_Default.xml ${GITHUB_WORKSPACE}/target/idea_inspections -v2

python3 /analyze_inspections.py -i ${GITHUB_WORKSPACE}/target/idea_inspections > ${GITHUB_WORKSPACE}/target/idea_inspections/diagnostics.json
