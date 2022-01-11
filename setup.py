from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

with open("LICENSE", "r", encoding="utf-8") as f:
    license = f.read()

setup(
    name="bcap",
    version="0.2.0",
    description="b-CAP client library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Keiji Okuhara",
    author_email="ihpen428ye4w7tb-geek@yahoo.co.jp",
    url="https://github.com/keioku/bcap-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license=license,
    packages=find_packages(),
    python_requires=">=3.6",
)
