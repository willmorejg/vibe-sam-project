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

import unittest
import sys
import os

# Add the parent directory to the path so that imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == "__main__":
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Run tests individually to isolate failures
    print("Running model tests...")
    model_suite = loader.discover(start_dir, pattern="test_models.py")
    model_result = unittest.TextTestRunner(verbosity=2).run(model_suite)
    
    print("\nRunning repository tests...")
    repo_suite = loader.discover(start_dir, pattern="test_repositories.py")
    repo_result = unittest.TextTestRunner(verbosity=2).run(repo_suite)
    
    print("\nRunning service tests...")
    service_suite = loader.discover(start_dir, pattern="test_services.py")
    service_result = unittest.TextTestRunner(verbosity=2).run(service_suite)
    
    # Determine overall success
    success = all([
        model_result.wasSuccessful(),
        repo_result.wasSuccessful(),
        service_result.wasSuccessful()
    ])
    
    if not success:
        print("\nSome tests failed. Check the error messages above.")
    else:
        print("\nAll tests passed successfully!")
    
    sys.exit(not success)
