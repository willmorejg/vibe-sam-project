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

import duckdb
import os
from pathlib import Path

DB_PATH = "archman.ddb"


def get_connection():
    """Get a connection to the DuckDB database."""
    # Create directory if it doesn't exist
    os.makedirs(Path(DB_PATH).parent, exist_ok=True)
    
    # Connect to the database
    conn = duckdb.connect(DB_PATH)
    
    # Create tables if they don't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS components (
            uuid VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            type VARCHAR NOT NULL,
            properties JSON
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS systems (
            uuid VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            components JSON,
            properties JSON
        )
    """)
    
    return conn
