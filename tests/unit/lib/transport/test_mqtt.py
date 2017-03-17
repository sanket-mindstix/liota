# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------#
#  Copyright © 2015-2016 VMware, Inc. All Rights Reserved.                    #
#                                                                             #
#  Licensed under the BSD 2-Clause License (the “License”); you may not use   #
#  this file except in compliance with the License.                           #
#                                                                             #
#  The BSD 2-Clause License                                                   #
#                                                                             #
#  Redistribution and use in source and binary forms, with or without         #
#  modification, are permitted provided that the following conditions are met:#
#                                                                             #
#  - Redistributions of source code must retain the above copyright notice,   #
#      this list of conditions and the following disclaimer.                  #
#                                                                             #
#  - Redistributions in binary form must reproduce the above copyright        #
#      notice, this list of conditions and the following disclaimer in the    #
#      documentation and/or other materials provided with the distribution.   #
#                                                                             #
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"#
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE  #
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE #
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE  #
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR        #
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF       #
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS   #
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN    #
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)    #
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF     #
#  THE POSSIBILITY OF SUCH DAMAGE.                                            #
# ----------------------------------------------------------------------------#

import unittest
import os
import sys
import mock

from paho.mqtt.client import Client, MQTTMessage
from liota.lib.transports.mqtt import Mqtt
from liota.lib.transports.mqtt import MqttMessagingAttributes, QoSDetails
from liota.entities.edge_systems.dell5k_edge_system import Dell5KEdgeSystem
from liota.lib.utilities.identity import Identity
from liota.lib.utilities.tls_conf import TLSConf

# MQTT configurations
config = {}
execfile(os.path.dirname(os.path.abspath(__file__)) + '/conf/testMqttTransportsProp.conf', config)
connect_rc = 0
disconnect_rc = 0


# Monkey patched connect method of Paho client
def mocked_connect(self, *args, **kwargs):
    # Call on_connect method with connection established options connect_rc
    self.on_connect(self._client_id, self._userdata, None, connect_rc)


# Monkey patched disconnect method of Paho client
def mocked_disconnect(self):
    self.on_disconnect("test-client", None, disconnect_rc)


# Monkey patched Mqtt class constructor
def mocked_mqtt_init(self, *args, **kwargs):
    pass


# Monkey patched loop_start method of Paho client
def mocked_loop_start(self, *args, **kwargs):
    pass


# Monkey patched loop_start method of Paho client
def mocked_loop_stop(self, *args, **kwargs):
    pass


# Method to test the on message callback of the topic.
def topic_subscribe_callback(self, *args, **kwargs):
    pass


