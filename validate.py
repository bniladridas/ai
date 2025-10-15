import json
import os


def repair_notebook(notebook_path):
    try:
        # Read the notebook
        with open(notebook_path) as f:
            notebook = json.load(f)

        # Flag to track if changes were made
        notebook_modified = False

        # Repair code cells
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "code":
                # Ensure outputs exist
                if "outputs" not in cell:
                    cell["outputs"] = []
                    notebook_modified = True

                # Reset execution count
                cell["execution_count"] = None

        # Write back if modified
        if notebook_modified:
            with open(notebook_path, "w") as f:
                json.dump(notebook, f, indent=2)
            print(f"Repaired notebook: {notebook_path}")
            return True

        return False

    except Exception as e:
        print(f"Error processing {notebook_path}: {e}")
        return False


# Find and repair notebooks
modified_notebooks = []
for root, _dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".ipynb"):
            notebook_path = os.path.join(root, file)
            if repair_notebook(notebook_path):
                modified_notebooks.append(notebook_path)

# If notebooks were modified, fail the workflow
if modified_notebooks:
    print("The following notebooks were modified:")
    for notebook in modified_notebooks:
        print(f"  - {notebook}")
    exit(1)
