Name:		compress-lzf
Version:	1.2.1
Release:	1
Summary:	LZF compression codec
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/ning/compress
Source0:	https://github.com/ning/compress/archive/refs/tags/compress-lzf-%{version}.tar.gz#/compress-lzf-%{version}.tar.gz

BuildArch:	noarch
Obsoletes:	%{name}-javadoc < %{version}
BuildRequires:	mvn(com.fasterxml:oss-parent:pom::)
# oss-parent pins the compiler plugin to this ASM jar.
BuildRequires:	mvn(org.ow2.asm:asm)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name compress-lzf

%description
Compress-LZF is a Lempel-Ziv codec compatible with the C liblzf
package, without Huffman or statistical post-encoding. 1.2.1 rejects
malformed back references. 1.2.0 fixes the difference between the
big-endian and little-endian Unsafe encoders. The fast path uses
sun.misc.Unsafe. Tests are skipped. The OSGi bundle descriptor and
the Java module descriptor are left out.

%prep
%autosetup -n compress-compress-lzf-%{version}
# packaging bundle needs the Felix plugin, which is not packaged.
# The version of these plugins is only in oss-parent, so the rewrite
# keeps the child declarations. Moditect is on the keep list and would
# run during package. Test dependencies are JUnit 5 and Jazzer.
# .mvn holds a prebuilt Maven wrapper jar.
python - <<'PY'
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

def local(tag):
    return tag.rsplit("}", 1)[-1]

drop_plugins = {
    "central-publishing-maven-plugin",
    "maven-javadoc-plugin",
    "maven-release-plugin",
    "maven-bundle-plugin",
    "moditect-maven-plugin",
}

path = Path("pom.xml")
tree = ET.parse(path)
root = tree.getroot()
packaging = None
removed = []
removed_deps = 0
for parent in list(root.iter()):
    for child in list(parent):
        name = local(child.tag)
        if name == "packaging" and (child.text or "").strip() == "bundle":
            child.text = "jar"
            packaging = "jar"
        if name in {"dependencies", "dependencyManagement"} and local(parent.tag) == "project":
            parent.remove(child)
            removed_deps += 1
            continue
        if name != "plugin":
            continue
        artifact = ""
        for item in child:
            if local(item.tag) == "artifactId":
                artifact = (item.text or "").strip()
        if artifact in drop_plugins:
            parent.remove(child)
            removed.append(artifact)
if packaging != "jar" or sorted(removed) != sorted(drop_plugins) or removed_deps != 2:
    raise SystemExit(f"packaging={packaging} removed={removed} deps={removed_deps}")
# Keep source and target. Adding release hides sun.misc.Unsafe.
compiler = None
for parent in root.iter():
    for child in parent:
        if local(child.tag) != "plugin":
            continue
        artifact = ""
        for item in child:
            if local(item.tag) == "artifactId":
                artifact = (item.text or "").strip()
        if artifact == "maven-compiler-plugin":
            compiler = child
if compiler is None:
    raise SystemExit("compiler plugin missing")
source = target = None
for item in compiler.iter():
    if local(item.tag) == "source":
        source = (item.text or "").strip()
    if local(item.tag) == "target":
        target = (item.text or "").strip()
    if local(item.tag) == "release":
        raise SystemExit("compiler release was added")
if source != "1.8" or target != "1.8":
    raise SystemExit(f"compiler source={source} target={target}")
tree.write(path, encoding="UTF-8", xml_declaration=True)
wrapper = Path(".mvn")
if not (wrapper / "wrapper" / "maven-wrapper.jar").is_file():
    raise SystemExit("maven wrapper jar missing")
shutil.rmtree(wrapper)
PY

%files -f .mfiles
%doc LICENSE README.md VERSION.txt
