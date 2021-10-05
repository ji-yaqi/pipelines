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
"""Definitions for component spec."""

import dataclasses
import itertools
import json
from typing import Any, Dict, Mapping, Optional, Sequence, Union
try:
    from typing import OrderedDict
except ImportError:
    from collections import OrderedDict
from kfp.components import _components
from kfp.components import structures
import pydantic
import yaml


class BaseModel(pydantic.BaseModel):

    class Config:
        allow_population_by_field_name = True


class InputSpec(BaseModel):
    """Component input definitions.

    Attributes:
        type: The type of the input.
        default: Optional; the default value for the input.
    """
    # TODO(ji-yaqi): Add logic to cast default value into the specified type.
    type: str
    default: Optional[Union[str, int, float, bool, dict, list]] = None


class OutputSpec(BaseModel):
    """Component output definitions.

    Attributes:
        type: The type of the output.
    """
    type: str


class BasePlaceholder(BaseModel):
    """Base class for placeholders that could appear in container cmd and args.
    """
    pass


class InputValuePlaceholder(BasePlaceholder):
    """Class that holds input value for conditional cases.

    Attributes:
        input_name: name of the input.
    """
    input_name: str = pydantic.Field(alias='inputValue')


class InputPathPlaceholder(BasePlaceholder):
    """Class that holds input path for conditional cases.

    Attributes:
        input_name: name of the input.
    """
    input_name: str = pydantic.Field(alias='inputPath')


class InputUriPlaceholder(BasePlaceholder):
    """Class that holds input uri for conditional cases.

    Attributes:
        input_name: name of the input.
    """
    input_name: str = pydantic.Field(alias='inputUri')


class OutputPathPlaceholder(BasePlaceholder):
    """Class that holds output path for conditional cases.

    Attributes:
        output_name: name of the output.
    """
    output_name: str = pydantic.Field(alias='outputPath')


class OutputUriPlaceholder(BasePlaceholder):
    """Class that holds output uri for conditional cases.

    Attributes:
        output_name: name of the output.
    """
    output_name: str = pydantic.Field(alias='outputUri')


ValidCommandArgs = Union[str, InputValuePlaceholder, InputPathPlaceholder,
                         InputUriPlaceholder, OutputPathPlaceholder,
                         OutputUriPlaceholder, 'IfPresentPlaceholder',
                         'ConcatPlaceholder']


class ConcatPlaceholder(BasePlaceholder):
    """Class that extends basePlaceholders for concatenation.

    Attributes:
        concat: string or ValidCommandArgs for concatenation.
    """
    concat: Sequence[ValidCommandArgs]


class IfPresentPlaceholderStructure(BaseModel):
    """Class that holds structure for conditional cases.

    Attributes:
        input_name: name of the input/output.
        then: If the input/output specified in name is present,
            the command-line argument will be replaced at run-time by the
            expanded value of then.
        otherwise: If the input/output specified in name is not present,
            the command-line argument will be replaced at run-time by the
            expanded value of otherwise.
    """
    input_name: str = pydantic.Field(alias='inputName')
    then: Sequence[ValidCommandArgs]
    otherwise: Optional[Sequence[ValidCommandArgs]] = None

    @pydantic.validator('otherwise')
    def empty_sequence(cls, v):
        if v == []:
            return None
        return v


class IfPresentPlaceholder(BasePlaceholder):
    """Class that extends basePlaceholders for conditional cases.

    Attributes:
        if_present (ifPresent): holds structure for conditional cases.
    """
    if_present: IfPresentPlaceholderStructure = pydantic.Field(
        alias='ifPresent')


IfPresentPlaceholderStructure.update_forward_refs()
IfPresentPlaceholder.update_forward_refs()
ConcatPlaceholder.update_forward_refs()


@dataclasses.dataclass
class ResourceSpec:
    """The resource requirements of a container execution.

    Attributes:
        cpu_limit: Optional; the limit of the number of vCPU cores.
        memory_limit: Optional; the memory limit in GB.
        accelerator_type: Optional; the type of accelerators attached to the
            container.
        accelerator_count: Optional; the number of accelerators attached.
    """
    cpu_limit: Optional[float] = None
    memory_limit: Optional[float] = None
    accelerator_type: Optional[str] = None
    accelerator_count: Optional[int] = None


