from utils.directory_manager import clear_directories, ensure_directories_exist
from utils.project_loader import load_project_config
from utils.source_resolver import expand_sources

project = load_project_config()

print(project.name)
print(project.sources.vhdl)

ensure_directories_exist()

clear_directories()

expanded_vhdl = expand_sources(project.sources.vhdl)

for library, filepath in expanded_vhdl:
    print(f"vhdl {library} \"{filepath}\"")
