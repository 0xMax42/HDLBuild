# HDLBuild

HDLBuild is a flexible build management tool for FPGA projects. It simplifies the process of managing dependencies, building, testing, and deploying FPGA designs using Xilinx ISE tools.

## Features

- **Dependency Management**: Automatically resolves and manages project dependencies from Git repositories.
- **Build Automation**: Supports synthesis, implementation, and bitstream generation for FPGA designs.
- **Testbench Execution**: Automates the process of building and running testbenches.
- **Customizable Tool Options**: Provides extensive configuration options for Xilinx ISE tools.
- **Project Initialization**: Quickly set up new projects with predefined templates.
- **Rich Console Output**: Provides detailed and interactive console feedback using `rich`.

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)
- Xilinx ISE (14.7) installed and configured

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/hdlbuild.git
   cd hdlbuild
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Add the `hdlbuild` CLI to your PATH:
   ```bash
   poetry shell
   ```

---

## Installation per pip

To install HDLBuild via pip, run:
```bash
pip install --index-url https://git.0xmax42.io/api/packages/maxp/pypi/simple/ --extra-index-url https://pypi.org/ hdlbuild
```

---

## Usage

### CLI Commands

HDLBuild provides a command-line interface (CLI) for managing FPGA projects. Below are the available commands:

#### 1. **Initialize a New Project**
   ```bash
   hdlbuild init
   ```
   - Creates a new project with a project.yml configuration file and a .gitignore file.

#### 2. **Resolve Dependencies**
   ```bash
   hdlbuild dep
   ```
   - Clones and resolves all project dependencies defined in project.yml.

#### 3. **Build the Project**
   ```bash
   hdlbuild build
   ```
   - Runs the full build process, including synthesis, implementation, and bitstream generation.

   - To only synthesize the design:
     ```bash
     hdlbuild build synth
     ```

#### 4. **Run Testbenches**
   ```bash
   hdlbuild test <testbench_name>
   ```
   - Builds and runs the specified testbench.

#### 5. **Clean Build Artifacts**
   ```bash
   hdlbuild clean
   ```
   - Removes build artifacts.

   - To clean all generated files:
     ```bash
     hdlbuild clean all
     ```

---

## Configuration

The project is configured using a project.yml file. Below is an example configuration:

```yml
name: MyFPGAProject
topmodule: top_module
target_device: xc3s1200e-4-fg320
xilinx_path: /opt/Xilinx/14.7/ISE_DS/ISE

constraints: constraints.ucf

sources:
  vhdl:
    - path: src/*.vhd
      library: work

testbenches:
  vhdl:
    - path: tests/*.vhd
      library: work

dependencies:
  - git: "https://github.com/example/dependency.git"
    rev: "main"

build:
  build_dir: working
  report_dir: reports
  copy_target_dir: output

tool_options:
  xst:
    - "-opt_mode Speed"
    - "-opt_level 2"
  map:
    - "-detail"
    - "-timing"
  par: []
  bitgen:
    - "-g StartupClk:JtagClk"
```

---

## Development

### Building the Package

To build the Python package:
```bash
poetry build
```

---

## GitHub Actions

The project includes GitHub workflows for building and deploying the package:

1. **Build and Publish**: build-and-deploy.yml

---

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for details.