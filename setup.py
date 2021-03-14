import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    README = f.read()

setuptools.setup(
    name="lab_tool", 
    version="1.0",
    author="dylan14567",
    author_email="",
    description="lab_tool is a system that allows you to do ethical hacking tests",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/dylan14567/lab_tool",
    scripts = ['lab_tool'],
    project_urls={
        "Bug Tracker": "https://github.com/dylan14567/lab_tool/issues",
    },
    install_requires=[
        "colorama",
        "requests",
        "wheel",
        "nmap"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="server",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
)
