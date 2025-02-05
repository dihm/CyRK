import numpy as np
from numba import njit

from CyRK import cyrk_ode


@njit
def diffeq_extra_outputs(t, y, output):
    extra_0 = (1. - 0.01 * y[1])
    extra_1 = (0.02 * y[0] - 1.)
    output[0] = extra_0 * y[0]
    output[1] = extra_1 * y[1]
    output[2] = extra_0
    output[3] = extra_1


initial_conds = np.asarray((20., 20.), dtype=np.complex128)
time_span = (0., 10.)
time_span_large = (0., 1000.)
rtol = 1.0e-7
atol = 1.0e-8


def test_extra_output_integration():
    """Check that the cython solver is able to run and capture additional outputs """

    time_domain, all_output, success, message = \
        cyrk_ode(diffeq_extra_outputs, time_span, initial_conds, capture_extra=True, num_extra=2)

    # Check that the ndarrays make sense
    assert type(time_domain) == np.ndarray
    assert time_domain.dtype == np.float64
    assert all_output.dtype == np.complex128
    assert time_domain.size > 1
    assert time_domain.size == all_output[0].size
    assert len(all_output.shape) == 2
    assert all_output.shape[0] == 4
    assert all_output[0].size == all_output[1].size
    assert all_output[0].size == all_output[2].size
    assert all_output[0].size == all_output[3].size

    # Check that the other output makes sense
    assert type(success) == bool
    assert success
    assert type(message) == str


def test_extra_output_integration_teval_no_extra_interpolation():
    """Check that the cython solver is able to run and capture additional outputs.
    Reduced t_eval used but no interpolation used on the extra parameters.
    """

    t_eval = np.linspace(time_span[0], time_span[1], 5)

    time_domain, all_output, success, message = \
        cyrk_ode(
            diffeq_extra_outputs, time_span, initial_conds, t_eval=t_eval,
            capture_extra=True, num_extra=2, interpolate_extra=False)

    # Check that the ndarrays make sense
    assert type(time_domain) == np.ndarray
    assert time_domain.dtype == np.float64
    assert all_output.dtype == np.complex128
    assert time_domain.size == t_eval.size
    assert time_domain.size == all_output[0].size
    assert len(all_output.shape) == 2
    assert all_output.shape[0] == 4
    assert all_output[0].size == all_output[1].size
    assert all_output[0].size == all_output[2].size
    assert all_output[0].size == all_output[3].size

    # Check that the other output makes sense
    assert type(success) == bool
    assert success
    assert type(message) == str


def test_extra_output_integration_teval_with_extra_interpolation():
    """Check that the cython solver is able to run and capture additional outputs
    Reduced t_eval used with interpolation used on the extra parameters.
    """

    t_eval = np.linspace(time_span[0], time_span[1], 5)

    time_domain, all_output, success, message = \
        cyrk_ode(
                diffeq_extra_outputs, time_span, initial_conds, t_eval=t_eval,
                capture_extra=True, num_extra=2, interpolate_extra=True)

    # Check that the ndarrays make sense
    assert type(time_domain) == np.ndarray
    assert time_domain.dtype == np.float64
    assert all_output.dtype == np.complex128
    assert time_domain.size == t_eval.size
    assert time_domain.size == all_output[0].size
    assert len(all_output.shape) == 2
    assert all_output.shape[0] == 4
    assert all_output[0].size == all_output[1].size
    assert all_output[0].size == all_output[2].size
    assert all_output[0].size == all_output[3].size

    # Check that the other output makes sense
    assert type(success) == bool
    assert success
    assert type(message) == str
