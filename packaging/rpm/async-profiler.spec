%global profiler_version %{?version}%{!?version:4.3}

Name:           async-profiler
Version:        %{profiler_version}
Release:        1%{?dist}
Summary:        Sampling CPU and HEAP profiler for Java
License:        Apache-2.0
URL:            https://github.com/async-profiler/async-profiler
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  java-1.8.0-devel
BuildRequires:  patchelf
BuildRequires:  binutils

Requires:       java-headless >= 1:1.8.0

%description
async-profiler is a low overhead sampling profiler for Java that does not
suffer from the safepoint bias problem. It features HotSpot-specific APIs
to collect stack traces and to track memory allocations. The profiler works
with OpenJDK, Oracle JDK, and other Java runtimes based on the HotSpot JVM.

Supported profiling modes include CPU, wall-clock, allocation, and lock
profiling, with output in flame graph, JFR, and other formats.

%package debug
Summary:        Debug symbols for async-profiler
Requires:       %{name} = %{version}-%{release}

%description debug
Debug symbols for the async-profiler shared library.

%prep
%setup -q -n %{name}-%{version}

%build
make all JAVA_HOME="$(dirname $(dirname $(readlink -f $(which javac))))"

%install
rm -rf %{buildroot}

# Binaries
install -d %{buildroot}%{_bindir}
install -m 0755 build/bin/asprof %{buildroot}%{_bindir}/asprof
install -m 0755 build/bin/jfrconv %{buildroot}%{_bindir}/jfrconv

# Shared library
install -d %{buildroot}%{_libdir}/%{name}
install -m 0644 build/lib/libasyncProfiler.so %{buildroot}%{_libdir}/%{name}/libasyncProfiler.so

# Strip debug info into separate file
%{__strip} --only-keep-debug %{buildroot}%{_libdir}/%{name}/libasyncProfiler.so -o %{buildroot}%{_libdir}/%{name}/libasyncProfiler.so.debug
%{__strip} -g %{buildroot}%{_libdir}/%{name}/libasyncProfiler.so
%{__objcopy} --add-gnu-debuglink=%{buildroot}%{_libdir}/%{name}/libasyncProfiler.so.debug %{buildroot}%{_libdir}/%{name}/libasyncProfiler.so

# Header
install -d %{buildroot}%{_includedir}
install -m 0644 build/include/asprof.h %{buildroot}%{_includedir}/asprof.h

# JARs
install -d %{buildroot}%{_datadir}/%{name}
install -m 0644 build/jar/async-profiler.jar %{buildroot}%{_datadir}/%{name}/async-profiler.jar
install -m 0644 build/jar/jfr-converter.jar %{buildroot}%{_datadir}/%{name}/jfr-converter.jar

# Documentation
install -d %{buildroot}%{_docdir}/%{name}
install -m 0644 LICENSE %{buildroot}%{_docdir}/%{name}/LICENSE
install -m 0644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -m 0644 CHANGELOG.md %{buildroot}%{_docdir}/%{name}/CHANGELOG.md

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/asprof
%{_bindir}/jfrconv
%{_libdir}/%{name}/libasyncProfiler.so
%{_includedir}/asprof.h
%{_datadir}/%{name}/async-profiler.jar
%{_datadir}/%{name}/jfr-converter.jar
%{_docdir}/%{name}/

%files debug
%{_libdir}/%{name}/libasyncProfiler.so.debug

%changelog