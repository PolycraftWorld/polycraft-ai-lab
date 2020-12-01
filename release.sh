#!/usr/bin/env bash
# TODO: Wrap in virtualenv, maybe a Docker container for building

# Ensure dependencies are installed before release
echo -e "\n=======Preparing dependencies for release======="
pip3 install -r requirements.txt

# Install build tools
pip3 install build twine

# Create distribution archives for PAL
echo -e "\n==========Creating archives for release========="
# TODO: Handle virtual environment issue
python3 -m build --sdist --wheel --no-isolation
python setup.py sdist bdist_wheel

# Upload to PyPI
echo -e "\n================Uploading to PyPI==============="
# Verify the long_description in setup.py makes sense
twine check dist/*

if [ "$1" = "--release" ]; then
    echo "Uploading to PyPI"
    twine upload dist/*
else
    echo "Uploading to test PyPI repository"
    twine upload dist/* --repository testpypi
fi

