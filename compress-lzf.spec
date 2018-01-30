%{?_javapackages_macros:%_javapackages_macros}

Name:          compress-lzf
Version:       1.0.3
Release:       7.1
Summary:       Basic LZF codec, compatible with standard C LZF package
Group:         Development/Java
License:       ASL 2.0
URL:           https://github.com/ning/compress
Source0:       https://github.com/ning/compress/archive/%{name}-%{version}.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires: mvn(org.apache.maven.plugins:maven-enforcer-plugin)
BuildRequires: mvn(org.apache.maven.surefire:surefire-testng)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)
BuildRequires: mvn(org.testng:testng)

BuildArch:     noarch

%description
Compression codec for LZF encoding for particularly encoding/decoding,
with reasonable compression. Compressor is basic Lempel-Ziv codec,
without Huffman (deflate/gzip) or statistical post-encoding. See
"http://oldhome.schmorp.de/marc/liblzf.html" for more on
original LZF package.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n compress-%{name}-%{version}

find . -name "*.class" -print -delete
find . -name "*.jar" -type f -print -delete

%pom_remove_plugin :maven-source-plugin
%pom_xpath_remove "pom:project/pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"

%pom_add_dep junit:junit::test

%mvn_file : %{name}

%build

%mvn_build -- -Poffline-testing

%install
%mvn_install

%files -f .mfiles
%doc README.md VERSION.txt
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 21 2016 gil cattaneo <puntogil@libero.it> 1.0.3-5
- add missing build requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 30 2015 gil cattaneo <puntogil@libero.it> 1.0.3-2
- introduce license macro

* Mon Nov 03 2014 gil cattaneo <puntogil@libero.it> 1.0.3-1
- update to 1.0.3

* Wed Jul 02 2014 gil cattaneo <puntogil@libero.it> 0.9.8-3
- fix SUID issue in LZF compression rhbz#1115264

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 14 2013 gil cattaneo <puntogil@libero.it> 0.9.8-1
- initial rpm
