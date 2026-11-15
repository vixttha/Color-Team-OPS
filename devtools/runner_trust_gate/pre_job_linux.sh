#!/bin/bash
# INSTALLATION TEMPLATE. Admin must copy outside checkout, inspect immutable absolute paths,
# set ACTIONS_RUNNER_HOOK_JOB_STARTED in protected runner-service environment.
set -euo pipefail
exec /usr/bin/timeout --signal=TERM --kill-after=2s 15s /usr/bin/python3 -I -B /opt/color-team-ops/runner-gate/admission.py