class MQTTTest(unittest.TestCase):
    """
    MQTT library unit test cases
    """

    def setUp(self):
        """Initialise the MQTT parameters"""

        # Broker details
        self.url = config["BrokerIP"]
        self.port = config["BrokerPort"]
        self.mqtt_username = config["mqtt_username"]
        self.mqtt_password = config["mqtt_password"]
        self.enable_authentication = config["enable_authentication"]
        self.client_clean_session = True
        self.protocol = config["protocol"]
        self.transport = config["transport"]
        self.connection_disconnect_timeout = config["connection_disconnect_timeout"]
        self.user_data = config["user_data"]
        self.clean_session_flag = config["clean_session_flag"]

        # Message QoS and connection details
        self.QoSlevel = config["QoSlevel"]
        self.inflight = config["inflight"]
        self.queue_size = config["queue_size"]
        self.retry = config["retry"]
        self.keep_alive = config["keep_alive"]

        # EdgeSystem name
        self.edge_system = Dell5KEdgeSystem(config['EdgeSystemName'])

        # TLS configurations
        self.root_ca_cert = config["root_ca_cert"]
        self.client_cert_file = config["client_cert_file"]
        self.client_key_file = config["client_key_file"]
        self.cert_required = config["cert_required"]
        self.tls_version = config["tls_version"]
        self.cipher = config["cipher"]

    @mock.patch.object(Mqtt, 'connect_soc')
    def test_mqtt_init(self, mock_connect):
        """
        Method to test the creation of Mqtt class object
        :param mock_connect: Mocked connect_soc method
        :return: None
        """

        # Mocked connect_soc method
        mock_connect.returnvalue = None

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport, self.keep_alive,
                           self.enable_authentication, self.connection_disconnect_timeout)
        # Check we are able to generate Mqtt class object
        self.assertIsInstance(mqtt_client, Mqtt, "Invalid Mqtt class implementation")

    @mock.patch.object(Mqtt, 'connect_soc')
    def test_mqtt_init_clean_session_false(self, mock_connect):
        """
        Method to test the creation of Mqtt class object
        :param mock_connect: Mocked connect_soc method
        :return: None
        """

        # Mocked connect_soc method
        mock_connect.returnvalue = None

        # Clean session flag as False
        self.client_clean_session = False

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport, self.keep_alive,
                           self.enable_authentication, self.connection_disconnect_timeout)
        # Check we are able to generate Mqtt class object
        self.assertIsInstance(mqtt_client, Mqtt, "Invalid Mqtt class implementation")

    def test_connect_soc_invalid_root_ca(self):
        """
        Method to test invalid root ca validation.
        :return: None
        """
        # Setting invalid root ca path
        self.root_ca_cert = "Invalid Root CA Path"
        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid root ca_certs
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_empty_root_ca(self):
        """
        Method to test empty root ca validation.
        :return: None
        """
        # Setting invalid root ca path
        self.root_ca_cert = ""
        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid root ca_certs
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_invalid_client_ca(self):
        """
        Method to test invalid client ca validation.
        :return: None
        """
        # Setting invalid client ca path
        self.client_cert_file = "Invalid Client CA Path"

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid client ca_certs
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_empty_client_ca(self):
        """
        Method to test empty client ca validation.
        :return: None
        """
        # Setting invalid client ca path
        self.client_cert_file = ""
        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid client ca_certs
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_invalid_client_key(self):
        """
        Method to test invalid client key validation.
        :return: None
        """
        # Setting invalid client key path
        self.client_key_file = "Invalid Client Key Path"

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid client key
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_invalid_client_cert(self):
        """
        Method to test invalid client key validation.
        :return: None
        """
        # Setting invalid client cert path
        self.client_key_file = ""

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid client cert
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_empty_client_key(self):
        """
        Method to test empty client key validation.
        :return: None
        """
        # Setting invalid client key path
        self.client_cert_file = ""
        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid client ca_certs
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_for_empty_username(self):
        """
        Method to test empty username validation.
        :return: None
        """

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, "", self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid client ca_certs
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_for_empty_password(self):
        """
        Method to test empty username validation.
        :return: None
        """

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, "",
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the ValueError for invalid client ca_certs
        with self.assertRaises(ValueError):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_connection_setup(self):
        """
        Method to test connection setup with connect_soc.
        :return: None
        """
        global connect_rc

        # Setting connection accepted flag
        connect_rc = 0

        # Mocked the connect and loop_start method of Paho library
        Client.connect = mocked_connect
        Client.loop_start = mocked_loop_start

        # Mocked the on_connect method of Mqtt class
        # Mqtt.on_connect = on_connect

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport,
                           self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

        # Check we are able to generate Mqtt class object
        self.assertIsInstance(mqtt_client, Mqtt, "Invalid Mqtt class implementation")

    def test_connect_soc_connection_timeout(self):
        """
        Method to test connection setup with connect_soc.
        :return: None
        """
        global connect_rc

        # Setting connection timeout flag
        connect_rc = sys.maxsize

        # Mocked the connect and loop_start method of Paho library
        Client.connect = mocked_connect
        Client.loop_start = mocked_loop_start
        Client.loop_stop = mocked_loop_stop

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the Exception for broker timeout
        with self.assertRaises(Exception):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_connect_soc_connection_refused(self):
        """
        Method to test connection setup with connect_soc.
        :return: None
        """
        global connect_rc

        # Setting connection refused flag
        connect_rc = 1

        # Mocked the connect and loop_start method of Paho library
        Client.connect = mocked_connect
        Client.loop_start = mocked_loop_start
        Client.loop_stop = mocked_loop_stop

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the Exception for broker timeout
        with self.assertRaises(Exception):
            Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                 self.client_clean_session, self.user_data, self.protocol, self.transport,
                 self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

    def test_mqtt_connection_over_only_root_ca_cert(self):
        """
        Method to test the implementation of connection_soc method for root_ca.
        :return: None
        """
        global connect_rc

        # Setting connection accepted flag
        connect_rc = 0

        # Mocked the connect and loop_start method of Paho library
        Client.connect = mocked_connect
        Client.loop_start = mocked_loop_start

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password, None, None)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport, self.keep_alive,
                           self.enable_authentication, self.connection_disconnect_timeout)
        # Check we are able to generate Mqtt class object
        self.assertIsInstance(mqtt_client, Mqtt, "Invalid Mqtt class implementation")

    @mock.patch.object(Mqtt, 'connect_soc')
    def test_client_clean_session_and_client_id_implementation(self, mock_connect):
        """
        Method to test the creation of Mqtt class object
        :param mock_connect: Mocked connect_soc method
        :return: None
        """

        # Mocked connect_soc method
        mock_connect.returnvalue = None

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport, self.keep_alive,
                           self.enable_authentication, self.connection_disconnect_timeout)
        # Check we are able to generate Mqtt class object
        self.assertIsInstance(mqtt_client, Mqtt, "Invalid Mqtt class implementation")

        client_id = mqtt_client.get_client_id()
        self.assertEqual("test-client", client_id, "Received invalid client-id, check the implementation.")

    def test_clean_disconnect_connection(self):
        """
        Method to test clean-connection disconnect.
        :return: None
        """
        global connect_rc, disconnect_rc

        # Setting connection accepted flag
        connect_rc = 0
        # Setting connection disconnect flag
        disconnect_rc = 0

        # Monkey patched connect, disconnect, loop_start and loop_stop methods of Paho library
        Client.connect = mocked_connect
        Client.disconnect = mocked_disconnect
        Client.loop_start = mocked_loop_start
        Client.loop_stop = mocked_loop_stop

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport,
                           self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

        self.assertEqual(mqtt_client.disconnect(), None)

    def test_timeout_disconnect_connection(self):
        """
        Method to test timeout-connection disconnect.
        :return: None
        """
        global connect_rc, disconnect_rc

        # Setting connection accepted flag
        connect_rc = 0
        # Setting connection disconnect flag
        disconnect_rc = sys.maxsize

        # Monkey patched connect, disconnect, loop_start and loop_stop methods of Paho library
        Client.connect = mocked_connect
        Client.disconnect = mocked_disconnect
        Client.loop_start = mocked_loop_start
        Client.loop_stop = mocked_loop_stop

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the Exception for broker disconnect timeout
        with self.assertRaises(Exception):
            mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                               self.client_clean_session, self.user_data, self.protocol, self.transport,
                               self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

            mqtt_client.disconnect()

    def test_invalid_disconnect_connection(self):
        """
        Method to test invalid-connection disconnect.
        :return: None
        """
        global connect_rc, disconnect_rc

        # Setting connection accepted flag
        connect_rc = 0
        # Setting connection disconnect flag
        disconnect_rc = 2

        # Monkey patched connect, disconnect, loop_start and loop_stop methods of Paho library
        Client.connect = mocked_connect
        Client.disconnect = mocked_disconnect
        Client.loop_start = mocked_loop_start
        Client.loop_stop = mocked_loop_stop

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        # Checking whether implementation raising the Exception for broker disconnect
        with self.assertRaises(Exception):
            mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                               self.client_clean_session, self.user_data, self.protocol, self.transport,
                               self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

            mqtt_client.disconnect()

    def test_publish(self):
        """
        Method to test publish method of Mqtt class.
        :return: None
        """
        global connect_rc, disconnect_rc

        # Setting connection accepted flag
        connect_rc = 0

        # Mocked the connect and loop_start method of Paho library
        Client.connect = mocked_connect
        Client.loop_start = mocked_loop_start

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport,
                           self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

        # Check publish is executes successfully and returns None
        self.assertEqual(mqtt_client.publish("test/publish", "Testing publish", 1), None)

    def test_subscribe(self):
        """
        Method to test invalid-connection disconnect.
        :return: None
        """
        global connect_rc, disconnect_rc

        # Setting connection accepted flag
        connect_rc = 0

        # Monkey patched the connect and loop_start methods of Paho library
        Client.connect = mocked_connect
        Client.loop_start = mocked_loop_start

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport,
                           self.keep_alive, self.enable_authentication, self.connection_disconnect_timeout)

        # Check publish is executing successfully and returning None
        self.assertEqual(mqtt_client.subscribe("test/publish", 1, topic_subscribe_callback), None)

    def test_QoS_class_implementation(self):
        """
        Method to test the implementation of QoSDetails class.
        :return: None
        """

        self.assertIsInstance(QoSDetails(config['inflight'], config['queue_size'], config['retry']), QoSDetails,
                              "Invalid implementation for QoSDetails class")

    def test_mqtt_messaging_attributes_implementation_for_gateway_name(self):
        """
        Method to test the implementation of MqttMessagingAttributes class for automatic topic generation.
        :return: None
        """
        self.assertIsInstance(MqttMessagingAttributes(self.edge_system.name), MqttMessagingAttributes,
                              "Changed the implementation MqttMessagingAttributes")

    def test_validation_of_sub_qos_mqtt_messaging_attributes(self):
        """
        Method to test validation of subscribe qos levels.
        :return: None
        """
        self.assertRaises(ValueError, MqttMessagingAttributes, self.edge_system.name, None, None, 1, -1)

    def test_validation_of_pub_qos_mqtt_messaging_attributes(self):
        """
        Method to test validation of publish qos levels.
        :return: None
        """
        self.assertRaises(ValueError, MqttMessagingAttributes, self.edge_system.name, None, None, -1, 1)

    def test_validation_of_retain_flag_mqtt_messaging_attributes(self):
        """
        Method to test validation of retain flag.
        :return: None
        """
        self.assertRaises(ValueError, MqttMessagingAttributes, self.edge_system.name, None, None, pub_retain="")

    def test_validation_of_sub_callback_mqtt_messaging_attributes(self):
        """
        Method to test validation of sub_callback argument.
        :return: None
        """
        self.assertRaises(ValueError, MqttMessagingAttributes, self.edge_system.name,
                          sub_callback="")

    def test_validation_of_sub_and_pub_topic_attributes(self):
        """
        Method to test validation of subscribe, publish and sub_callback attributes.
        :return: None
        """
        self.assertRaises(ValueError, MqttMessagingAttributes)

    @mock.patch.object(Mqtt, 'connect_soc')
    def test_mqtt_callback_methods(self, mock_connect):
        """
        Method to test the implementation of all callback methods of the Mqtt class
        :return: None
        """

        # Mocked connect_soc method
        mock_connect.returnvalue = None

        test_pub_message = MQTTMessage(1, "test/topic")

        # Encapsulate the authentication details
        credentials = Identity(self.root_ca_cert, self.mqtt_username, self.mqtt_password,
                               self.client_cert_file, self.client_key_file)

        # Encapsulate TLS parameters
        tls_conf = TLSConf(self.cert_required, config['tls_version'], config['cipher'])

        # Encapsulate QoS related parameters
        qos_details = QoSDetails(config['inflight'], config['queue_size'], config['retry'])

        mqtt_client = Mqtt(self.url, self.port, credentials, tls_conf, qos_details, "test-client",
                           self.client_clean_session, self.user_data, self.protocol, self.transport, self.keep_alive,
                           self.enable_authentication, self.connection_disconnect_timeout)

        on_message_called = mqtt_client.on_message("test-client", self.user_data, test_pub_message)

        on_publish_called = mqtt_client.on_publish("test-client", self.user_data, 1)

        on_subscribe_called = mqtt_client.on_subscribe("test-client", self.user_data, 1, 1)

        on_unsubscribe_called = mqtt_client.on_unsubscribe("test-client", self.user_data, 1)

        # Check on_message called successfully
        self.assertEqual(on_message_called, None, "Check implementation of on_message method")

        # Check on_publish called successfully
        self.assertEqual(on_publish_called, None, "Check implementation of on_publish method")

        # Check on_subscribe called successfully
        self.assertEqual(on_subscribe_called, None, "Check implementation of on_subscribe method")

        # Check on_unsubscribe called successfully
        self.assertEqual(on_unsubscribe_called, None, "Check implementation of on_unsubscribe method")


if __name__ == '__main__':
    unittest.main(verbosity=1)
