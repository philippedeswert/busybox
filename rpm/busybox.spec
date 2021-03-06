Summary: Single binary providing simplified versions of system commands
Name: busybox
Version: 1.21.0
Release: 1
License: GPLv2
Group: System/Shells
Source: http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1: rpm/udhcpd.service
URL: https://github.com/mer-packages/busybox 

%define debug_package %{nil}

%package docs
Group: Documentation
Summary: Busybox Documentation

%description
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries.

%package symlinks-gzip
Requires: %{name}
Group: System/Shells
Summary: Busybox replacements for gzip
Provides: gzip = %{version}
Obsoletes: gzip <= 1.5

%description symlinks-gzip
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This
is the symlinks implementing gzip replacements.

%package symlinks-dhcp
Requires: %{name}
Group: System/Shells
Summary: Busybox dhcp utilities

%description symlinks-dhcp
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This contains
the symlinks implementing the dhcp utilities (udhcpc/udhcpcd).

%description docs
Busybox documentation and user guides

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
cp busybox-sailfish.config .config
yes "" | make oldconfig
make %{_smp_mflags}
make busybox.links
cat >> busybox.links << EOF
/usr/bin/gzip
/usr/bin/gunzip
/usr/sbin/udhcpc
EOF

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/bin
install -m 755 busybox %{buildroot}/bin/busybox
install -m 644 -D %{SOURCE1} %{buildroot}/lib/systemd/system/udhcpd.service
applets/install.sh %{buildroot} --symlinks
rm -f %{buildroot}/sbin/udhcpc

%files
%defattr(-,root,root,-)
%doc LICENSE
/bin/busybox

%files docs
%defattr(-,root,root,-)
%doc LICENSE docs/busybox.net/*.html

%files symlinks-gzip
%defattr(-,root,root,-)
/bin/gunzip
/usr/bin/gunzip
/bin/gzip
/usr/bin/gzip
/bin/zcat

%files symlinks-dhcp
%defattr(-,root,root,-)
/usr/sbin/udhcpc
/usr/sbin/udhcpd
/lib/systemd/system/udhcpd.service
