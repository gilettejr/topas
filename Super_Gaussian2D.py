import numpy as np

from astropy import units as u
from astropy.units import UnitsError

from astropy.modeling import Fittable2DModel
from astropy.modeling.parameters import InputParameterError, Parameter
from astropy.modeling.utils import ellipse_extent

TWOPI = 2 * np.pi
FLOAT_EPSILON = float(np.finfo(np.float32).tiny)

# Note that we define this here rather than using the value defined in
# astropy.stats to avoid importing astropy.stats every time astropy.modeling
# is loaded.
GAUSSIAN_SIGMA_TO_FWHM = 2.0 * np.sqrt(2.0 * np.log(2.0))


class Super_Gaussian2D(Fittable2DModel):
    r"""
    Two dimensional Gaussian model.

    Parameters
    ----------
    amplitude : float or `~astropy.units.Quantity`.
        Amplitude (peak value) of the Gaussian.
    x_mean : float or `~astropy.units.Quantity`.
        Mean of the Gaussian in x.
    y_mean : float or `~astropy.units.Quantity`.
        Mean of the Gaussian in y.
    x_stddev : float or `~astropy.units.Quantity` or None.
        Standard deviation of the Gaussian in x before rotating by theta. Must
        be None if a covariance matrix (``cov_matrix``) is provided. If no
        ``cov_matrix`` is given, ``None`` means the default value (1).
    y_stddev : float or `~astropy.units.Quantity` or None.
        Standard deviation of the Gaussian in y before rotating by theta. Must
        be None if a covariance matrix (``cov_matrix``) is provided. If no
        ``cov_matrix`` is given, ``None`` means the default value (1).
    theta : float or `~astropy.units.Quantity`, optional.
        The rotation angle as an angular quantity
        (`~astropy.units.Quantity` or `~astropy.coordinates.Angle`)
        or a value in radians (as a float). The rotation angle
        increases counterclockwise. Must be `None` if a covariance matrix
        (``cov_matrix``) is provided. If no ``cov_matrix`` is given,
        `None` means the default value (0).
    cov_matrix : ndarray, optional
        A 2x2 covariance matrix. If specified, overrides the ``x_stddev``,
        ``y_stddev``, and ``theta`` defaults.

    Notes
    -----
    Either all or none of input ``x, y``, ``[x,y]_mean`` and ``[x,y]_stddev``
    must be provided consistently with compatible units or as unitless numbers.

    Model formula:

        .. math::

            f(x, y) = A e^{-a\left(x - x_{0}\right)^{2}  -b\left(x - x_{0}\right)
            \left(y - y_{0}\right)  -c\left(y - y_{0}\right)^{2}}

    Using the following definitions:

        .. math::
            a = \left(\frac{\cos^{2}{\left (\theta \right )}}{2 \sigma_{x}^{2}} +
            \frac{\sin^{2}{\left (\theta \right )}}{2 \sigma_{y}^{2}}\right)

            b = \left(\frac{\sin{\left (2 \theta \right )}}{2 \sigma_{x}^{2}} -
            \frac{\sin{\left (2 \theta \right )}}{2 \sigma_{y}^{2}}\right)

            c = \left(\frac{\sin^{2}{\left (\theta \right )}}{2 \sigma_{x}^{2}} +
            \frac{\cos^{2}{\left (\theta \right )}}{2 \sigma_{y}^{2}}\right)

    If using a ``cov_matrix``, the model is of the form:
        .. math::
            f(x, y) = A e^{-0.5 \left(
                    \vec{x} - \vec{x}_{0}\right)^{T} \Sigma^{-1} \left(\vec{x} - \vec{x}_{0}
                \right)}

    where :math:`\vec{x} = [x, y]`, :math:`\vec{x}_{0} = [x_{0}, y_{0}]`,
    and :math:`\Sigma` is the covariance matrix:

        .. math::
            \Sigma = \left(\begin{array}{ccc}
            \sigma_x^2               & \rho \sigma_x \sigma_y \\
            \rho \sigma_x \sigma_y   & \sigma_y^2
            \end{array}\right)

    :math:`\rho` is the correlation between ``x`` and ``y``, which should
    be between -1 and +1.  Positive correlation corresponds to a
    ``theta`` in the range 0 to 90 degrees.  Negative correlation
    corresponds to a ``theta`` in the range of 0 to -90 degrees.

    See [1]_ for more details about the 2D Gaussian function.

    See Also
    --------
    Gaussian1D, Box2D, Moffat2D

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Gaussian_function
    """

    amplitude = Parameter(default=1, description="Amplitude of the Gaussian")
    x_mean = Parameter(
        default=0, description="Peak position (along x axis) of Gaussian"
    )
    y_mean = Parameter(
        default=0, description="Peak position (along y axis) of Gaussian"
    )
    x_stddev = Parameter(
        default=1, description="Standard deviation of the Gaussian (along x axis)"
    )
    y_stddev = Parameter(
        default=1, description="Standard deviation of the Gaussian (along y axis)"
    )

    power = Parameter(default=1.0, description=(
        'Power to characterise super Gaussian flat top'))

    def __init__(
        self,
        amplitude=amplitude.default,
        x_mean=x_mean.default,
        y_mean=y_mean.default,
        x_stddev=None,
        y_stddev=None,
        power=None,
        cov_matrix=None,
        **kwargs,
    ):
        if cov_matrix is None:
            if x_stddev is None:
                x_stddev = self.__class__.x_stddev.default
            if y_stddev is None:
                y_stddev = self.__class__.y_stddev.default
            if power is None:
                power = self.__class__.power.default
        else:
            if x_stddev is not None or y_stddev is not None or power is not None:
                raise InputParameterError(
                    "Cannot specify both cov_matrix and x/y_stddev/theta/power"
                )
            # Compute principle coordinate system transformation
            # don't know how to make cov_matrix work with power
            cov_matrix = np.array(cov_matrix)

            if cov_matrix.shape != (2, 2):
                raise ValueError("Covariance matrix must be 2x2")

            eig_vals, eig_vecs = np.linalg.eig(cov_matrix)
            x_stddev, y_stddev = np.sqrt(eig_vals)
            y_vec = eig_vecs[:, 0]
            theta = np.arctan2(y_vec[1], y_vec[0])

        # Ensure stddev makes sense if its bounds are not explicitly set.
        # stddev must be non-zero and positive.
        # TODO: Investigate why setting this in Parameter above causes
        #       convolution tests to hang.
        kwargs.setdefault("bounds", {})
        kwargs["bounds"].setdefault("x_stddev", (FLOAT_EPSILON, None))
        kwargs["bounds"].setdefault("y_stddev", (FLOAT_EPSILON, None))

        super().__init__(
            amplitude=amplitude,
            x_mean=x_mean,
            y_mean=y_mean,
            x_stddev=x_stddev,
            y_stddev=y_stddev,
            power=power,
            ** kwargs,
        )

    @property
    def x_fwhm(self):
        """Gaussian full width at half maximum in X."""
        return self.x_stddev * GAUSSIAN_SIGMA_TO_FWHM

    @property
    def y_fwhm(self):
        """Gaussian full width at half maximum in Y."""
        return self.y_stddev * GAUSSIAN_SIGMA_TO_FWHM

    def bounding_box(self, factor=5.5):
        """
        Tuple defining the default ``bounding_box`` limits in each dimension,
        ``((y_low, y_high), (x_low, x_high))``

        The default offset from the mean is 5.5-sigma, corresponding
        to a relative error < 1e-7. The limits are adjusted for rotation.

        Parameters
        ----------
        factor : float, optional
            The multiple of `x_stddev` and `y_stddev` used to define the limits.
            The default is 5.5.

        Examples
        --------
        >>> from astropy.modeling.models import Gaussian2D
        >>> model = Gaussian2D(x_mean=0, y_mean=0, x_stddev=1, y_stddev=2)
        >>> model.bounding_box
        ModelBoundingBox(
            intervals={
                x: Interval(lower=-5.5, upper=5.5)
                y: Interval(lower=-11.0, upper=11.0)
            }
            model=Gaussian2D(inputs=('x', 'y'))
            order='C'
        )

        This range can be set directly (see: `Model.bounding_box
        <astropy.modeling.Model.bounding_box>`) or by using a different factor
        like:

        >>> model.bounding_box = model.bounding_box(factor=2)
        >>> model.bounding_box
        ModelBoundingBox(
            intervals={
                x: Interval(lower=-2.0, upper=2.0)
                y: Interval(lower=-4.0, upper=4.0)
            }
            model=Gaussian2D(inputs=('x', 'y'))
            order='C'
        )
        """

        a = factor * self.x_stddev
        b = factor * self.y_stddev
        dx, dy = ellipse_extent(a, b, self.theta)

        return (
            (self.y_mean - dy, self.y_mean + dy),
            (self.x_mean - dx, self.x_mean + dx),
        )

    @staticmethod
    def evaluate(x, y, amplitude, x_mean, y_mean, x_stddev, y_stddev, power):
        #print(amplitude, x_mean, y_mean, x_stddev, y_stddev, power)
        """Two dimensional Gaussian function"""

        xstd2 = x_stddev**2
        ystd2 = y_stddev**2
        xdiff = x - x_mean
        ydiff = y - y_mean
        xdiff2 = xdiff**2
        ydiff2 = ydiff**2
        exponent = np.divide(xdiff2, 2*xstd2)+np.divide(ydiff2, 2*ystd2)
        return amplitude*np.exp(-(exponent**power))

    @staticmethod
    def fit_deriv(x, y, amplitude, x_mean, y_mean, x_stddev, y_stddev, power):
        """Two dimensional Gaussian function derivative with respect to parameters"""

        xstd2 = x_stddev**2
        ystd2 = y_stddev**2
        xstd3 = x_stddev**3
        ystd3 = y_stddev**3
        xdiff = x - x_mean
        ydiff = y - y_mean
        xdiff2 = xdiff**2
        ydiff2 = ydiff**2
        exponent = np.divide(xdiff2, 2*xstd2)+np.divide(ydiff2, 2*ystd2)
        exponent_factor = (exponent**(power-1))*np.exp(-(exponent**(power)))
        print(exponent)
        g = amplitude*np.exp(-exponent**power)
        p = power
        dg_dA = g / amplitude
        dg_dx_mean = (1/xstd2)*amplitude*power*xdiff * \
            exponent_factor
        dg_dy_mean = (1/ystd2)*amplitude*power*ydiff * \
            exponent_factor
        dg_dx_stddev = (1/xstd3)*amplitude*power*xdiff2*exponent_factor
        dg_dy_stddev = (1/ystd3)*amplitude*power*ydiff2*exponent_factor
        dg_dpower = amplitude*(-2**(-p))*(2*exponent)**p * \
            np.log(exponent)*np.exp(-2**(-p)*(2*exponent)**p)

        #print('using derivative, everything is fucked')
        return [dg_dA, dg_dx_mean, dg_dy_mean, dg_dx_stddev, dg_dy_stddev, dg_dpower]

    @property
    def input_units(self):
        if self.x_mean.unit is None and self.y_mean.unit is None:
            return None
        return {self.inputs[0]: self.x_mean.unit, self.inputs[1]: self.y_mean.unit}

    def _parameter_units_for_data_units(self, inputs_unit, outputs_unit):
        # Note that here we need to make sure that x and y are in the same
        # units otherwise this can lead to issues since rotation is not well
        # defined.
        if inputs_unit[self.inputs[0]] != inputs_unit[self.inputs[1]]:
            raise UnitsError("Units of 'x' and 'y' inputs should match")
        return {
            "x_mean": inputs_unit[self.inputs[0]],
            "y_mean": inputs_unit[self.inputs[0]],
            "x_stddev": inputs_unit[self.inputs[0]],
            "y_stddev": inputs_unit[self.inputs[0]],
            "amplitude": outputs_unit[self.outputs[0]],
            'power': outputs_unit[self.outputs[0]]
        }
