*********
Rotations
*********

.. currentmodule:: astrodynamics.rotation

.. autoclass:: astrodynamics.rotation.Rotation
   :members: __init__, from_axis_angle, from_matrix, from_euler_angles, angle,
             get_axis, get_angles, matrix, apply_to, compose
   :show-inheritance:

.. autoclass:: astrodynamics.rotation.RotationOrder
   :members:
   :show-inheritance:

Rotation Convention
===================

Vector Operator
---------------

Pass ``convention='vector'`` to use the semantics of a vector operator.
According to this convention, the rotation moves vectors with respect to a fixed
reference frame.

This means that if we define rotation r is a 90 degrees rotation around the Z
axis, the image of vector I would be J, the image of vector J would be -I, the
image of vector K would be K, and the image of vector with coordinates (1, 2, 3)
would be vector (-2, 1, 3). This means that the vector rotates counterclockwise.

The difference with the frame transform convention is only the semantics of the
sign of the angle. It is always possible to create or use a rotation using
either convention to really represent a rotation that would have been best
created or used with the other convention, by changing accordingly the sign of
the rotation angle.

Frame Transform
---------------

Pass ``convention='frame'`` to use the semantics of a frame conversion.

According to this convention, the rotation considered vectors to be fixed, but
their coordinates change as they are converted from an initial frame to a
destination frame rotated with respect to the initial frame.

This means that if we define rotation r is a 90 degrees rotation around the Z
axis, the image of vector I would be -J, the image of vector J would be I, the
image of vector K would be K, and the image of vector with coordinates (1, 2, 3)
would be vector (2, -1, 3). This means that the coordinates of the vector
rotates clockwise, because they are expressed with respect to a destination
frame that is rotated counterclockwise.

The difference with vector operator convention is only the semantics of the sign
of the angle. It is always possible to create or use a rotation using either
convention to really represent a rotation that would have been best created or
used with the other convention, by changing accordingly the sign of the rotation
angle.

