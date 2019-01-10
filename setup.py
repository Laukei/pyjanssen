import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name = "pyjanssen",
	version = "0.1.1",
	author = "Robert Heath",
	author_email = "rob@robheath.me.uk",
	description = "Wrapper for cacli.exe for Janssen Precision Engineering MCM module",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/Laukei/pyjanssen",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: Microsoft :: Windows",
		"Development Status :: 3 - Alpha"]

	)