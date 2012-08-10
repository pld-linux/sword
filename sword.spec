# TODO:
# - Package icu-sword and add bcond for it here
#
# Conditional build:
#%bcond_with	icusword
%bcond_without	clucene
%bcond_without	curl
%bcond_without	icu
%bcond_without	utilities

%define debug_package 0

Summary:	The SWORD Project framework for manipulating Bible texts
Name:		sword
Version:	1.6.2
Release:	7
License:	GPL
Group:		Libraries
Source0:	http://www.crosswire.org/ftpmirror/pub/sword/source/v1.6/%{name}-%{version}.tar.gz
# Source0-md5:	a7dc4456e20e915fec46d774b690e305
Patch0:		%{name}-curl.patch
Patch1:		%{name}-gcc47.patch
Patch2:		%{name}-clucene2.patch
URL:		http://www.crosswire.org/sword
BuildRequires:	pakchois-devel
BuildRequires:	pkgconfig
BuildRequires:	sqlite3-devel
BuildRequires:	xulrunner-devel >= 1.9.2.3
%{?with_clucene:BuildRequires:	clucene-core-devel}
%{?with_clucene:Requires:	clucene-core}
%{?with_curl:BuildRequires:	curl-devel}
%{?with_curl:Requires:	curl}
%{?with_icu:BuildRequires:	icu}
%{?with_icu:BuildRequires:	libicu-devel}
%{?with_icu:Requires:	icu}
#%{?with_icusword:BuildRequires:	icu-sword}
#%{?with_icusword:Requires:	icu-sword}
Requires:	xulrunner >= 1.9.2.3
Requires:	zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SWORD Project creats cross-platform open-source tools that allow
programmers and Bible societies to write new Bible software more
quickly and easily. The SWORD Bible Framework allows easy manipulation
of Bible texts, commentaries, lexicons, dictionaries, etc. Many
frontends are built using this framework. An installed module set may
be shared between any frontend using the framework.

%package utilities
Summary:	Utility programs that use the sword libraries
Group:		Applications
Requires:	%{name} = %{version}-%{release}
Provides:	diatheke

%description utilities
Utility programs that use the sword libraries.

%package devel
Summary:	Include files and static libraries for developing sword applications
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel >= 7.10.5
Requires:	zlib-devel

%description devel
Include files and static libraries for developing sword applications.
This package is required to compile Sword frontends, too.

%prep
%setup -q
%if %{with_curl}
%patch0 -p0
%endif
%patch1 -p0
%patch2 -p1

%build
%{configure} \
	--with-conf \
	--with%{!?with_clucene:out}-clucene \
	--with%{!?with_curl:out}-curl \
	--with%{!?with_icu:out}-icu \
	--disable-debug \
	--disable-dependency-tracking \
	--disable-examples \
	--disable-tests \
	--%{?with_utilities:en}%{!?with_utilities:dis}able-utilities \
	#--with%{!?with_icusword:out}-icusword \

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-strip \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install_config \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/sword
exit 0

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%config %{_sysconfdir}/sword.conf
%dir %{_datadir}/sword
%dir %{_datadir}/sword/mods.d
%dir %{_datadir}/sword/locales.d
%config %{_datadir}/sword/mods.d/globals.conf
%config %{_datadir}/sword/locales.d/*.conf
%doc README AUTHORS NEWS INSTALL
%attr(755,root,root) %{_libdir}/libsword*.so*
%dir %{_libdir}/sword
%dir %{_libdir}/sword/*icu*
%{_libdir}/sword/*/*.res

%files utilities
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_pkgconfigdir}/sword.pc
%{_includedir}/sword
%{_libdir}/libsword*.*a

%clean
rm -rf $RPM_BUILD_ROOT
