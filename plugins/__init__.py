"""
    Copyright 2013 KU Leuven Research and Development - iMinds - Distrinet

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Administrative Contact: dnet-project-office@cs.kuleuven.be
    Technical Contact: bart.vanbrabant@cs.kuleuven.be
"""

from Imp.plugins.base import plugin, Context
from Imp.export import dependency_manager
from Imp.resources import Resource

import hashlib
import os.path

@plugin
def unique_file(prefix : "string", seed : "string", suffix : "string") -> "string":
    return prefix + hashlib.md5(seed.encode("utf-8")).hexdigest() + suffix

@dependency_manager
def dir_before_file(model, resources):
    """
        If a file is defined on a host, then make the file depend on its parent directory
    """
    # loop over all resources to find files
    for _id, resource in resources.items():
        res_class = resource.model.__class__
        if resource.model.__module__ == "std" and res_class.__name__ == "File":
            model = resource.model
            host = model.host


            for dir in host.directories:
                dir_res = Resource.get_resource(dir)
                if dir_res is not None and os.path.dirname(resource.path) == dir_res.path:
                    #Make the File resource require the directory
                    resource.requires.add(dir_res.id)

@dependency_manager
def package_before_service(model, resources):
    """
        If a service is defined on a host, then make the service depend on all packages
        A brute force way of defining pkg->srv dependencies.
        Optional better way:
            1. somehow ask the package manager what service a package installs
            2. see if that service is described in the model
            3. if so: get the resource of that service and make it depend on the original package
    """
    # loop over all resources to find services
    for _id, resource in resources.items():
        res_class = resource.model.__class__
        if resource.model.__module__ == "std" and res_class.__name__ == "Service":
            model = resource.model
            host = model.host

            # now find all packages on the same host as the service and add the packages as a requirement
            for pkg in host.services:
                pkg_res = Resource.get_resource(pkg)
                if pkg_res is not None:
                        #Make the Service resource require the package
                        resource.requires.add(pkg_res.id)

@dependency_manager
def file_before_service(model, resources):
    """
        If a service is defined on a host, then make the service depend on all packages
        A brute force way of defining pkg->srv dependencies.
        Optional better way:
            1. somehow ask the package manager what service a package installs
            2. see if that service is described in the model
            3. if so: get the resource of that service and make it depend on the original package
    """
    # loop over all resources to find services
    for _id, resource in resources.items():
        res_class = resource.model.__class__
        if resource.model.__module__ == "std" and res_class.__name__ == "Service":
            model = resource.model
            host = model.host

            # now find all packages on the same host as the service and add the packages as a requirement
            for file in host.files:
                file_res = Resource.get_resource(file)
                if file_res is not None:
                        #Make the Service resource require the package
                        resource.requires.add(file_res.id)