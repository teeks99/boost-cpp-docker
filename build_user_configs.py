from string import Template
import os

clang_mandatory =  "-Wno-c99-extensions"
expand = {
  "O2": "-O2",
  "warn": "-Wall -Wextra"
}
types = ["c++", "gnu++"]
extras = ["O2", "warn"]
libcxx = {
    "manual": {
        "compile": "-stdlib=libc++ -isystem/usr/include/libcxxabi",
        "link": "-stdlib=libc++ -lc++abi"
    }
}

convert_dir = {"clang-4.0": "clang-4", "clang-5.0": "clang-5", "clang-6.0": "clang-6"}
compiler_cmd = {"clang":"clang++", "gcc":"g++"}

compilers = {
    "clang-2.9":{"distro": "trusty", "configs": ["98", "11"]},
    "clang-3.0":{"distro": "trusty", "configs": ["98", "11"]},
    "clang-3.1":{"distro": "trusty", "configs": ["98", "11"]},
    "clang-3.2":{"distro": "trusty", "configs": ["98", "11", "1y"]},
    "clang-3.3":{"distro": "trusty", "configs": ["98", "11", "1y"]},
    "clang-3.4":{"distro": "trusty", "configs": ["98", "11", "14", "1z"]},
    "clang-3.5":{"distro": "trusty", "configs": ["98", "11", "14", "1z"]},
    "clang-3.6":{"distro": "trusty", "configs": ["98", "11", "14", "1z"]},
    "clang-3.7":{"distro": "trusty", "configs": ["98", "11", "14", "1z"]},
    "clang-3.8":{"distro": "trusty", "configs": ["98", "11", "14", "1z"]},
    "clang-3.9":{"distro": "xenial", "configs": ["98", "11", "14", "1z"], "libcxx":"manual"},
    "clang-4.0":{"distro": "xenial", "configs": ["98", "11", "14", "1z"], "libcxx":"manual"},
    "clang-5.0":{"distro": "xenial", "configs": ["98", "11", "14", "1z"], "libcxx":"manual"},
    "clang-6.0":{"distro": "xenial", "configs": ["98", "11", "14", "17"], "libcxx":"manual"},
    "clang-7":{"distro": "bionic", "configs": ["98", "11", "14", "17", "2a"], "libcxx":"manual"},
    "clang-8":{"distro": "bionic", "configs": ["98", "11", "14", "17", "2a"], "libcxx":"manual"},
    "gcc-4.4":{"distro": "precise", "configs": ["98", "0x"]},
    "gcc-4.5":{"distro": "precise", "configs": ["98", "0x"]},
    "gcc-4.6":{"distro": "precise", "configs": ["98", "0x"]},
    "gcc-4.7":{"distro": "precise", "configs": ["98", "11", "1y"]},
    "gcc-4.8":{"distro": "trusty", "configs": ["98", "11", "1y"]},
    "gcc-4.9":{"distro": "trusty", "configs": ["98", "11", "1y"]},
    "gcc-5":{"distro": "trusty", "configs": ["98", "11", "14", "1z"]},
    "gcc-6":{"distro": "trusty", "configs": ["98", "11", "14", "1z"]},
    "gcc-7":{"distro": "xenial", "configs": ["98", "11", "14", "1z"]},
    "gcc-8":{"distro": "xenial", "configs": ["98", "11", "14", "17", "2a"]}
}

def make_toolset(compiler, version, config, cfgtype, extra=None, libcxx_cfg=None):
    conf = cfgtype + config
    short_conf = conf
    if cfgtype == "gnu++":
        short_conf = "gnu" + config

    ver = version + "~" + short_conf
    if libcxx_cfg:
        ver += "~lc"
    if extra:
        ver += "~" + extra

    t = "using {compiler} : {ver} : {cmd}-{version} : ".format(
        compiler=compiler, ver=ver, version=version, cmd=compiler_cmd[compiler])
    t += '<cxxflags>"'
    if compiler == "clang":
        t += clang_mandatory + " "
    t += "-std=" + conf + " "
    if extra:
        t += expand[extra] + " "
    if libcxx_cfg:
        t += libcxx[libcxx_cfg]["compile"] + " "
    t = t[:-1]
    t += '" '
    if libcxx_cfg:
        t += '<linkflags>"'
        t += libcxx[libcxx_cfg]["link"]
        t += '" '
    t += ";\n"
    return t

def build_configs():
    for compiler, options in compilers.items():
        cdir = compiler
        if compiler in convert_dir:
            cdir = convert_dir[compiler]

        compiler_type, version = compiler.split("-")

        toolsets = "using {compiler} : {version} : {cmd}-{version} : ".format(
            compiler=compiler_type, version=version, cmd=compiler_cmd[compiler_type])
        if compiler_type == "clang":
            toolsets += '<cxxflags>"-Wno-c99-extensions" '
        toolsets += ";\n"

        for config in options["configs"]:
            for cfgtype in types:
                toolsets += make_toolset(compiler_type, version, config, cfgtype)
                for extra in extras:
                    toolsets += make_toolset(compiler_type, version, config, cfgtype, extra)

                if "libcxx" in options:
                    toolsets += make_toolset(compiler_type, version, config, cfgtype, libcxx_cfg=options["libcxx"])
                    for extra in extras:
                        toolsets += make_toolset(
                            compiler_type, version, config, cfgtype, extra, libcxx_cfg=options["libcxx"])

        template_file = "user-config.jam.{distro}.template".format(distro=options["distro"])
        with open(template_file, "r") as f:
            ts = f.read()

        t = Template(ts)
        cfg = t.safe_substitute(toolsets=toolsets)

        with open(os.path.join(cdir, "user-config.jam"), "w") as f:
            f.write(cfg)


if __name__ == "__main__":
    build_configs()
