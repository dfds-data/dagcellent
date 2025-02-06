"""
This type stub file was generated by pyright.
"""

import datetime
from typing import TYPE_CHECKING

from kubernetes.client import models as k8s

"""
Pod generator compatible with cncf-providers released before 2.7.0 of airflow.

Compatible with pre-7.4.0 of the cncf.kubernetes provider.

This module provides an interface between the previous Pod
API and outputs a kubernetes.client.models.V1Pod.
The advantage being that the full Kubernetes API
is supported and no serialization need be written.
"""
if TYPE_CHECKING: ...
log = ...
MAX_LABEL_LEN = ...
alphanum_lower = ...

def rand_str(num):  # -> str:
    """
    Generate random lowercase alphanumeric string of length num.

    :meta private:
    """
    ...

def add_pod_suffix(pod_name: str, rand_len: int = ..., max_len: int = ...) -> str:
    """
    Add random string to pod name while staying under max length.

    :param pod_name: name of the pod
    :param rand_len: length of the random string to append
    :max_len: maximum length of the pod name
    :meta private:
    """
    ...

def make_safe_label_value(string: str) -> str:
    """
    Normalize a provided label to be of valid length and characters.

    Valid label values must be 63 characters or less and must be empty or begin and
    end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_),
    dots (.), and alphanumerics between.

    If the label value is greater than 63 chars once made safe, or differs in any
    way from the original value sent to this function, then we need to truncate to
    53 chars, and append it with a unique hash.
    """
    ...

def datetime_to_label_safe_datestring(datetime_obj: datetime.datetime) -> str:
    """
    Transform a datetime string to use as a label.

    Kubernetes doesn't like ":" in labels, since ISO datetime format uses ":" but
    not "_" let's
    replace ":" with "_"

    :param datetime_obj: datetime.datetime object
    :return: ISO-like string representing the datetime
    """
    ...

def label_safe_datestring_to_datetime(string: str) -> datetime.datetime:
    """
    Transform a label back to a datetime object.

    Kubernetes doesn't permit ":" in labels. ISO datetime format uses ":" but not
    "_", let's
    replace ":" with "_"

    :param string: str
    :return: datetime.datetime object
    """
    ...

