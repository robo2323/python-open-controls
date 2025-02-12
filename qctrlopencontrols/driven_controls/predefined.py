# Copyright 2019 Q-CTRL Pty Ltd & Q-CTRL Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
==========================
driven_controls.predefined
==========================

More information and publication references to all driven controls defined here
can be found at https://docs.q-ctrl.com/control-library
"""

import numpy as np

from ..exceptions.exceptions import ArgumentsValueError
from ..driven_controls import (
    BB1, CORPSE, CORPSE_IN_BB1, CORPSE_IN_SCROFULOUS, CORPSE_IN_SK1,
    PRIMITIVE, SCROFULOUS, SK1, WAMF1)

from .driven_control import DrivenControl


def new_predefined_driven_control(
        scheme=PRIMITIVE,
        **kwargs):
    """
    Create a new driven control

    Parameters
    ----------
    scheme : string, optional
        Defaults to None. The name of the driven control type,
        supported options are:
        - 'primitive'
        - 'wimperis_1'
        - 'solovay_kitaev_1'
        - 'compensating_for_off_resonance_with_a_pulse_sequence'
        - 'compensating_for_off_resonance_with_a_pulse_sequence_with_wimperis'
        - 'compensating_for_off_resonance_with_a_pulse_sequence_with_solovay_kitaev'
        - 'walsh_amplitude_modulated_filter_1'
        - 'short_composite_rotation_for_undoing_length_over_and_under_shoot'
        - 'corpse_in_scrofulous'
    kwargs : dict, optional
        options to make the corresponding control type.

    Returns
    -------
    qctrlopencontrols.DrivenControls
        Returns a driven control corresponding to the driven_control_type.

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """

    # Raise error if the input driven_control_type is not known
    if scheme == PRIMITIVE:
        driven_control = _new_primitive_control(**kwargs)
    elif scheme == BB1:
        driven_control = _new_wimperis_1_control(**kwargs)
    elif scheme == SK1:
        driven_control = _new_solovay_kitaev_1_control(**kwargs)
    elif scheme == WAMF1:
        driven_control = _new_walsh_amplitude_modulated_filter_1_control(**kwargs)
    elif scheme == CORPSE:
        driven_control = _new_compensating_for_off_resonance_with_a_pulse_sequence_control(
            **kwargs)
    elif scheme == CORPSE_IN_BB1:
        driven_control = \
            _new_compensating_for_off_resonance_with_a_pulse_sequence_with_wimperis_control(
                **kwargs)
    elif scheme == \
        CORPSE_IN_SK1:
        driven_control = \
            _new_compensating_for_off_resonance_with_a_pulse_sequence_with_solovay_kitaev_control(
                **kwargs)
    elif scheme == SCROFULOUS:
        driven_control = \
            _new_short_composite_rotation_for_undoing_length_over_and_under_shoot_control(**kwargs)
    elif scheme == CORPSE_IN_SCROFULOUS:
        driven_control = _new_corpse_in_scrofulous_control(**kwargs)
    else:
        raise ArgumentsValueError(
            'Unknown predefined pulse type. See help(new_predefined_driven_control) to display all'
            + ' allowed inputs.',
            {'scheme': scheme})
    return driven_control


def _predefined_common_attributes(maximum_rabi_rate,
                                  rabi_rotation,
                                  azimuthal_angle):
    """
    Adds some checks etc for all the predefined pulses

    Parameters
    ----------
    rabi_rotation : float
        The total polar angle to be performed by the pulse.
        Defined in polar coordinates.
    maximum_rabi_rate : float
        Defaults to 2.*np.pi
        The maximum rabi frequency for the pulse.
    azimuthal_angle : float
        The azimuthal position of the pulse.

    Returns
    -------
    tuple
        Tuple of floats made of:
            (rabi_rate, rabi_rotation, azimuthal)

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """

    maximum_rabi_rate = float(maximum_rabi_rate)
    if maximum_rabi_rate <= 0:
        raise ArgumentsValueError(
            'Maximum rabi angular frequency should be greater than zero.',
            {'maximum_rabi_rate': maximum_rabi_rate})

    rabi_rotation = float(rabi_rotation)
    if rabi_rotation == 0:
        raise ArgumentsValueError(
            'The rabi rotation must be non zero.',
            {'rabi_rotation': rabi_rotation}
        )

    azimuthal_angle = float(azimuthal_angle)

    return (maximum_rabi_rate, rabi_rotation, azimuthal_angle)

def _get_transformed_rabi_rotation_wimperis(rabi_rotation):
    """
    Calculates the Rabi rotation angle as required by Wimperis 1 (BB1)
    and Solovay-Kitaev driven controls.

    Parameters
    ----------
    rabi_rotation : float
        Rotation angle of the operation

    Returns
    -------
    float
        The transformed angle as per definition for the Wimperis 1 (BB1) control

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    # Raise error if the polar angle is incorrect
    if rabi_rotation > 4 * np.pi:
        raise ArgumentsValueError(
            'The polar angle must be between -4 pi and 4 pi (inclusive).',
            {'rabi_rotation': rabi_rotation})
    return np.arccos(-rabi_rotation / (4 * np.pi))

