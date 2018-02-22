#!/usr/bin/env python3
import os
from litmus.core.util import load_yaml
from litmus.core.manager import manager
from litmus.helper.helper import tizen_snapshot_downloader as downloader
from litmus.helper.helper import install_plugin_from_git
from litmus.helper.tests import add_test_helper


def main(*args, **kwargs):

    # init manager instance
    mgr = manager(*args, **kwargs)

    # init working directory
    mgr.init_workingdir()

    # get projectinfo
    project_info = load_yaml('conf_mobile.yaml')
    binary_urls = project_info['binary_urls']
    plugin_info = project_info['plugin_info']

    try:
        version = kwargs['param'][0]
    except (IndexError, TypeError):
        version = None

    dut = mgr.acquire_dut('standalone_tm1', max_retry_times=180)
    dut._booting_time = 40

    if project_info['flashing'] is True:
        # download binaries from snapshot download server
        filenames = []
        for url in binary_urls:
            filenames.extend(downloader(url=url,
                                        version=version))
        # flashing binaries to device.
        dut.flash(filenames)

    if project_info['installing_plugin'] is True:
        # install plugins
        install_plugin_from_git(dut,
                                url=plugin_info['url'],
                                branch=plugin_info['branch'],
                                script=plugin_info['script'],
                                commitid=plugin_info['commitid'])

    # turn on dut.
    dut.on()

    # run helper functions for testing.
    if not os.path.exists('result'):
        os.mkdir('result')

    testcases = load_yaml('tc_mobile.yaml')
    add_test_helper(dut, testcases)
    dut.run_tests()

    # turn off dut.
    dut.off()

    # release a device
    mgr.release_dut(dut)
