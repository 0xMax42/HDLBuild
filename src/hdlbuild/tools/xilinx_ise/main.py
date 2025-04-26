from hdlbuild.models.config import DIRECTORIES
from hdlbuild.models.project import ProjectConfig
from hdlbuild.tools.xilinx_ise.bitgen import copy_bitstream_file, run_bitgen
from hdlbuild.tools.xilinx_ise.map import copy_map_report, run_map
from hdlbuild.tools.xilinx_ise.ngdbuild import run_ngdbuild
from hdlbuild.tools.xilinx_ise.par import copy_par_report, copy_pinout_report, run_par
from hdlbuild.tools.xilinx_ise.trace import copy_trace_report, run_trace
from hdlbuild.tools.xilinx_ise.xst import copy_synthesis_report, generate_xst_project_file, generate_xst_script_file, run_xst


def xilinx_ise_synth(project: ProjectConfig):
    generate_xst_project_file(project, f"{DIRECTORIES.build}/{project.name}.prj")
    generate_xst_script_file(project, f"{DIRECTORIES.build}/{project.name}.scr")
    run_xst(project)

    copy_synthesis_report(project)

def xilinx_ise_all(project: ProjectConfig):
    xilinx_ise_synth(project)

    run_ngdbuild(project)

    run_map(project)
    copy_map_report(project)

    run_par(project)
    copy_par_report(project)
    copy_pinout_report(project)

    run_bitgen(project)
    copy_bitstream_file(project)

    run_trace(project)
    copy_trace_report(project)