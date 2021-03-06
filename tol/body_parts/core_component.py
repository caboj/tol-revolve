# System imports
from __future__ import absolute_import

# SDF builder imports
from sdfbuilder.sensor import Sensor as SdfSensor
from sdfbuilder.math import Vector3
from sdfbuilder.structure import Box, Mesh

# Revolve imports
from revolve.build.sdf import BodyPart
from revolve.build.util import in_grams, in_mm

# Local imports
from .util import ColorMixin

MASS = in_grams(90.0)
WIDTH = in_mm(90)
HEIGHT = in_mm(45)


class CoreComponent(BodyPart, ColorMixin):
    """
    The core component of the robot, basically a box with an IMU sensor.
    """

    def _initialize(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        self.link = self.create_component(Box(WIDTH, WIDTH, HEIGHT, MASS), "box",
                                          visual=Mesh("model://tol_robot/meshes/CoreComponent.dae"))

        # Now we will add the IMU sensor. First, we must
        # create a sensor in SDF. Be careful to give the
        # sensor a name which is unique for the entire
        # robot, adding the ID will help us do that.
        imu = SdfSensor("imu_sensor", "imu", update_rate=self.conf.sensor_update_rate)
        self.link.add_sensor(imu)

        self.apply_color()

    def get_slot(self, slot):
        """
        There's only one slot, return the link.
        """
        self.check_slot(slot)
        return self.link

    def get_slot_position(self, slot):
        """
        Return slot position
        """
        self.check_slot(slot)
        vmax = WIDTH / 2.0
        if slot == 0:
            # Front face
            return Vector3(0, -vmax, 0)
        elif slot == 1:
            # Back face
            return Vector3(0, vmax, 0)
        elif slot == 2:
            # Right face
            return Vector3(vmax, 0, 0)

        # Left face
        return Vector3(-vmax, 0, 0)

    def get_slot_normal(self, slot):
        """
        Return slot normal.
        """
        return self.get_slot_position(slot).normalized()

    def get_slot_tangent(self, slot):
        """
        Return slot tangent
        :param slot:
        """
        self.check_slot(slot)

        # The top face is tangent to all supported
        # slots in the plane, front, back, right, left
        # Since there's no particular reason for choosing any
        # other we just return the top face for all.
        return Vector3(0, 0, 1)
