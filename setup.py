from setuptools import setup, find_packages

setup(name="wookie",
      version="0.0.1",
      packages=find_packages("src"),
      package_dir={"": "src"},
      install_requires=["flask"],
      setup_requires=["pytest-runner"],
      tests_require=["pytest", "coverage"])
