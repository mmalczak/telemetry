The project provides an application to read data from cpufreq_adaptive
processor frequency controller.
Overmore, it provides module to parse the data for matlab as well as
python script to visualize the data.

Before there existed branches for each supported kernel version.
The reason for it was a difference in time structure:
old kernel versions were using microseconds while newer kernel versions
use nanoseconds. From now on it will be assumed, that telemetry module
uses nanoseconds, and in case of using different units by kernel,
the values should be recalculated. This will allow not to create different
branches for every kernel release, with just minor changes.
