%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kvirc
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	3.4.0
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	Trinity based next generation IRC client with module support
Group:		Applications/Utilities
URL:		http://kvirc.net/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/internet/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4 make

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xft)
BuildRequires:  nas-devel

Requires:		%{name}-data = %{?epoch:%{epoch}:}%{version}-%{release}


%description
A highly configurable graphical IRC client with an MDI interface,
built-in scripting language, support for IRC DCC, drag & drop file
browsing, and much more. KVIrc uses the TDE widget set, can be extended
using its own scripting language, integrates with TDE, and supports
custom plugins.

If you are a developer and you want to write a custom module for KVIrc,
you need to install the kvirc-dev package.

%package data
Group:			Applications/Utilities
Summary:		Data files for KVIrc
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description data
This package contains the architecture-independent data needed by KVIrc in
order to run, such as icons and images, language files, and shell scripts.
It also contains complete reference guides on scripting and functions
within KVIrc in its internal help format. Unless you want to use KVIrc only
as a very simple IRC client you are likely to want to write scripts to
tailor KVIrc to your needs.

KVIrc is a graphical IRC client based on the TDE widget set which integrates
with the Trinity Desktop Environment version 3.

%package devel
Group:			Development/Libraries
Summary:		Development files for KVIrc
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package contains KVIrc libraries and include files you need if you
want to develop plugins for KVIrc.

KVIrc is a graphical IRC client based on the TDE widget set which integrates
with the K Desktop Environment version 3.


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/"*"/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
./autogen.sh


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_prefix}/bin \
  --datadir=%{tde_prefix}/share \
  --libdir=%{tde_prefix}/%{_lib} \
  --mandir=%{tde_prefix}/share/man \
  --includedir=%{tde_prefix}/include/tde \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-wall \
  \
  --with-pic \
  \
  --with-big-channels \
  --enable-perl \
  --with-ix86-asm \
  --with-kde-services-dir=%{tde_prefix}/share/services \
  --with-kde-library-dir=%{tde_prefix}/%{_lib} \
  --with-kde-include-dir=%{tde_prefix}/include/tde \
  --with-tqt-name=tqt \
  --with-tqt-library-dir=%{_libdir} \
  --with-tqt-include-dir=%{_includedir}/tqt3 \
  --with-tqt-moc=%{_bindir}/tmoc

# Symbolic links must exist prior to parallel building
%__make symlinks -C src/kvilib/build
%__make symlinks -C src/kvirc/build

%__sed -i "src/modules/"*"/Makefile" -e "s|-Wl,--no-undefined||"

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_prefix}/bin:${PATH}"
%__make install DESTDIR=%{buildroot}

# Debian maintainer has renamed 'COPYING' file to 'EULA', so we do the same ...
%__mv \
  %{?buildroot}%{tde_prefix}/share/kvirc/3.4/license/COPYING \
  %{?buildroot}%{tde_prefix}/share/kvirc/3.4/license/EULA

# Move desktop file to XDG location
%__mkdir_p "%{?buildroot}%{tde_prefix}/share/applications/tde"
%__mv -f "%{?buildroot}%{tde_prefix}/share/applnk/"*"/%{tde_pkg}.desktop" "%{?buildroot}%{tde_prefix}/share/applications/tde"


%files
%defattr(-,root,root,-)
%doc ChangeLog FAQ README TODO
%{tde_prefix}/bin/kvirc
%{tde_prefix}/%{_lib}/*.so.*
%{tde_prefix}/%{_lib}/kvirc/*/modules/*.so

%files data
%defattr(-,root,root,-)
%{tde_prefix}/bin/kvi_run_netscape
%{tde_prefix}/bin/kvi_search_help
%exclude %{tde_prefix}/%{_lib}/kvirc/*/modules/*.la
%exclude %{tde_prefix}/%{_lib}/kvirc/*/modules/*.so
%{tde_prefix}/%{_lib}/kvirc/
%{tde_prefix}/share/applications/tde/kvirc.desktop
%{tde_prefix}/share/apps/tdeconf_update/kvirc_soundsystem.upd
%{tde_prefix}/share/apps/tdeconf_update/kvirc_soundsystem_upd.sh
%{tde_prefix}/share/icons/hicolor/*/*/*.png
%{tde_prefix}/share/icons/hicolor/*/*/*.svgz
%{tde_prefix}/share/icons/hicolor/*/*/*.xpm
%{tde_prefix}/share/kvirc
%{tde_prefix}/share/mimelnk/text/*.desktop
%{tde_prefix}/share/services/*.protocol
%{tde_prefix}/share/man/man1/kvirc.1

%files devel
%defattr(-,root,root,-)
%{tde_prefix}/bin/kvirc-config
%{tde_prefix}/include/kvirc/
%{tde_prefix}/%{_lib}/*.la
%{tde_prefix}/%{_lib}/*.so
%{tde_prefix}/%{_lib}/kvirc/*/modules/*.la

