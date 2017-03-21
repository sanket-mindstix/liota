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
import json
import pint

from liota.lib.utilities.si_unit import parse_unit
from liota.dccs.aws_iot import AWSIoT
from liota.dcc_comms.mqtt_dcc_comms import MqttDccComms
from liota.entities.metrics.metric import Metric
from liota.entities.devices.simulated_device import SimulatedDevice
from liota.entities.edge_systems.dell5k_edge_system import Dell5KEdgeSystem
from liota.entities.registered_entity import RegisteredEntity
from liota.entities.metrics.registered_metric import RegisteredMetric
from liota.lib.utilities.utility import getUTCmillis
from liota.lib.utilities.utility import ordered_list

# Create a pint unit registry
ureg = pint.UnitRegistry()


# Monkey patched init method of
def mocked_init_mqtt_dcc_comms(self, *args, **kwargs):
    pass


# Sampling function
def sampling_function():
    pass


class MQTTTest(unittest.TestCase):
    """
    AWSIoT unit test cases
    """

    def setUp(self):
        """
        Method to initialise the AWSIoT parameters.
        :return: None
        """

        # EdgeSystem name
        self.edge_system = Dell5KEdgeSystem("TestEdgeSystem")

        # Monkey patch the constructor of MqttDccComms
        MqttDccComms.__init__ = mocked_init_mqtt_dcc_comms

        self.mocked_mqtt_dcc_comms = MqttDccComms()

        self.aws = AWSIoT(self.mocked_mqtt_dcc_comms, enclose_metadata=True)

    def tearDown(self):
        """
        Method to cleanup the resource created during the execution of test case.
        :return: None
        """
        self.edge_system = None
        self.mocked_mqtt_dcc_comms = None
        self.aws = None

    def test_aws_class_implementation(self):
        """
        Method to test the implementation of AWSIoT class.
        :return: None
        """

        self.assertIsInstance(self.aws, AWSIoT, "Check the implementation of AWSIoT class")

    def test_validation_of_comms_parameter(self):
        """
        Method to test the validation of AWSIoT class for invalid connections object.
        :return: None
        """
        # Checking whether implementation raising the TypeError Exception for invalid comms object
        with self.assertRaises(TypeError):
            AWSIoT("Invalid object", enclose_metadata=True)

    def test_implementation_register_entity(self):
        """
        Method to test the implementation of register method of AWSIoT for entity type.
        :return: None
        """

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        # Check the returned object is of the class RegisteredEntity
        self.assertIsInstance(registered_entity, RegisteredEntity)

    def test_implementation_register_metric(self):
        """
        Method to test the implementation of register method of AWSIoT for entity type.
        :return: None
        """

        # Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=None,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        # Check the returned object is of the class RegisteredMetric
        self.assertIsInstance(registered_metric, RegisteredMetric)

    def test_implementation_create_relationship(self):
        """
        Method to test RegisteredEntity and Parent and RegisteredMetric as child.
        :return: None
        """

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        #  Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=None,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        # Creating the parent-child relationship
        self.aws.create_relationship(registered_entity, registered_metric)

        self.assertEqual(registered_metric.parent, registered_entity, "Check the implementation of create_relationship")

    def test_validation_create_relationship_metric_device(self):
        """
        Method to test RegisteredMetric as Parent and RegisteredEntity as child.
        :return: None
        """

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        #  Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=None,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        with self.assertRaises(TypeError):
            # Test case to check RegisteredEntity as both Parent and Child
            self.aws.create_relationship(registered_metric, registered_entity)

    def test_validation_create_relationship_child_entity(self):
        """
        Method to test the validation of create_relationship method of class AWSIoT.
        :return: None
        """

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        with self.assertRaises(TypeError):
            # Creating the parent-child relationship between Edge-System and Edge-System
            self.aws.create_relationship(registered_entity, registered_entity)

    def test_implementation_get_entity_hierarchy(self):
        """
        Method to check get_entity_entity_hierarchy() for RegisteredEdgeSystem->RegisteredMetric
        :return: None
        """

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        #  Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=None,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        # Creating the parent-child relationship
        self.aws.create_relationship(registered_entity, registered_metric)

        # Getting the parent child relationship array from registered metric
        entity_hierarchy = self.aws._get_entity_hierarchy(registered_metric)

        self.assertSequenceEqual([registered_entity.ref_entity.name, registered_metric.ref_entity.name],
                                 entity_hierarchy, "Check the implementation of _get_entity_hierarchy for "
                                                   "RegisteredEdgeSystem->RegisteredMetric")

    def test_implementation_get_entity_hierarchy_device_metric(self):
        """
        Method to check get_entity_entity_hierarchy() for RegisteredEdgeSystem->RegisteredDevice->RegisteredMetric
        :return: None
        """

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        #  Creating Simulated Device
        test_sensor = SimulatedDevice("TestSensor")

        #  Registering Device and creating Parent-Child relationship
        reg_test_sensor = self.aws.register(test_sensor)

        self.aws.create_relationship(registered_entity, reg_test_sensor)

        #  Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=ureg.degC,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        # Creating the parent-child relationship
        self.aws.create_relationship(reg_test_sensor, registered_metric)

        # Getting the parent child relationship array from registered metric
        entity_hierarchy = self.aws._get_entity_hierarchy(registered_metric)

        self.assertSequenceEqual([registered_entity.ref_entity.name, reg_test_sensor.ref_entity.name,
                                  registered_metric.ref_entity.name],
                                 entity_hierarchy, "Check the implementation of _get_entity_hierarchy for "
                                                   "RegisteredEdgeSystem->RegisteredDevice->RegisteredMetric")

    def test_validation_get_entity_hierarchy(self):
        """
        Method to test the validation of _get_entity_hierarchy method of class AWSIoT.
        :return: None
        """

        # Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=None,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        # Checking whether implementation raising the TypeError for invalid input
        with self.assertRaises(TypeError):
            self.aws._get_entity_hierarchy(test_metric)

    def test_implementation_format_data_no_data(self):
        """
        Method to test the implementation of _format_data for empty metric data.
        :return: None
        """

        self.aws = AWSIoT(self.mocked_mqtt_dcc_comms, enclose_metadata=False)

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        #  Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=None,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        # Creating the parent-child relationship
        self.aws.create_relationship(registered_entity, registered_metric)

        # Getting the parent child relationship array from registered metric
        formatted_data = self.aws._format_data(registered_metric)

        # Check two dicts are equal or not
        self.assertEqual(None, formatted_data, "Check implementation of _format_data")

    def test_implementation_format_data_with_enclose_metadata(self):
        """
        Method to test the implementation of _format_data method of class AWSIoT.
        :return: None
        """

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        #  Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=None,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        # Creating the parent-child relationship
        self.aws.create_relationship(registered_entity, registered_metric)

        timestamp = getUTCmillis()

        registered_metric.values.put((timestamp, 10))

        expected_output = {
            "edge_system_name": registered_entity.ref_entity.name,
            "metric_name": registered_metric.ref_entity.name,
            "metric_data": [{
                "value": 10,
                "timestamp": timestamp
            }],
            "unit": "null"
        }

        # Getting the parent child relationship array from registered metric
        formatted_data = self.aws._format_data(registered_metric)

        formatted_json_data = json.loads(formatted_data)

        # Check two dicts are equal or not
        self.assertEqual(ordered_list(formatted_json_data) == ordered_list(expected_output), True,
                         "Check implementation of _format_data")

    def test_implementation_format_data_without_enclose_metatadata(self):
        """
        Method to test the implementation of create_relationship method without enclosed meta_data option
        of class AWSIoT.
        :return: None
        """

        self.aws = AWSIoT(self.mocked_mqtt_dcc_comms, enclose_metadata=False)

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        #  Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=None,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        # Creating the parent-child relationship
        self.aws.create_relationship(registered_entity, registered_metric)

        # Get current timestamp
        timestamp = getUTCmillis()

        registered_metric.values.put((timestamp, 10))

        # Expected output without enclosed metadata
        expected_output = {
            "metric_name": registered_metric.ref_entity.name,
            "metric_data": [{
                "value": 10,
                "timestamp": timestamp
            }],
            "unit": "null"
        }

        # Getting the parent child relationship array from registered metric
        formatted_data = self.aws._format_data(registered_metric)

        # Convert json string to dict for the comparision
        formatted_json_data = json.loads(formatted_data)

        # Check two dicts are equal or not
        self.assertEqual(ordered_list(formatted_json_data) == ordered_list(expected_output), True,
                         "Check implementation of _format_data")

    def test_implementation_format_data_without_enclose_metadata_device(self):
        """
        Method to test the implementation of _format_data method of class AWSIoT.
        :return: None
        """

        # Register the edge
        registered_entity = self.aws.register(self.edge_system)

        #  Creating Simulated Device
        test_sensor = SimulatedDevice("TestSensor")

        #  Registering Device and creating Parent-Child relationship
        reg_test_sensor = self.aws.register(test_sensor)

        self.aws.create_relationship(registered_entity, reg_test_sensor)

        #  Creating test Metric
        test_metric = Metric(
            name="Test_Metric",
            unit=ureg.degC,
            interval=10,
            aggregation_size=2,
            sampling_function=sampling_function
        )

        registered_metric = self.aws.register(test_metric)

        # Creating the parent-child relationship
        self.aws.create_relationship(reg_test_sensor, registered_metric)

        # Get current timestamp
        timestamp = getUTCmillis()

        registered_metric.values.put((timestamp, 10))

        # Expected output without enclosed metadata
        expected_output = {
            "edge_system_name": registered_entity.ref_entity.name,
            "metric_name": registered_metric.ref_entity.name,
            "device_name": reg_test_sensor.ref_entity.name,
            "metric_data": [{
                "value": 10,
                "timestamp": timestamp
            }],
            "unit": "null"
        }

        unit_tuple = parse_unit(ureg.degC)

        if unit_tuple[0] is None:
            # Base and Derived Units
            expected_output['unit'] = unit_tuple[1]
        else:
            # Prefixed or non-SI Units
            expected_output['unit'] = unit_tuple[0] + unit_tuple[1]

        # Getting the parent child relationship array from registered metric
        formatted_data = self.aws._format_data(registered_metric)

        # Convert json string to dict for the comparision
        formatted_json_data = json.loads(formatted_data)

        # Check two dicts are equal or not
        self.assertEqual(ordered_list(formatted_json_data) == ordered_list(expected_output), True,
                         "Check implementation of _format_data")

    def test_set_properties(self):
        """
        Method to test the implementation of set_properties method of AWSIoT class.
        :return: None
        """
        # Check method raising the NotImplementedError exception.
        self.assertRaises(NotImplementedError, self.aws.set_properties, None, None)


if __name__ == '__main__':
    unittest.main(verbosity=1)