class ContainerSpec(BaseModel):
    """Container implementation definition.

    Attributes:
        image: The container image.
        commands: Optional; the container entrypoint.
        arguments: Optional; the arguments to the container entrypoint.
        env: Optional; the environment variables to be passed to the container.
        resources: Optional; the specification on the resource requirements.
    """
    image: str
    commands: Optional[Sequence[ValidCommandArgs]] = None
    arguments: Optional[Sequence[ValidCommandArgs]] = None
    env: Optional[Mapping[str, ValidCommandArgs]] = None
    resources: Optional[ResourceSpec] = None

    @pydantic.validator('commands', 'arguments')
    def empty_sequence(cls, v):
        if v == []:
            return None
        return v

    @pydantic.validator('env')
    def empty_map(cls, v):
        if v == {}:
            return None
        return v


class TaskSpec(BaseModel):
    """The spec of a pipeline task.

    Attributes:
        name: The name of the task.
        inputs: The sources of task inputs. Constant values or PipelineParams.
        dependent_tasks: The list of upstream tasks.
        enable_caching: Whether or not to enable caching for the task.
        component_ref: The name of a component spec this task is based on.
        trigger_condition: Optional; an expression which will be evaluated into
         a boolean value. True to trigger the task to run.
        trigger_strategy: Optional; when the task will be ready to be triggered.
            Valid values include: "TRIGGER_STRATEGY_UNSPECIFIED",
            "ALL_UPSTREAM_TASKS_SUCCEEDED", and "ALL_UPSTREAM_TASKS_COMPLETED".
        iterator_items: Optional; the items to iterate on. A constant value or
         a PipelineParam.
        iterator_item_input: Optional; the name of the input which has the item
         from the [items][] collection.
    """
    name: str
    inputs: Mapping[str, Any]
    dependent_tasks: Sequence[str]
    enable_caching: bool
    component_ref: str
    trigger_condition: Optional[str] = None
    trigger_strategy: Optional[str] = None
    iterator_items: Optional[Any] = None
    iterator_item_input: Optional[str] = None


class DagSpec(BaseModel):
    """DAG(graph) implementation definition.

    Attributes:
        tasks: The tasks inside the DAG.
        outputs: Defines how the outputs of the dag are linked to the sub tasks.
    """
    tasks: Mapping[str, TaskSpec]
    # TODO(chensun): revisit if we need a DagOutputsSpec class.
    outputs: Mapping[str, Any]


class ImporterSpec(BaseModel):
    """ImporterSpec definition.

    Attributes:
        artifact_uri: The URI of the artifact.
        type_schema: The type of the artifact.
        reimport: Whether or not import an artifact regardless it has been
         imported before.
        metadata: Optional; the properties of the artifact.
    """
    artifact_uri: str
    type_schema: str
    reimport: bool
    metadata: Optional[Mapping[str, Any]] = None


class Implementation(BaseModel):
    """Implementation definition.

    Attributes:
        container: container implementation details.
        graph: graph implementation details.
        importer: importer implementation details.
    """
    container: Optional[ContainerSpec] = None
    graph: Optional[DagSpec] = None
    importer: Optional[ImporterSpec] = None


