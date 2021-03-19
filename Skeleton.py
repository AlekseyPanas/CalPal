import pygame
from enum import IntEnum
import math
import Utils


class InsufficientBoneData(Exception):
    def __init__(self):
        super().__init__("The Bone data you provided was not enough to calculate the bone")


class Bone:

    class NodeTypes(IntEnum):
        START_NODE = 0
        END_NODE = 1

    def __init__(self, meat_image, meat_start_pt, bone_z_order, start_node_pos=None, end_node_pos=None, node_angle=None, length=None):
        """

        :param meat_image: Pygame surface of image
        :param meat_start_pt: Offset from top left corner of image where starting node links
        :param bone_z_order: In a skeleton, what order to draw this bone in
        :param start_node_pos: Offset from center where bone starts
        :param end_node_pos: Offset from center where bone ends
        :param node_angle: Angle between node points
        :param length: Constant length of bone
        """
        # The exact offset positions of the 2 nodes
        self.sNodePos = ()
        self.eNodePos = ()

        # Bone length always constant
        self.length = 0

        # Angle between the nodes
        self.node_angle = 0

        # Rendering shit
        self.image = meat_image
        self.img_start_node_offset = meat_start_pt
        self.z_order = bone_z_order

        # The 3 ways of creating a node: single node + angle, both nodes
        if start_node_pos is not None and node_angle is not None and length is not None:
            # Sets values
            self.length = length
            self.node_angle = math.radians(node_angle)
            self.sNodePos = start_node_pos

            # Determines eNodePos
            self.eNodePos = (start_node_pos[0] + length * math.cos(node_angle),
                             start_node_pos[1] + length * math.sin(node_angle))

        elif end_node_pos is not None and node_angle is not None and length is not None:
            raise InsufficientBoneData
        elif end_node_pos is not None and start_node_pos is not None:
            # Sets node positions
            self.sNodePos = start_node_pos
            self.eNodePos = end_node_pos

            # Calculates angle between nodes
            self.node_angle = math.atan2(-(self.eNodePos[1] - self.sNodePos[1]),
                                         self.eNodePos[0] - self.sNodePos[0])

            # Finds length
            self.length = Utils.distance(self.sNodePos, self.eNodePos)

        else:
            raise InsufficientBoneData

        self.sNodePos = list(self.sNodePos)
        self.eNodePos = list(self.eNodePos)

        # All bone connections
        self.sNodeConnects = []  # {"bone": <Bone>, "node": <START_NODE or END_NODE>}
        self.eNodeConnects = []
        self.add_connection()

    # self bone keeps their node positions while bone2 inherits!!!
    def add_connection(self, node, bone_other, node_other):  # node/node_other are NodeTypes
        """

        :param node: Which end of this bone to connect to
        :param bone_other: Other bone to connect
        :param node_other: Other bone's connecting end
        """
        if node == Bone.NodeTypes.START_NODE:
            self.sNodeConnects.append({"bone": bone_other, "node": node_other})
            new_pos = self.sNodePos
        else:
            self.eNodeConnects.append({"bone": bone_other, "node": node_other})
            new_pos = self.eNodePos

        if node_other == Bone.NodeTypes.START_NODE:
            bone_other.sNodeConnects.append({"bone": self, "node": node})
        else:
            bone_other.eNodeConnects.append({"bone": self, "node": node})

        bone_other.set_node(*new_pos, node_other)

    def move_node(self, deltaX, deltaY):
        self.sNodePos[0] += deltaX
        self.sNodePos[1] += deltaY

        self.eNodePos[0] += deltaX
        self.eNodePos[1] += deltaY

    # Moves the bone's specified node to (x, y), adjusting the whole bone in the process
    def set_node(self, x, y, node_type):
        if node_type == Bone.NodeTypes.START_NODE:
            deltaX = x - self.sNodePos[0]
            deltaY = y - self.sNodePos[1]
        else:
            deltaX = x - self.eNodePos[0]
            deltaY = y - self.eNodePos[1]
        self.move_node(deltaX, deltaY)

    # Returns the actual coordinate given a center and an offset
    @staticmethod
    def get_pos(center, offset):
        return (center[0] + offset[0],
                center[1] + offset[1])

    # Renders the bone
    def render(self, surface, time_delta, center):
        pygame.draw.line(surface, (0, 0, 255),
                         self.get_pos(center, self.sNodePos),
                         self.get_pos(center, self.eNodePos))
        pygame.draw.circle(surface, (255, 0, 0), self.get_pos(center, self.sNodePos), 4, 2)
        pygame.draw.circle(surface, (0, 255, 0), self.get_pos(center, self.eNodePos), 4, 2)


class Skeleton:
    def __init__(self, bones):
        self.bones = bones

    def render(self, screen, time_delta, center):
        for bone in self.bones:
            bone.render(screen, time_delta, center)

