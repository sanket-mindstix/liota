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

import Queue
import unittest
from threading import Thread

import mock
from aenum import UniqueEnum
from bluepy.sensortag import *

from liota.entities.devices.sensor_tag import Sensors, SensorTagDevice, SensorTagCollector


class SensorTest(unittest.TestCase):
    """
    Unit test cases for Sensors class
    """

    def setUp(self):
        """
        Method to initialise the Sensors parameters.
        :return: None
        """
        pass

    def tearDown(self):
        """
        Method to clean up the resources created during the test.
        :return: None
        """
        pass

    def test_sensors_class(self):
        """
        Test case to test the parent of Sensors class.
        :return: None
        """

        self.assertTrue(issubclass(Sensors, UniqueEnum))

    def test_sensors_class_implementation(self):
        """
        Method to test the implementation of Sensors class.
        :return: None
        """
        # Check class contains the TEMPERATURE attribute
        self.assertTrue(hasattr(Sensors, "TEMPERATURE"), "Check implementation of Sensors class")
        # Check class contains the HUMIDITY attribute
        self.assertTrue(hasattr(Sensors, "HUMIDITY"), "Check implementation of Sensors class")
        # Check class contains the BAROMETER attribute
        self.assertTrue(hasattr(Sensors, "BAROMETER"), "Check implementation of Sensors class")
        # Check class contains the BAROMETER attribute
        self.assertTrue(hasattr(Sensors, "ACCELEROMETER"), "Check implementation of Sensors class")
        # Check class contains the MAGNETOMETER attribute
        self.assertTrue(hasattr(Sensors, "MAGNETOMETER"), "Check implementation of Sensors class")
        # Check class contains the GYROSCOPE attribute
        self.assertTrue(hasattr(Sensors, "GYROSCOPE"), "Check implementation of Sensors class")
        # Check class contains the LIGHTMETER attribute
        self.assertTrue(hasattr(Sensors, "LIGHTMETER"), "Check implementation of Sensors class")
        # Check class contains the BATTERY_LEVEL attribute
        self.assertTrue(hasattr(Sensors, "BATTERY_LEVEL"), "Check implementation of Sensors class")
        # Check class contains the ALL attribute
        self.assertTrue(hasattr(Sensors, "ALL"), "Check implementation of Sensors class")


class SensorTagDeviceTest(unittest.TestCase):
    """
    Unit test cases for SensorTagDevice class
    """

    def setUp(self):
        """
        Method to initialise the SensorTagDevice parameters
        :return: None
        """
        self.device_name = "Test-Device"
        self.device_mac = "00:00:00:00:00:00"
        self.entity_type = "Device"

    def tearDown(self):
        """
        Method to clean up the resources created during the test.
        :return: None
        """
        self.device_name = None
        self.device_mac = None
        self.entity_type = None

    def test_sensor_tag_class_implementation(self):
        """
        Test case to test the implementation of SensorTagDevice class.
        :return: None
        """
        # Mock the SensorTag class
        with mock.patch("liota.entities.devices.sensor_tag.SensorTag.__init__") as mock_lm:
            sensor_tag_device = SensorTagDevice(self.device_name, self.device_mac, self.entity_type)

            self.assertIsInstance(sensor_tag_device, SensorTagDevice, "Check implementation of SensorTagDevice class")

            # Check constructor has been called with this arguments
            mock_lm.assert_called_with(sensor_tag_device, addr=self.device_mac)


