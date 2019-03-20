#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""helper functions for testing graypy

These functions are used for both the integration and unit testing.
"""

import os
import logging
import pytest

from graypy import GELFUDPHandler, GELFTCPHandler, GELFTLSHandler,  \
    GELFTcpHandler, GELFHTTPHandler


TEST_CERT = os.path.join("tests", "config", "localhost.cert.pem")

KEY_PASS = "secret"

TEST_TCP_PORT = 12201
TEST_UDP_PORT = 12202
TEST_HTTP_PORT = 12203
TEST_TLS_PORT = 12204

if not os.path.isfile(TEST_CERT):
    TEST_TLS_GELFTcpHandlers = []
else:
    # if we have a valid testing cert we can also test with TLS
    TEST_TLS_GELFTcpHandlers = [
        GELFTcpHandler("localhost", TEST_TLS_PORT, tls=True, tls_cafile=TEST_CERT),
        GELFTcpHandler("localhost", TEST_TLS_PORT, tls=True,  tls_server_name="localhost", tls_cafile=TEST_CERT),
        GELFTcpHandler("127.0.0.1", TEST_TLS_PORT, tls=True, tls_server_name="localhost", tls_cafile=TEST_CERT),
    ]


@pytest.fixture(
    params=[
        GELFTCPHandler("127.0.0.1", TEST_TCP_PORT),
        GELFTCPHandler("127.0.0.1", TEST_TCP_PORT, extra_fields=True),
        GELFTCPHandler("127.0.0.1", TEST_TCP_PORT, extra_fields=True, debugging_fields=True),
        GELFTLSHandler("localhost", TEST_TLS_PORT),
        GELFTLSHandler("localhost", TEST_TLS_PORT, validate=True, ca_certs=TEST_CERT),
        GELFTLSHandler("127.0.0.1", TEST_TLS_PORT),
        GELFTLSHandler("127.0.0.1", TEST_TLS_PORT, validate=True, ca_certs=TEST_CERT),
        GELFHTTPHandler('127.0.0.1', TEST_HTTP_PORT),
        GELFHTTPHandler('127.0.0.1', TEST_HTTP_PORT, compress=False),
        GELFUDPHandler("127.0.0.1", TEST_UDP_PORT),
        GELFUDPHandler("127.0.0.1", TEST_UDP_PORT, compress=False),
        GELFUDPHandler("127.0.0.1", TEST_UDP_PORT, extra_fields=True),
        GELFUDPHandler("127.0.0.1", TEST_UDP_PORT, extra_fields=True, compress=False),
        GELFUDPHandler("127.0.0.1", TEST_UDP_PORT, extra_fields=True, debugging_fields=True),
        GELFUDPHandler("127.0.0.1", TEST_UDP_PORT, extra_fields=True, debugging_fields=True, compress=False),
        GELFTcpHandler("127.0.0.1", TEST_TCP_PORT),
        GELFTcpHandler("127.0.0.1", TEST_TCP_PORT, extra_fields=True),
        GELFTcpHandler("127.0.0.1", TEST_TCP_PORT, extra_fields=True, debugging_fields=True),
    ] + TEST_TLS_GELFTcpHandlers
)
def handler(request):
    return request.param


@pytest.yield_fixture
def logger(handler):
    logger_ = logging.getLogger("test_logger")
    logger_.addHandler(handler)
    yield logger_
    logger_.removeHandler(handler)


@pytest.yield_fixture
def formatted_logger(handler):
    logger_ = logging.getLogger("formatted_test_logger")
    handler.setFormatter(logging.Formatter("%(levelname)s : %(message)s"))
    logger_.addHandler(handler)
    yield logger_
    logger_.removeHandler(handler)