class ComponentSpec(BaseModel):
    """The definition of a component.

    Attributes:
        name: The name of the component.
        description: Optional; the description of the component.
        inputs: Optional; the input definitions of the component.
        outputs: Optional; the output definitions of the component.
        implementation: The implementation of the component. Either an executor
            (container, importer) or a DAG consists of other components.
    """

    name: str
    description: Optional[str] = None
    inputs: Optional[OrderedDict[str, InputSpec]] = None
    outputs: Optional[OrderedDict[str, OutputSpec]] = None
    implementation: Implementation

    @pydantic.validator('inputs', 'outputs')
    def empty_map(cls, v):
        if v == {}:
            return None
        return v

    @pydantic.root_validator
    def validate_placeholders(cls, values):
        if values.get('implementation').container is None:
            return values
        containerSpec: ContainerSpec = values.get('implementation').container

        try:
            valid_inputs = values.get('inputs').keys()
        except AttributeError:
            valid_inputs = []

        try:
            valid_outputs = values.get('outputs').keys()
        except AttributeError:
            valid_outputs = []

        for arg in itertools.chain((containerSpec.commands or []),
                                   (containerSpec.arguments or [])):
            cls._check_valid_placeholder_reference(valid_inputs, valid_outputs,
                                                   arg)

        return values

    @classmethod
    def _check_valid_placeholder_reference(cls, valid_inputs: Sequence[str],
                                           valid_outputs: Sequence[str],
                                           arg: ValidCommandArgs) -> None:
        """Validates placeholder reference existing input/output names.

        Args:
            valid_inputs: The existing input names.
            valid_outputs: The existing output names.
            arg: The placeholder argument for checking.

        Raises:
            ValueError: if any placeholder references a non-existing input or
                output.
            TypeError: if any argument is neither a str nor a placeholder
                instance.
        """

        if isinstance(
                arg,
            (InputValuePlaceholder, InputPathPlaceholder, InputUriPlaceholder)):
            if arg.input_name not in valid_inputs:
                raise ValueError(
                    f'Argument "{arg}" references non-existing input.')
        elif isinstance(arg, (OutputPathPlaceholder, OutputUriPlaceholder)):
            if arg.output_name not in valid_outputs:
                raise ValueError(
                    f'Argument "{arg}" references non-existing output.')
        elif isinstance(arg, IfPresentPlaceholder):
            if arg.if_present.input_name not in valid_inputs:
                raise ValueError(
                    f'Argument "{arg}" references non-existing input.')
            for placeholder in itertools.chain(arg.if_present.then,
                                               arg.if_present.otherwise):
                cls._check_valid_placeholder_reference(valid_inputs,
                                                       valid_outputs,
                                                       placeholder)
        elif isinstance(arg, ConcatPlaceholder):
            for placeholder in arg.concat:
                cls._check_valid_placeholder_reference(valid_inputs,
                                                       valid_outputs,
                                                       placeholder)
        elif not isinstance(arg, str):
            raise TypeError(f'Unexpected argument "{arg}".')

    @classmethod
    def from_v1_component_spec(
            cls,
            v1_component_spec: structures.ComponentSpec) -> 'ComponentSpec':
        """Converts V1 ComponentSpec to V2 ComponentSpec.

        Args:
            v1_component_spec: The V1 ComponentSpec.

        Returns:
            Component spec in the form of V2 ComponentSpec.

        Raises:
            ValueError: If implementation is not found.
            TypeError: if any argument is neither a str nor Dict.
        """
        component_dict = v1_component_spec.to_dict()
        if component_dict.get('implementation') is None:
            raise ValueError('Implementation field not found')
        if 'container' not in component_dict.get('implementation'):
            raise NotImplementedError

        def _transform_arg(arg: Union[str, Dict[str, str]]) -> ValidCommandArgs:
            if isinstance(arg, str):
                return arg
            if 'inputValue' in arg:
                return InputValuePlaceholder(input_name=arg['inputValue'])
            if 'inputPath' in arg:
                return InputPathPlaceholder(input_name=arg['inputPath'])
            if 'inputUri' in arg:
                return InputUriPlaceholder(input_name=arg['inputUri'])
            if 'outputPath' in arg:
                return OutputPathPlaceholder(output_name=arg['outputPath'])
            if 'outputUri' in arg:
                return OutputUriPlaceholder(output_name=arg['outputUri'])
            if 'if' in arg:
                if_placeholder_values = arg['if']
                if_placeholder_values_then = list(if_placeholder_values['then'])
                try:
                    if_placeholder_values_else = list(
                        if_placeholder_values['else'])
                except KeyError:
                    if_placeholder_values_else = []

                IfPresentPlaceholderStructure.update_forward_refs()
                return IfPresentPlaceholder(
                    if_present=IfPresentPlaceholderStructure(
                        input_name=if_placeholder_values['cond']['isPresent'],
                        then=list(
                            _transform_arg(val)
                            for val in if_placeholder_values_then),
                        otherwise=list(
                            _transform_arg(val)
                            for val in if_placeholder_values_else)))
            if 'concat' in arg:
                ConcatPlaceholder.update_forward_refs()

                return ConcatPlaceholder(
                    concat=list(_transform_arg(val) for val in arg['concat']))
            raise ValueError(
                f'Unexpected command/argument type: "{arg}" of type "{type(arg)}".'
            )

        implementation = component_dict['implementation']['container']
        implementation['commands'] = [
            _transform_arg(command)
            for command in implementation.pop('command', [])
        ]
        implementation['arguments'] = [
            _transform_arg(command)
            for command in implementation.pop('args', [])
        ]
        implementation['env'] = {
            key: _transform_arg(command)
            for key, command in implementation.pop('env', {}).items()
        }
        container_spec = ContainerSpec.parse_obj(implementation)

        return ComponentSpec(
            name=component_dict.get('name', 'name'),
            description=component_dict.get('description'),
            implementation=Implementation(container=container_spec,),
            inputs={
                spec['name']: InputSpec(
                    type=spec.get('type', 'Artifact'),
                    default=spec.get('default', None))
                for spec in component_dict.get('inputs', [])
            },
            outputs={
                spec['name']: OutputSpec(type=spec.get('type', 'Artifact'))
                for spec in component_dict.get('outputs', [])
            })

    def to_v1_component_spec(self) -> structures.ComponentSpec:
        """Converts to v1 ComponentSpec.

        Returns:
            Component spec in the form of V1 ComponentSpec.

        Needed until downstream accept new ComponentSpec.
        """

        def _transform_arg(arg: ValidCommandArgs) -> Any:
            if isinstance(arg, str):
                return arg
            if isinstance(arg, InputValuePlaceholder):
                return structures.InputValuePlaceholder(arg.input_name)
            if isinstance(arg, InputPathPlaceholder):
                return structures.InputPathPlaceholder(arg.input_name)
            if isinstance(arg, InputUriPlaceholder):
                return structures.InputUriPlaceholder(arg.input_name)
            if isinstance(arg, OutputPathPlaceholder):
                return structures.OutputPathPlaceholder(arg.output_name)
            if isinstance(arg, OutputUriPlaceholder):
                return structures.OutputUriPlaceholder(arg.output_name)
            if isinstance(arg, IfPresentPlaceholder):
                return structures.IfPlaceholder(arg.if_present)
            if isinstance(arg, ConcatPlaceholder):
                return structures.ConcatPlaceholder(arg.concat)
            raise ValueError(
                f'Unexpected command/argument type: "{arg}" of type "{type(arg)}".'
            )

        return structures.ComponentSpec(
            name=self.name,
            inputs=[
                structures.InputSpec(
                    name=name,
                    type=input_spec.type,
                    default=input_spec.default,
                ) for name, input_spec in self.inputs.items()
            ],
            outputs=[
                structures.OutputSpec(
                    name=name,
                    type=output_spec.type,
                ) for name, output_spec in self.outputs.items()
            ],
            implementation=structures.ContainerImplementation(
                container=structures.ContainerSpec(
                    image=self.implementation.container.image,
                    command=[
                        _transform_arg(cmd)
                        for cmd in self.implementation.container.commands or []
                    ],
                    args=[
                        _transform_arg(arg) for arg in
                        self.implementation.container.arguments or []
                    ],
                    env={
                        name: _transform_arg(value) for name, value in
                        self.implementation.container.env or {}
                    },
                )),
        )

    @classmethod
    def load_from_component_yaml(cls, component_yaml: str) -> 'ComponentSpec':
        """Loads V1 or V2 component yaml into ComponentSpec.

        Args:
            component_yaml: the component yaml in string format.

        Returns:
            Component spec in the form of V2 ComponentSpec.
        """

        json_component = yaml.safe_load(component_yaml)
        try:
            return ComponentSpec.parse_obj(json_component)
        except:
            v1_component = _components._load_component_spec_from_component_text(
                component_yaml)
            return cls.from_v1_component_spec(v1_component)

    def save_to_component_yaml(self, output_file: str) -> None:
        """Saves ComponentSpec into yaml file.

        Args:
            output_file: File path to store the component yaml.
        """
        with open(output_file, 'a') as output_file:
            json_component = self.json(
                exclude_none=True, exclude_unset=True, by_alias=True)
            yaml_file = yaml.safe_dump(
                json.loads(json_component),
                default_flow_style=None,
                sort_keys=False)
            output_file.write(yaml_file)
