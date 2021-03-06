#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import os

from pymongo import MongoClient

from testcontainers.core.generic import DockerContainer


class MongoDbContainer(DockerContainer):
    MONGO_INITDB_ROOT_USERNAME = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "test")
    MONGO_INITDB_ROOT_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "test")
    MONGO_DB = os.environ.get("MONGO_DB", "test")

    def __init__(self, image="mongodb:latest"):
        super(MongoDbContainer, self).__init__(image=image)
        self.command = "mongo"
        self.port_to_expose = 27017
        self.with_exposed_ports(self.port_to_expose)

    def _configure(self):

        self.with_env("MONGO_INITDB_ROOT_USERNAME", self.MONGO_INITDB_ROOT_USERNAME)
        self.with_env("MONGO_INITDB_ROOT_PASSWORD", self.MONGO_INITDB_ROOT_PASSWORD)
        self.with_env("MONGO_DB", self.MONGO_DB)

    def get_connection_url(self):
        port = self.get_exposed_port(self.port_to_expose)
        return "mongodb://{}:{}".format(self.get_container_host_ip(), port)

    def get_connection_client(self):
        return MongoClient("mongodb://{}:{}".format(self.get_container_host_ip(),
                                                    self.get_exposed_port(self.port_to_expose)))