class SensorTagCollectorTest(unittest.TestCase):
    """Unit test cases for SensorTagCollector class"""

    def setUp(self):
        """
        Method to initialise the parameters required for SensorTagCollector class and creating the object of it.
        :return: None
        """
        self.device_name = "Test-Device"
        self.device_mac = "00:00:00:00:00:00"
        self.test_sensors = [Sensors.ALL]

        with mock.patch.object(SensorTagCollector, "_re_connect") as mock_reconnect, \
                mock.patch.object(Thread, "start") as mock_start:
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=self.test_sensors, sampling_interval_sec=1,
                                                            retry_interval_sec=1)

    def tearDown(self):
        """
        Method to clean up the resources created during the test.
        :return: None
        """
        self.device_name = None
        self.device_mac = None
        self.test_sensors = None
        self.temp_sensor_collector = None

    def test_init_no_sensors(self):
        """
        Test case to test the validation of SensorTagCollector class for empty Sensor list.
        :return: None
        """
        self.assertRaises(TypeError, lambda: SensorTagCollector(self.device_name, self.device_mac))

    @mock.patch.object(SensorTagCollector, '_re_connect')
    @mock.patch.object(Thread, 'start')
    def test_init_with_sensors(self, mock_start, mocked_re_connect):
        """
        Test case to test the implementation of constructor of SensorTagCollector class.
        :param mock_start: Thread start mocked argument
        :param mocked_re_connect: Mocked _re_connect method of SensorTagCollector class.
        :return:
        """
        test_sensors = [Sensors.ALL]

        # Creating the SensorTagCollector object
        SensorTagCollector(self.device_name, self.device_mac, sensors=test_sensors)

        # Checking the mocked method has been called
        mocked_re_connect.assert_called()

    def test_get_temperature(self):
        """
        Test case to test the implementation of get_temperature method.
        :return: None
        """
        # Enabling the temperature sensor configurations
        self.temp_sensor_collector._temp_enabled = True
        self.temp_sensor_collector._temp_queue = Queue.Queue()

        # Inserting the sample temperature sensor data into the temperature queue
        test_temp_data = (10, 20)
        self.temp_sensor_collector._temp_queue.put(test_temp_data)

        # Check getting same value using get_temperature method
        self.assertEqual(test_temp_data, self.temp_sensor_collector.get_temperature(),
                         "Invalid implementation of get_temperature")

    def test_get_humidity(self):
        """
        Test case to test the implementation of get_humidity method.
        :return: None
        """
        # Enabling the humidity sensor configurations
        self.temp_sensor_collector._humi_enabled = True
        self.temp_sensor_collector._humi_queue = Queue.Queue()

        # Inserting the sample humidity sensor data into the humidity queue
        test_humi_data = (10, 20)
        self.temp_sensor_collector._humi_queue.put(test_humi_data)

        # Check getting same value using get_humidity method
        self.assertEqual(test_humi_data, self.temp_sensor_collector.get_humidity(),
                         "Invalid implementation of get_humidity")

    def test_get_accelerometer(self):
        """
        Test case to test the implementation of get_accelerometer method.
        :return: None
        """

        # Enabling the accelerometer sensor
        self.temp_sensor_collector._acce_enabled_enabled = True
        self.temp_sensor_collector._acce_queue = Queue.Queue()

        # Inserting the sample accelerometer sensor data into the accelerometer queue
        test_acc_data = (10, 20, 30)
        self.temp_sensor_collector._acce_queue.put(test_acc_data)

        # Check getting same value using get_accelerometer method
        self.assertEqual(test_acc_data, self.temp_sensor_collector.get_accelerometer(),
                         "Invalid implementation of get_accelerometer")

    def test_get_magnetometer(self):
        """
        Test case to test the implementation of get_magnetometer method.
        :return: None
        """

        # Enabling the magnetometer sensor
        self.temp_sensor_collector._magn_enabled = True
        self.temp_sensor_collector._magn_queue = Queue.Queue()

        # Inserting the sample accelerometer sensor data into the accelerometer queue
        test_mgn_data = (10, 20, 30)
        self.temp_sensor_collector._magn_queue.put(test_mgn_data)

        # Check getting same value using get_magnetometer method
        self.assertEqual(test_mgn_data, self.temp_sensor_collector.get_magnetometer(),
                         "Invalid implementation of get_magnetometer")

    def test_get_gyroscope(self):
        """
        Test case to test the implementation of get_gyroscope method.
        :return: None
        """

        # Enabling the gyroscope sensor
        self.temp_sensor_collector._gyro_enabled = True
        self.temp_sensor_collector._gyro_queue = Queue.Queue()

        # Inserting the sample gyroscope sensor data into the gyroscope queue
        test_gyro_data = (10, 20, 30)
        self.temp_sensor_collector._gyro_queue.put(test_gyro_data)

        # Check getting same value using get_gyroscope method
        self.assertEqual(test_gyro_data, self.temp_sensor_collector.get_gyroscope(),
                         "Invalid implementation of get_gyroscope")

    def test_get_barometer(self):
        """
        Test case to test the implementation of get_barometer method.
        :return: None
        """

        # Enabling the barometer sensor
        self.temp_sensor_collector._baro_enabled = True
        self.temp_sensor_collector._baro_queue = Queue.Queue()

        # Inserting the sample barometer sensor data into the barometer queue
        test_baro_data = (10, 20, 30)
        self.temp_sensor_collector._baro_queue.put(test_baro_data)

        # Check getting same value using get_barometer method
        self.assertEqual(test_baro_data, self.temp_sensor_collector.get_barometer(),
                         "Invalid implementation of get_gyroscope")

    def test_get_battery_level(self):
        """
        Test case to test the implementation of get_battery_level method.
        :return: None
        """

        # Enabling the battery level sensor
        self.temp_sensor_collector._bat_level_enabled = True
        self.temp_sensor_collector._bat_level_queue = Queue.Queue()

        # Inserting the sample battery level sensor data into the battery level queue
        test_battery_data = 10
        self.temp_sensor_collector._bat_level_queue.put(test_battery_data)

        # Check getting same value using get_battery_level method
        self.assertEqual(test_battery_data, self.temp_sensor_collector.get_battery_level(),
                         "Invalid implementation of get_battery_level")

    def test_get_light_level(self):
        """
        Test case to test the implementation of get_light_level method.
        :return: None
        """

        # Enabling the light sensor
        self.temp_sensor_collector._light_enabled = True
        self.temp_sensor_collector._light_queue = Queue.Queue()

        # Inserting the sample light sensor data into the light queue
        test_battery_data = 10
        self.temp_sensor_collector._light_queue.put(test_battery_data)

        # Check getting same value using get_light_level method
        self.assertEqual(test_battery_data, self.temp_sensor_collector.get_light_level(),
                         "Invalid implementation of get_light_level")

    @mock.patch.object(SensorTagCollector, '_connect')
    @mock.patch.object(Thread, 'start')
    def test_re_connect_implementation(self, mocked_start, mocked_connect):
        """
        Test case to test the implementation of _re_connect method.
        :return: None
        """

        # Creating the SensorTagCollector object
        self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                        sensors=self.test_sensors, sampling_interval_sec=0.1,
                                                        retry_interval_sec=0.1)

        # Check connect method call has been made from _re_connect
        mocked_connect.assert_called()

    @mock.patch.object(SensorTagCollector, '_enable')
    @mock.patch.object(Thread, 'start')
    def test_connect_implementation(self, mocked_start, mocked_enable):
        """
        Test case to test the implementation of get_light_level method.
        :return: None
        """
        # Creating the SensorTagCollector object
        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=self.test_sensors, sampling_interval_sec=0.1,
                                                            retry_interval_sec=0.1)

            # Check _enable method call has been made from _connect
            mocked_enable.assert_called()

    @mock.patch.object(Thread, 'start')
    def test_enable_validation(self, mocked_start):
        """
        Test case to test the validation of _enable method.
        :return: None
        """
        # Mocking the SensorTag class object
        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            with self.assertRaises(TypeError):
                # Check implementation raising the TypeError for invalid sensor type
                self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                                sensors=["Invalid_Sensor"], sampling_interval_sec=0.1,
                                                                retry_interval_sec=0.1)

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_temperature")
    def test_enable_implementation_temperature_sensor(self, mocked_enable_temperature, mocked_start):
        """
        Test case to test the implementation of _enable method with temperature sensor.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.TEMPERATURE], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            mocked_enable_temperature.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_humidity")
    def test_enable_implementation_humidity_sensor(self, mocked_enable_humidity, mocked_start):
        """
        Test case to test the implementation of _enable method with humidity sensor.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.HUMIDITY], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            mocked_enable_humidity.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_barometer")
    def test_enable_implementation_barometer_sensor(self, enable_barometer, mocked_start):
        """
        Test case to test the implementation of _enable method with barometer sensor.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.BAROMETER], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            enable_barometer.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_accelerometer")
    def test_enable_implementation_accelerometer_sensor(self, enable_accelerometer, mocked_start):
        """
        Test case to test the implementation of _enable method with accelerometer sensor.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.ACCELEROMETER], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            enable_accelerometer.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_magnetometer")
    def test_enable_implementation_magnetometer_sensor(self, enable_magnetometer, mocked_start):
        """
        Test case to test the implementation of _enable method with magnetometer sensor.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.MAGNETOMETER], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            enable_magnetometer.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_gyroscope")
    def test_enable_implementation_gyroscope_sensor(self, enable_gyroscope, mocked_start):
        """
        Test case to test the implementation of _enable method with gyroscope sensor.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.GYROSCOPE], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            enable_gyroscope.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_battery_level")
    def test_enable_implementation_battery_level_sensor(self, enable_battery_level, mocked_start):
        """
        Test case to test the implementation of _enable method with battery_level sensor.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.BATTERY_LEVEL], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            enable_battery_level.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_lightmeter")
    def test_enable_implementation_light_meter_sensor(self, enable_lightmeter, mocked_start):
        """
        Test case to test the implementation of _enable method with lightmeter sensor.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.LIGHTMETER], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            enable_lightmeter.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable_temperature")
    @mock.patch.object(SensorTagCollector, "_enable_humidity")
    @mock.patch.object(SensorTagCollector, "_enable_barometer")
    @mock.patch.object(SensorTagCollector, "_enable_accelerometer")
    @mock.patch.object(SensorTagCollector, "_enable_magnetometer")
    @mock.patch.object(SensorTagCollector, "_enable_gyroscope")
    @mock.patch.object(SensorTagCollector, "_enable_battery_level")
    @mock.patch.object(SensorTagCollector, "_enable_lightmeter")
    def test_enable_implementation_all_sensor(self, _enable_lightmeter, _enable_battery_level, _enable_gyroscope
                                              , _enable_magnetometer, _enable_accelerometer, _enable_barometer,
                                              _enable_humidity, _enable_temperature, mocked_start):
        """
        Test case to test the implementation of _enable method with all available sensors.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector object
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.ALL], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked methods call has been made from _enable
            _enable_lightmeter.assert_called()
            _enable_battery_level.assert_called()
            _enable_gyroscope.assert_called()
            _enable_magnetometer.assert_called()
            _enable_accelerometer.assert_called()
            _enable_barometer.assert_called()
            _enable_humidity.assert_called()
            _enable_temperature.assert_called()
            mocked_start.assert_called()

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable")
    def test_implementation_get_sensor_tag(self, enable, mocked_start):
        """
        Test case to test the implementation of get_sensor_tag method.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm:
            # Creating the SensorTagCollector
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.LIGHTMETER], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Check mocked method call has been made from _enable
            enable.assert_called()

            # Check method returning SensorTagDevice object
            self.assertIsInstance(self.temp_sensor_collector.get_sensor_tag(), SensorTagDevice)

    @mock.patch.object(Thread, 'start')
    @mock.patch.object(SensorTagCollector, "_enable")
    def test_enable_implementation_get_sensor_tag(self, enable, mocked_start):
        """
        Test case to test the implementation of stop method.
        :return: None
        """

        with mock.patch("liota.entities.devices.sensor_tag.SensorTag") as mock_lm, \
                mock.patch.object(SensorTag, "disconnect") as disconnect:
            # Creating the SensorTagCollector
            self.temp_sensor_collector = SensorTagCollector(self.device_name, self.device_mac,
                                                            sensors=[Sensors.LIGHTMETER], sampling_interval_sec=0.1
                                                            , retry_interval_sec=0.1)
            # Call the stop method of SensorTagCollector class
            self.temp_sensor_collector.stop()

            # Check implementation calling underline disconnect method of SensorTag class
            disconnect.assert_called()


if __name__ == '__main__':
    unittest.main(verbosity=1)
