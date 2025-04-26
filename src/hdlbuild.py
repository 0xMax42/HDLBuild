from models.config import DIRECTORIES
from tools.xilinx_ise.bitgen import copy_bitstream_file, run_bitgen
from tools.xilinx_ise.map import copy_map_report, run_map
from tools.xilinx_ise.ngdbuild import run_ngdbuild
from tools.xilinx_ise.par import copy_par_report, copy_pinout_report, run_par
from tools.xilinx_ise.xst import copy_synthesis_report, generate_xst_project_file, generate_xst_script_file, run_xst
from utils.directory_manager import clear_directories, ensure_directories_exist
from utils.project_loader import load_project_config
from utils.source_resolver import expand_sources

project = load_project_config()

print(project.name)
print(project.sources.vhdl)

clear_directories()

ensure_directories_exist()



expanded_vhdl = expand_sources(project.sources.vhdl)

for library, filepath in expanded_vhdl:
    print(f"vhdl {library} \"{filepath}\"")

generate_xst_project_file(project, f"{DIRECTORIES.build}/{project.name}.prj")
generate_xst_script_file(project, f"{DIRECTORIES.build}/{project.name}.scr")
print(f"XST project file generated at {DIRECTORIES.build}/{project.name}.prj")
print(f"XST script file generated at {DIRECTORIES.build}/{project.name}.scr")

run_xst(project)

copy_synthesis_report(project)

run_ngdbuild(project)

run_map(project)
copy_map_report(project)

run_par(project)
copy_par_report(project)
copy_pinout_report(project)

run_bitgen(project)
copy_bitstream_file(project)