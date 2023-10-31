from warnings import simplefilter
from glob import glob

from setuptools import setup
from setuptools import SetuptoolsDeprecationWarning
from pkg_resources import PkgResourcesDeprecationWarning

simplefilter("ignore", category=SetuptoolsDeprecationWarning)
simplefilter("ignore", category=PkgResourcesDeprecationWarning)

package_name = "launch_unifier"

setup(
    name=package_name,
    version="0.1.0",
    packages=[package_name],
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (f"share/{package_name}/templates", glob("templates/*")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="M. Fatih Cırıt",
    maintainer_email="mfc@leodrive.ai",
    description="Launch Unifier package.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            f"{package_name}={package_name}.bin.{package_name}:main",
        ],
    },
)
