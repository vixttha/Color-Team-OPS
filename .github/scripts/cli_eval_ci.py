"""Self-hosted CI only; no inference, installs, packaging, or publication."""
import os
import subprocess
import sys
import tempfile

import jsonschema  # Required preinstalled dependency; do not install on owner runner.

assert os.environ['RUNNER_NAME'] == os.environ['EXPECTED_RUNNER']
assert subprocess.check_output(['git','rev-parse','HEAD']).decode().strip() == os.environ['EXPECTED_SHA']
with tempfile.TemporaryDirectory(prefix='cto-cli-ci-', dir=os.environ['RUNNER_TEMP']) as scratch:
    env = dict(os.environ, GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.autocrlf', GIT_CONFIG_VALUE_0='false')
    subprocess.run(['git','clone','--no-hardlinks','--no-checkout','.',scratch], check=True, env=env)
    subprocess.run(['git','checkout','--detach',os.environ['EXPECTED_SHA']], cwd=scratch, check=True, env=env)
    subprocess.run([sys.executable,'-B','-m','unittest','discover','-s','tests','-p','test*.py'], cwd=scratch, check=True, env=env)
    assert not subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=all'], cwd=scratch).strip()
print('CLI_DEV_REGRESSION_PASS', os.environ['EXPECTED_SHA'], os.environ['RUNNER_NAME'])
