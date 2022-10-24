%global commit cb33e0d27892b885b0d86b5f99af2b71f660de56
%global shortcommit %(c=%{commit}; echo ${c:0:7})

#global gitdate 20210201
%global pkgname %{?gitdate:xserver}%{!?gitdate:xwayland}

%global default_font_path "catalogue:/etc/X11/fontpath.d,built-ins"

Summary:   Xwayland
Name:      xorg-x11-server-Xwayland
Version:   22.1.3
Release:   2%{?gitdate:.%{gitdate}git%{shortcommit}}%{?dist}

URL:       http://www.x.org
%if 0%{?gitdate}
Source0:   https://gitlab.freedesktop.org/xorg/%{pkgname}/-/archive/%{commit}/%{pkgname}-%{shortcommit}.tar.gz
%else
Source0:   https://www.x.org/pub/individual/xserver/%{pkgname}-%{version}.tar.xz
%endif
#Patch0:         0001-xwayland-patch-fix-vsync.patch

License:   MIT

Requires: xorg-x11-server-common
Requires: libEGL
Requires: libepoxy >= 1.5.5

BuildRequires: gcc
BuildRequires: git-core
BuildRequires: meson

BuildRequires: wayland-devel
BuildRequires: pkgconfig(wayland-client) >= 1.3.0
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(wayland-eglstream-protocols)

BuildRequires: pkgconfig(epoxy) >= 1.5.5
BuildRequires: pkgconfig(fontenc)
BuildRequires: pkgconfig(libdrm) >= 2.4.0
BuildRequires: pkgconfig(libssl)
BuildRequires: pkgconfig(libtirpc)
BuildRequires: pkgconfig(pixman-1)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xau)
BuildRequires: pkgconfig(xdmcp)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xfont2)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xinerama)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xmu)
BuildRequires: pkgconfig(xorg-macros) >= 1.17
BuildRequires: pkgconfig(xpm)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xres)
BuildRequires: pkgconfig(xshmfence) >= 1.1
BuildRequires: pkgconfig(xtrans) >= 1.3.2
BuildRequires: pkgconfig(xtst)
BuildRequires: pkgconfig(xv)
BuildRequires: pkgconfig(libxcvt)
BuildRequires: xorg-x11-proto-devel >= 7.7-10

BuildRequires: mesa-libGL-devel >= 9.2
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libgbm-devel

BuildRequires: audit-libs-devel
BuildRequires: libselinux-devel >= 2.0.86-1

# libunwind is Exclusive for the following arches
%ifarch aarch64 %{arm} hppa ia64 mips ppc ppc64 %{ix86} x86_64
%if !0%{?rhel}
BuildRequires: libunwind-devel
%endif
%endif

BuildRequires: pkgconfig(xcb-aux)
BuildRequires: pkgconfig(xcb-image)
BuildRequires: pkgconfig(xcb-icccm)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-renderutil)

%description
Xwayland is an X server for running X clients under Wayland.

%package devel
Summary: Development package
Requires: pkgconfig

%description devel
The development package provides the developmental files which are
necessary for developing Wayland compositors using Xwayland.

%prep
%autosetup -S git_am -n %{pkgname}-%{?gitdate:%{commit}}%{!?gitdate:%{version}}

%build
%meson \
        -Dxwayland_eglstream=true \
        -Ddefault_font_path=%{default_font_path} \
        -Dbuilder_string="Build ID: %{name} %{version}-%{release}" \
        -Dxkb_output_dir=%{_localstatedir}/lib/xkb \
        -Dxcsecurity=true \
        -Dglamor=true \
        -Ddri3=true

%meson_build

%install
%meson_install

# Remove unwanted files/dirs
rm $RPM_BUILD_ROOT%{_mandir}/man1/Xserver.1*
rm -Rf $RPM_BUILD_ROOT%{_libdir}/xorg
rm -Rf $RPM_BUILD_ROOT%{_includedir}/xorg
rm -Rf $RPM_BUILD_ROOT%{_datadir}/aclocal
rm -Rf $RPM_BUILD_ROOT%{_localstatedir}/lib/xkb

%files
%{_bindir}/Xwayland
%{_mandir}/man1/Xwayland.1*

%files devel
%{_libdir}/pkgconfig/xwayland.pc

%changelog
* Tue Jul 12 2022 Olivier Fourdan <ofourdan@redhat.com> - 22.1.3-1
- xwayland 22.1.3 - (#2106387)
  Fix CVE-2022-2319/ZDI-CAN-16062, CVE-2022-2320/ZDI-CAN-16070

* Wed May 25 2022 Olivier Fourdan <ofourdan@redhat.com> - 22.1.2-1
- xwayland 22.1.2 - (#2090172)

* Thu Mar 31 2022 Olivier Fourdan <ofourdan@redhat.com> - 22.1.1-1
- xwayland 22.1.1 - (#2070435)

* Wed Feb 16 2022 Olivier Fourdan <ofourdan@redhat.com> - 22.1.0
- xwayland 22.1.0 - (#2055270)

* Wed Feb  2 2022 Olivier Fourdan <ofourdan@redhat.com> - 22.0.99.902
- xwayland 22.0.99.902 (xwayland 22.1.0 rc2) - (#2042521)

* Tue Jan 25 2022 Olivier Fourdan <ofourdan@redhat.com> - 22.0.99.901
- xwayland 22.0.99.901 (xwayland 22.1.0 rc1) - (#2042521)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.4
- xwayland 21.1.4

* Mon Nov  8 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.3
- xwayland 21.1.3 - (#2016468)

* Thu Oct 21 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.2.901-1
- xwayland 21.1.2.901 (aka 21.1.3 RC1) - (#2015413)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 21.1.2-3
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 9 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.2-1
- xwayland 21.1.2

* Thu Jul 1 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.1.901-1
- xwayland 21.1.1.901

* Mon Jun 21 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.1-3
- Fix a use-after-free in the previous changes for GLX

* Thu Jun 10 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.1-2
- Backport fixes for GLX and EGLstream (#1948003)

* Wed Apr  14 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.1-1
- xwayland 21.1.1 (CVE-2021-3472 / ZDI-CAN-1259)

* Thu Mar  18 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.1.0-1
- xwayland 21.1.0

* Thu Mar  4 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.0.99.902-1
- xwayland 21.0.99.902
- Remove xdmcp, udev, udev_kms build options
- Stop overriding the vendor name, same as xorg-x11-server

* Thu Feb 18 2021 Olivier Fourdan <ofourdan@redhat.com> - 21.0.99.901-1
- xwayland 21.0.99.901

* Mon Feb  1 2021 Olivier Fourdan <ofourdan@redhat.com> - 1.20.99.1-0.1.20210201git5429791
- Initial import (#1912335).
