# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from setuptools import setup, find_packages


setup(
    name='mycroft-core',
    version="2021.1.11",
    license='Apache-2.0',
    author='Mycroft A.I.',
    author_email='devs@mycroft.ai',
    url='https://github.com/MycroftAI/mycroft-core',
    description='Mycroft Core',
    install_requires=["requests",
                      "pyee",
                      "lingua-franca",
                      "pyxdg",
                      "mycroft-messagebus-client",
                      "inflection",
                      "psutil",
                      "fasteners",
                      "requests-futures"],
    packages=find_packages(include=['mycroft*']),
    include_package_data=True,

)