def _derive_segments(angles, amplitude=2. * np.pi):
    """
    Derive the driven control segments from a set of rabi_rotations defined in terms of the
        spherical polar angles

    Parameters
    ----------
    angles : numpy.array
        angles is made of a list polar angle 2-lists formatted
        as [polar_angle, azimuthal_angle].
        All angles should be greater or equal to 0, and the polar_angles
        must be greater than zero.
    amplitude : float, optional
        Defaults to 1. The total amplitude of each segment in
        rad Hz.

    Returns
    -------
    list
        Segments for the driven control.

    """
    segments = [[amplitude * np.cos(phi), amplitude * np.sin(phi), 0., theta / amplitude]
                for (theta, phi) in angles]
    return segments


def _new_primitive_control(
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    Primitive driven control.

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the driven control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the driven control.
    azimuthal_angle : float, optional
        The azimuthal position of the driven control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControl
        The driven control.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    return DrivenControl(
        rabi_rates=[maximum_rabi_rate],
        azimuthal_angles=[azimuthal_angle],
        detunings=[0],
        durations=[rabi_rotation/maximum_rabi_rate],
        **kwargs)


def _new_wimperis_1_control(
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    Wimperis or BB1 control.

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the control.
    azimuthal_angle : float, optional
        The azimuthal position of the control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControl
        The driven control.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    phi_p = _get_transformed_rabi_rotation_wimperis(rabi_rotation)

    rabi_rotations = [rabi_rotation, np.pi, 2 * np.pi, np.pi]

    rabi_rates = [maximum_rabi_rate] * 4
    azimuthal_angles = [azimuthal_angle, azimuthal_angle + phi_p,
                        azimuthal_angle + 3 * phi_p, azimuthal_angle + phi_p]
    detunings = [0] * 4
    durations = [rabi_rotation_ / maximum_rabi_rate for rabi_rotation_ in rabi_rotations]

    return DrivenControl(
        rabi_rates=rabi_rates,
        azimuthal_angles=azimuthal_angles,
        detunings=detunings,
        durations=durations,
        **kwargs)

def _new_solovay_kitaev_1_control(
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    First-order Solovay-Kitaev control, also known as SK1

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the control.
    azimuthal_angle : float, optional
        The azimuthal position of the control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControl
        The driven control.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    phi_p = _get_transformed_rabi_rotation_wimperis(rabi_rotation)

    rabi_rotations = [rabi_rotation, 2 * np.pi, 2 * np.pi]

    rabi_rates = [maximum_rabi_rate] * 3
    azimuthal_angles = [azimuthal_angle, azimuthal_angle - phi_p, azimuthal_angle + phi_p]
    detunings = [0] * 3
    durations = [rabi_rotation_ / maximum_rabi_rate for rabi_rotation_ in rabi_rotations]

    return DrivenControl(
        rabi_rates=rabi_rates,
        azimuthal_angles=azimuthal_angles,
        detunings=detunings,
        durations=durations,
        **kwargs)


def _new_short_composite_rotation_for_undoing_length_over_and_under_shoot_control(  # pylint: disable=invalid-name
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    SCROFULOUS control to compensate for pulse length errors

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the control.
    azimuthal_angle : float, optional
        The azimuthal position of the control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControl
        The driven control.

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    # Create a lookup table for rabi rotation and phase angles, taken from the official paper.
    # Note: values in the paper are in degrees.
    def degrees_to_radians(angle_in_degrees):
        return angle_in_degrees / 180 * np.pi

    if np.isclose(rabi_rotation, np.pi):
        theta_1 = degrees_to_radians(180.)
        phi_1 = np.arccos(
            -np.pi * np.cos(theta_1) / 2 / theta_1 / np.sin(rabi_rotation / 2)
        )
        phi_2 = phi_1 - np.arccos(- np.pi / 2 / theta_1)
    elif np.isclose(rabi_rotation, 0.5 * np.pi):
        theta_1 = degrees_to_radians(115.2)
        phi_1 = np.arccos(
            -np.pi * np.cos(theta_1) / 2 / theta_1 / np.sin(rabi_rotation / 2)
        )
        phi_2 = phi_1 - np.arccos(- np.pi / 2 / theta_1)
    elif np.isclose(rabi_rotation, 0.25 * np.pi):
        theta_1 = degrees_to_radians(96.7)
        phi_1 = np.arccos(
            -np.pi * np.cos(theta_1) / 2 / theta_1 / np.sin(rabi_rotation / 2)
        )
        phi_2 = phi_1 - np.arccos(- np.pi / 2 / theta_1)
    else:
        raise ArgumentsValueError(
            'rabi_rotation angle must be either pi, pi/2 or pi/4',
            {'rabi_rotation': rabi_rotation})

    theta_3 = theta_1
    phi_3 = phi_1
    theta_2 = np.pi

    rabi_rotations = [theta_1, theta_2, theta_3]

    rabi_rates = [maximum_rabi_rate] * 3
    azimuthal_angles = [azimuthal_angle + phi_1, azimuthal_angle + phi_2, azimuthal_angle + phi_3]
    detunings = [0] * 3
    durations = [rabi_rotation_ / maximum_rabi_rate for rabi_rotation_ in rabi_rotations]

    return DrivenControl(
        rabi_rates=rabi_rates,
        azimuthal_angles=azimuthal_angles,
        detunings=detunings,
        durations=durations,
        **kwargs)


def _new_compensating_for_off_resonance_with_a_pulse_sequence_control(  # pylint: disable=invalid-name
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    Compensating for off resonance with a pulse sequence, often abbreviated as CORPSE.

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the control.
    azimuthal_angle : float, optional
        The azimuthal position of the control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControl
        The driven control.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    k = np.arcsin(np.sin(rabi_rotation / 2.) / 2.)

    rabi_rotations = [rabi_rotation / 2. + 2 * np.pi - k, 2 * np.pi - 2 * k, rabi_rotation / 2. - k]

    rabi_rates = [maximum_rabi_rate] * 3
    azimuthal_angles = [azimuthal_angle, azimuthal_angle + np.pi, azimuthal_angle]
    detunings = [0] * 3
    durations = [rabi_rotation_ / maximum_rabi_rate for rabi_rotation_ in rabi_rotations]

    return DrivenControl(
        rabi_rates=rabi_rates,
        azimuthal_angles=azimuthal_angles,
        detunings=detunings,
        durations=durations,
        **kwargs)


def _new_compensating_for_off_resonance_with_a_pulse_sequence_with_wimperis_control(  # pylint: disable=invalid-name
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    Compensating for off resonance with a pulse sequence with an embedded
    Wimperis (or BB1) control, also known as CinBB.

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the control.
    azimuthal_angle : float, optional
        The azimuthal position of the control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControl
        The driven control.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    phi_p = _get_transformed_rabi_rotation_wimperis(rabi_rotation)
    k = np.arcsin(np.sin(rabi_rotation / 2.) / 2.)

    rabi_rotations = [2 * np.pi + rabi_rotation / 2. - k, 2 * np.pi - 2 * k,
                      rabi_rotation / 2. - k, np.pi, 2 * np.pi, np.pi]

    rabi_rates = [maximum_rabi_rate] * 6
    azimuthal_angles = [azimuthal_angle, azimuthal_angle + np.pi, azimuthal_angle,
                        azimuthal_angle + phi_p, azimuthal_angle + 3 * phi_p,
                        azimuthal_angle + phi_p]
    detunings = [0] * 6
    durations = [rabi_rotation_ / maximum_rabi_rate for rabi_rotation_ in rabi_rotations]

    return DrivenControl(
        rabi_rates=rabi_rates,
        azimuthal_angles=azimuthal_angles,
        detunings=detunings,
        durations=durations,
        **kwargs)


def _new_compensating_for_off_resonance_with_a_pulse_sequence_with_solovay_kitaev_control(  # pylint: disable=invalid-name
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    Compensating for off resonance with a pulse sequence with an
     embedded Solovay Kitaev (or SK1) control, also knowns as CinSK.

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the control.
    azimuthal_angle : float, optional
        The azimuthal position of the control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControl
        The driven control.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    phi_p = _get_transformed_rabi_rotation_wimperis(rabi_rotation)
    k = np.arcsin(np.sin(rabi_rotation / 2.) / 2.)

    rabi_rotations = [2 * np.pi + rabi_rotation / 2. - k, 2 * np.pi - 2 * k,
                      rabi_rotation / 2. - k, 2 * np.pi, 2 * np.pi]

    rabi_rates = [maximum_rabi_rate] * 5
    azimuthal_angles = [azimuthal_angle, azimuthal_angle + np.pi, azimuthal_angle,
                        azimuthal_angle - phi_p, azimuthal_angle + phi_p]
    detunings = [0] * 5
    durations = [rabi_rotation_ / maximum_rabi_rate for rabi_rotation_ in rabi_rotations]

    return DrivenControl(
        rabi_rates=rabi_rates,
        azimuthal_angles=azimuthal_angles,
        detunings=detunings,
        durations=durations,
        **kwargs)


def _new_corpse_in_scrofulous_control( # pylint: disable=invalid-name
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    CORPSE (Compensating for Off Resonance with a Pulse SEquence) embedded within a
    SCROFULOUS (Short Composite ROtation For Undoing Length Over and Under Shoot) control,
    also knowns as CinS.

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the control.
    azimuthal_angle : float, optional
        The azimuthal position of the control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControl
        The driven control.

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    # Create a lookup table for rabi rotation and phase angles, taken from
    # the Cummings paper. Note: values in the paper are in degrees.
    def degrees_to_radians(angle_in_degrees):
        return angle_in_degrees / 180 * np.pi

    if np.isclose(rabi_rotation, np.pi):
        theta_1 = theta_3 = degrees_to_radians(180.)
        phi_1 = phi_3 = np.arccos(
            -np.pi * np.cos(theta_1) / 2 / theta_1 / np.sin(rabi_rotation / 2)
        )
        phi_2 = phi_1 - np.arccos(- np.pi / 2 / theta_1)
    elif np.isclose(rabi_rotation, 0.5 * np.pi):
        theta_1 = theta_3 = degrees_to_radians(115.2)
        phi_1 = phi_3 = np.arccos(
            -np.pi * np.cos(theta_1) / 2 / theta_1 / np.sin(rabi_rotation / 2)
        )
        phi_2 = phi_1 - np.arccos(- np.pi / 2 / theta_1)
    elif np.isclose(rabi_rotation, 0.25 * np.pi):
        theta_1 = theta_3 = degrees_to_radians(96.7)
        phi_1 = phi_3 = np.arccos(
            -np.pi * np.cos(theta_1) / 2 / theta_1 / np.sin(rabi_rotation / 2)
        )
        phi_2 = phi_1 - np.arccos(- np.pi / 2 / theta_1)
    else:
        raise ArgumentsValueError(
            'rabi_rotation angle must be either pi, pi/2 or pi/4',
            {'rabi_rotation': rabi_rotation})

    theta_2 = np.pi

    total_angles = []
    # Loop over all SCROFULOUS Rabi rotations (theta) and azimuthal angles (phi)
    # And make CORPSEs with those.
    for theta, phi in zip([theta_1, theta_2, theta_3], [phi_1, phi_2, phi_3]):
        k = np.arcsin(np.sin(theta / 2.) / 2.)
        angles = np.array([
            [2. * np.pi + theta / 2. - k, phi + azimuthal_angle],
            [2. * np.pi - 2. * k, np.pi + phi + azimuthal_angle],
            [theta / 2. - k, phi + azimuthal_angle]])
        total_angles.append(angles)

    total_angles = np.vstack(total_angles)

    rabi_rotations = total_angles[:, 0]

    rabi_rates = [maximum_rabi_rate] * 9
    azimuthal_angles = total_angles[:, 1]
    detunings = [0] * 9
    durations = [rabi_rotation_ / maximum_rabi_rate for rabi_rotation_ in rabi_rotations]

    return DrivenControl(
        rabi_rates=rabi_rates,
        azimuthal_angles=azimuthal_angles,
        detunings=detunings,
        durations=durations,
        **kwargs)


def _new_walsh_amplitude_modulated_filter_1_control(  # pylint: disable=invalid-name
        rabi_rotation=None,
        azimuthal_angle=0.,
        maximum_rabi_rate=2. * np.pi,
        **kwargs):
    """
    First order Walsh control with amplitude modulation.

    Parameters
    ----------
    rabi_rotation : float, optional
        The total rabi rotation to be performed by the control.
    maximum_rabi_rate : float, optional
        Defaults to 2.*np.pi
        The maximum rabi frequency for the control.
    azimuthal_angle : float, optional
        The azimuthal position of the control.
    kwargs : dict
        Other keywords required to make a qctrlopencontrols.DrivenControls.

    Returns
    -------
    qctrlopencontrols.DrivenControls
        The driven control.

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    (maximum_rabi_rate, rabi_rotation, azimuthal_angle) = _predefined_common_attributes(
        maximum_rabi_rate, rabi_rotation, azimuthal_angle)

    if np.isclose(rabi_rotation, np.pi):
        theta_plus = np.pi
        theta_minus = np.pi / 2.
    elif np.isclose(rabi_rotation, 0.5 * np.pi):
        theta_plus = np.pi * (2.5 + 0.65667825) / 4.
        theta_minus = np.pi * (2.5 - 0.65667825) / 4.
    elif np.isclose(rabi_rotation, 0.25 * np.pi):
        theta_plus = np.pi * (2.25 + 0.36256159) / 4.
        theta_minus = np.pi * (2.25 - 0.36256159) / 4.
    else:
        raise ArgumentsValueError(
            'rabi_rotation angle must be either pi, pi/2 or pi/4',
            {'rabi_rotation': rabi_rotation})

    rabi_rotations = [theta_plus, theta_minus, theta_minus, theta_plus]
    segment_duration = theta_plus / maximum_rabi_rate

    rabi_rates = [rabi_rotation_ / segment_duration for rabi_rotation_ in rabi_rotations]
    azimuthal_angles = [azimuthal_angle] * 4
    detunings = [0] * 4
    durations = [segment_duration] * 4

    return DrivenControl(
        rabi_rates=rabi_rates,
        azimuthal_angles=azimuthal_angles,
        detunings=detunings,
        durations=durations,
        **kwargs)
