# Copyright 2021 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable, List, Optional

from kfp.v2.components import python_component
from kfp.v2.components import structures
from kfp.v2.components import component_factory


def create_graph_component_from_pipeline(pipeline: Callable):
    """Implementation for the @pipeline decorator.

    The decorator is defined under pipeline_context.py. This function wraps
    pipeline into a dag.
    """
    print('creating ', pipeline.__name__)
    # component_spec = component_factory.extract_component_interface(pipeline)
    # component_spec.implementation = structures.Implementation(
    #     graph=structures.DagSpec(
    #         tasks={},
    #         outputs={},
    #     ))
    # print('implementation', component_spec)

    # return python_component.PythonComponent(
    #     component_spec=component_spec, python_func=pipeline)
