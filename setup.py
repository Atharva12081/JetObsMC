from setuptools import find_packages, setup

setup(
    name="jetobsmc",
    version="0.3.0",
    description="JetObsMC: unified jet observable toolkit for Monte Carlo validation workflows.",
    url="https://github.com/Atharva12081/JetObsMC",
    license="MIT",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.10",
    install_requires=["numpy>=1.24"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "notebook>=7.0",
            "matplotlib>=3.8",
            "scikit-learn>=1.4",
            "black>=24.0",
        ]
    },
)