class PodGenerator:
    """
    Contains Kubernetes Airflow Worker configuration logic.

    Represents a kubernetes pod and manages execution of a single pod.
    Any configuration that is container specific gets applied to
    the first container in the list of containers.

    :param pod: The fully specified pod. Mutually exclusive with `pod_template_file`
    :param pod_template_file: Path to YAML file. Mutually exclusive with `pod`
    :param extract_xcom: Whether to bring up a container for xcom
    """

    def __init__(
        self,
        pod: k8s.V1Pod | None = ...,
        pod_template_file: str | None = ...,
        extract_xcom: bool = ...,
    ) -> None: ...
    def gen_pod(self) -> k8s.V1Pod:
        """Generate pod."""
        ...

    @staticmethod
    def add_xcom_sidecar(pod: k8s.V1Pod) -> k8s.V1Pod:
        """Add sidecar."""
        ...

    @staticmethod
    def from_obj(obj) -> dict | k8s.V1Pod | None:
        """Convert to pod from obj."""
        ...

    @staticmethod
    def from_legacy_obj(obj) -> k8s.V1Pod | None:
        """Convert to pod from obj."""
        ...

    @staticmethod
    def reconcile_pods(base_pod: k8s.V1Pod, client_pod: k8s.V1Pod | None) -> k8s.V1Pod:
        """
        Merge Kubernetes Pod objects.

        :param base_pod: has the base attributes which are overwritten if they exist
            in the client pod and remain if they do not exist in the client_pod
        :param client_pod: the pod that the client wants to create.
        :return: the merged pods

        This can't be done recursively as certain fields are overwritten and some are concatenated.
        """
        ...

    @staticmethod
    def reconcile_metadata(base_meta, client_meta):  # -> dict[Any, Any] | None:
        """
        Merge Kubernetes Metadata objects.

        :param base_meta: has the base attributes which are overwritten if they exist
            in the client_meta and remain if they do not exist in the client_meta
        :param client_meta: the spec that the client wants to create.
        :return: the merged specs
        """
        ...

    @staticmethod
    def reconcile_specs(
        base_spec: k8s.V1PodSpec | None, client_spec: k8s.V1PodSpec | None
    ) -> k8s.V1PodSpec | None:
        """
        Merge Kubernetes PodSpec objects.

        :param base_spec: has the base attributes which are overwritten if they exist
            in the client_spec and remain if they do not exist in the client_spec
        :param client_spec: the spec that the client wants to create.
        :return: the merged specs
        """
        ...

    @staticmethod
    def reconcile_containers(
        base_containers: list[k8s.V1Container], client_containers: list[k8s.V1Container]
    ) -> list[k8s.V1Container]:
        """
        Merge Kubernetes Container objects.

        :param base_containers: has the base attributes which are overwritten if they exist
            in the client_containers and remain if they do not exist in the client_containers
        :param client_containers: the containers that the client wants to create.
        :return: the merged containers

        The runs recursively over the list of containers.
        """
        ...

    @classmethod
    def construct_pod(
        cls,
        dag_id: str,
        task_id: str,
        pod_id: str,
        try_number: int,
        kube_image: str,
        date: datetime.datetime | None,
        args: list[str],
        pod_override_object: k8s.V1Pod | None,
        base_worker_pod: k8s.V1Pod,
        namespace: str,
        scheduler_job_id: str,
        run_id: str | None = ...,
        map_index: int = ...,
        *,
        with_mutation_hook: bool = ...,
    ) -> k8s.V1Pod:
        """
        Create a Pod.

        Construct a pod by gathering and consolidating the configuration from 3 places:
            - airflow.cfg
            - executor_config
            - dynamic arguments
        """
        ...

    @classmethod
    def build_selector_for_k8s_executor_pod(
        cls,
        *,
        dag_id,
        task_id,
        try_number,
        map_index=...,
        execution_date=...,
        run_id=...,
        airflow_worker=...,
    ):  # -> str:
        """
        Generate selector for kubernetes executor pod.

        :meta private:
        """
        ...

    @classmethod
    def build_labels_for_k8s_executor_pod(
        cls,
        *,
        dag_id,
        task_id,
        try_number,
        airflow_worker=...,
        map_index=...,
        execution_date=...,
        run_id=...,
    ):  # -> dict[str, str]:
        """
        Generate labels for kubernetes executor pod.

        :meta private:
        """
        ...

    @staticmethod
    def serialize_pod(pod: k8s.V1Pod) -> dict:
        """
        Convert a k8s.V1Pod into a json serializable dictionary.

        :param pod: k8s.V1Pod object
        :return: Serialized version of the pod returned as dict
        """
        ...

    @staticmethod
    def deserialize_model_file(path: str) -> k8s.V1Pod:
        """
        Generate a Pod from a file.

        :param path: Path to the file
        :return: a kubernetes.client.models.V1Pod
        """
        ...

    @staticmethod
    def deserialize_model_dict(pod_dict: dict | None) -> k8s.V1Pod:
        """
        Deserializes a Python dictionary to k8s.V1Pod.

        Unfortunately we need access to the private method
        ``_ApiClient__deserialize_model`` from the kubernetes client.
        This issue is tracked here; https://github.com/kubernetes-client/python/issues/977.

        :param pod_dict: Serialized dict of k8s.V1Pod object
        :return: De-serialized k8s.V1Pod
        """
        ...

    @staticmethod
    def make_unique_pod_id(pod_id: str) -> str | None:
        r"""
        Generate a unique Pod name.

        Kubernetes pod names must consist of one or more lowercase
        rfc1035/rfc1123 labels separated by '.' with a maximum length of 253
        characters.

        Name must pass the following regex for validation
        ``^[a-z0-9]([-a-z0-9]*[a-z0-9])?(\\.[a-z0-9]([-a-z0-9]*[a-z0-9])?)*$``

        For more details, see:
        https://github.com/kubernetes/kubernetes/blob/release-1.1/docs/design/identifiers.md

        :param pod_id: requested pod name
        :return: ``str`` valid Pod name of appropriate length
        """
        ...

def merge_objects(base_obj, client_obj):  # -> dict[Any, Any]:
    """
    Merge objects.

    :param base_obj: has the base attributes which are overwritten if they exist
        in the client_obj and remain if they do not exist in the client_obj
    :param client_obj: the object that the client wants to create.
    :return: the merged objects
    """
    ...

def extend_object_field(base_obj, client_obj, field_name):
    """
    Add field values to existing objects.

    :param base_obj: an object which has a property `field_name` that is a list
    :param client_obj: an object which has a property `field_name` that is a list.
        A copy of this object is returned with `field_name` modified
    :param field_name: the name of the list field
    :return: the client_obj with the property `field_name` being the two properties appended
    """
    ...
