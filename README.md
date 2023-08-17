# Namespace
Namespace is a feature of Linux OS that allows processes to have isolated space where they can run independently and don't interfere with other processes. There are several types of namespaces in Linux, each focusing on isolating a specific set of resources. We are going to focus on creating network namespace using python.

# Network Namespace
It isolates network related resources such as network interfaces, routing tables etc.

we created two network namespaces.Then we assigned two virtul ethernet cables known as veth to each namespaces. Physical ethernet cables are used to connect different devices. Virtual ethernet just mimics that attribute. It helps each namespace to communicate with other namespaces.
