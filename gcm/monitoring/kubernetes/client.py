# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
from __future__ import annotations

from typing import Iterable, Protocol

from gcm.schemas.kubernetes.node import KubernetesNodeConditionRow
from gcm.schemas.kubernetes.pod import KubernetesPodRow


class KubernetesClient(Protocol):
    """A low-level Kubernetes client for pod and node monitoring."""

    def list_pods(
        self, namespace: str = "", label_selector: str = ""
    ) -> Iterable[KubernetesPodRow]:
        """Get pod information from the Kubernetes API.

        Args:
            namespace: Kubernetes namespace to filter pods. Empty string means all namespaces.
            label_selector: Kubernetes label selector to filter pods.

        If an error occurs during execution, RuntimeError should be raised.
        """

    def list_pod_nodes(
        self, namespace: str = "", label_selector: str = ""
    ) -> Iterable[tuple[str, str]]:
        """Get (pod name, node name) pairs for scheduled pods.

        A lightweight alternative to `list_pods` for callers that only need
        pod placement.

        Args:
            namespace: Kubernetes namespace to filter pods. Empty string means all namespaces.
            label_selector: Kubernetes label selector to filter pods.

        If an error occurs during execution, RuntimeError should be raised.
        """

    def list_node_conditions(self) -> Iterable[KubernetesNodeConditionRow]:
        """Get node condition information from the Kubernetes API.

        If an error occurs during execution, RuntimeError should be raised.
        """


def get_pod_node_mapping(
    client: KubernetesClient,
    namespace: str = "",
    label_selector: str = "",
) -> dict[str, str]:
    return dict(
        client.list_pod_nodes(
            namespace=namespace,
            label_selector=label_selector,
        )
    )
