import os, glob, shutil
import re

root_to_name_map = {
    "DLS": "Deep Learning Specialization",
    "MLS": "Machine Learning Specialization",
    "TF_Specialization": "TensorFlow Advanced Techniques Specialization",
    "GAN": "Generative Adversarial Networks Specialization",
    "DLAI": "Deep Learning AI",
}


all_ipynb_files = glob.glob("./**/*.ipynb", recursive=True)
all_ipynb_files = [f for f in all_ipynb_files if not f.startswith("./all_notebooks")]
all_ipynb_files = [f for f in all_ipynb_files if not f.startswith("./site")]
print(len(all_ipynb_files))

with open(".exclude", "r") as f:
    exclude_files = f.read().splitlines()

final_notebooks_to_copy = [f for f in all_ipynb_files if f not in exclude_files]
print(len(final_notebooks_to_copy))

new_base_dir = "./all_notebooks"
if not os.path.exists(new_base_dir):
    os.makedirs(new_base_dir)

for file in final_notebooks_to_copy:
    new_file = os.path.join(new_base_dir, file)
    new_dir = os.path.dirname(new_file)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
    if not os.path.exists(new_file) and "temp.ipynb" not in file:
        shutil.copyfile(file, new_file)


sep = " " * 4
root_node = "DLS"
root_to_name_map = {
    "DLS": "Deep Learning Specialization",
    "MLS": "Machine Learning Specialization",
    "TF_Specialization": "TensorFlow Advanced Techniques Specialization",
    "GAN": "Generative Adversarial Networks Specialization",
    "DLAI": "Deep Learning AI",
}


def get_node_and_final_path(root_node, notebook_dir, max_nodes=1, skip_nodes=3):
    """Get the node name and final path for a notebook"""
    all_nodes = notebook_dir.split(os.path.sep)
    final_notebooks_path = os.path.sep.join(all_nodes[skip_nodes:])
    final_notebooks_path = os.path.join(root_node, final_notebooks_path)
    nodes = all_nodes[skip_nodes : skip_nodes + max_nodes]
    nodes = "/".join(nodes)
    return nodes, final_notebooks_path


def create_node_yaml(nodes):
    """Create the yaml text for a node"""
    nodes = nodes.split("/")
    yaml_text = ""
    for i, node in enumerate(nodes):
        yaml_text += sep * (i + 1) + "- " + node + ":\n"
    return yaml_text


def one_root(root_node, max_nodes=1, skip_nodes=3):
    all_notebooks_second = glob.glob(
        f"./all_notebooks/{root_node}/**/*.ipynb", recursive=True
    )
    all_nodes = []
    all_file_paths = []

    for file in all_notebooks_second:
        res = get_node_and_final_path(root_node, file, max_nodes, skip_nodes)
        all_nodes.append(res[0])
        all_file_paths.append(res[1])
    unique_nodes = list(set(all_nodes))
    unique_nodes = sorted(unique_nodes)
    unique_yamls = [create_node_yaml(n) for n in unique_nodes]
    node_yaml_mapping = {k: v for k, v in zip(unique_nodes, unique_yamls)}

    for i, (file, node) in enumerate(zip(all_file_paths, all_nodes)):
        depth = len(node.split("/")) + 1
        node_yaml_mapping[node] += sep * depth + "- " + file + "\n"

    final_text = f"- {root_to_name_map[root_node]}:\n"
    # sort node_yaml_mapping via value
    for val in node_yaml_mapping.values():
        final_text += val + "\n"
    return final_text


all_root_nodes = ["DLS", "MLS", "TF_Specialization", "GAN", "DLAI"]

final_text = ""
for root_node in all_root_nodes:
    final_text += one_root(root_node) + "\n"

with open(".yml_out", "w") as f:
    for line in final_text.split("\n"):
        f.write("  " + line + "\n")
