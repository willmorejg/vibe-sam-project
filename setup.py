#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup, find_packages

setup(
    name="vibe-sam-project",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "pydantic>=1.8.0",
        "python-multipart>=0.0.5",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5",
            "httpx>=0.19.0",  # For TestClient in testing
            "pytest-cov>=2.12.1",
            "black>=21.7b0",
            "isort>=5.9.3",
            "flake8>=3.9.2",
        ],
    },
    python_requires=">=3.7",
    author="Your Name",
    author_email="your.email@example.com",
    description="A FastAPI project for component and system management",
    keywords="fastapi, api, components, systems",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
