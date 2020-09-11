import os
import shutil
import time

import pytest
import requests

from nearuplib.nodelib import restart_nearup, setup_and_run, stop_nearup
from nearuplib.constants import LOGS_FOLDER

NEAR_DIR = '~/.near'
NEARUP_DIR = '~/.nearup'

NEARUP_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../nearup',
)


def cleanup():
    if os.path.exists(NEAR_DIR):
        shutil.rmtree(NEAR_DIR)

    if os.path.exists(NEARUP_DIR):
        shutil.rmtree(NEARUP_DIR)

    if os.path.exists(LOGS_FOLDER):
        shutil.rmtree(LOGS_FOLDER)


def setup_module(module):  # pylint: disable=W0613
    cleanup()

    if not os.path.exists(LOGS_FOLDER):
        os.makedirs(LOGS_FOLDER)


def teardown_module(module):  # pylint: disable=W0613
    cleanup()


def test_nearup_still_runnable():
    setup_and_run(binary_path='',
                  home_dir='',
                  init_flags=['--chain-id=betanet'],
                  boot_nodes='',
                  verbose=True,
                  no_watcher=True)
    time.sleep(10)

    resp = requests.get('http://localhost:3030/status')
    assert resp.status_code == 200
    assert resp.text

    stop_nearup()
    time.sleep(10)

    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get('http://localhost:3030/status')

    restart_nearup('betanet', NEARUP_PATH, watcher=False)
    time.sleep(10)

    resp = requests.get('http://localhost:3030/status')
    assert resp.status_code == 200
    assert resp.text

    stop_nearup()
    time.sleep(10)

    with pytest.raises(requests.exceptions.ConnectionError):
        requests.get('http://localhost:3030/status')