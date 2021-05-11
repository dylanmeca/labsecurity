import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setuptools.setup(
    name="labsecurity", 
    version="1.6",
    author="dylan14567",
    author_email="",
    description="labsecurity is a framework and its use is for ethical hacking and computer security",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dylan14567/labsecurity",
    scripts = ['labsecurity'],
    project_urls={
        "Bug Tracker": "https://github.com/dylan14567/labsecurity/issues",
        "Documentation": "https://dylan14567.github.io/2021/04/07/labtool-documentation.html",
    },
    install_requires=[
        "colorama",
        "requests",
        "wheel",
        "python-nmap",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="lab_tool",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
)
