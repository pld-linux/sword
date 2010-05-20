#
# TODO:
# - Split subpackage out for diatheke
# - Add bconds for icu, utilities, tests, clucene, icusword, curl
# - Fix debug package. Patch Makefile so debugfiles.list is generated?
#
%define debug_package %{nil}

Summary:	The SWORD Project framework for manipulating Bible texts
Name:		sword
Version:	1.6.1
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://www.crosswire.org/ftpmirror/pub/sword/source/v1.6/%{name}-%{version}.tar.gz
# Source0-md5:	347e72f73313ff3ba700368db76a5d50
URL:		http://www.crosswire.org/sword
BuildRequires:	clucene-core-devel
BuildRequires:	curl-devel
BuildRequires:	icu
Requires:	clucene-core
Requires:	curl
Requires:	icu
Requires:	zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SWORD Project is an effort to create an ever expanding software
package for research and study of God and His Word. The SWORD Bible
Framework allows easy manipulation of Bible texts, commentaries,
lexicons, dictionaries, etc. Many frontends are build using this
framework. An installed module set may be shared between any frontend
using the framework.

%package devel
Summary:	Include files and static libraries for developing sword applications
Group:		Development/Libraries
Requires:	curl-devel >= 7.10.5
Requires:	sword = %{version}
Requires:	zlib-devel

%description devel
Include files and static libraries for developing sword applications.
This package is required to compile Sword frontends, too.

%prep
%setup -q

%build
%{configure} \
	--with-conf \
	--disable-utilities \
	--disable-debug \
	--disable-tests \
	--disable-dependency-tracking

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
%config %{_datadir}/sword/mods.d/globals.conf
%config %{_datadir}/sword/locales.d/*.conf
%doc README AUTHORS NEWS INSTALL
%attr(755,root,root) %{_libdir}/libsword*.so*
%dir %{_libdir}/sword
%{_libdir}/sword/*/*.res

%files devel
%defattr(644,root,root,755)
%doc doc/*
%{_pkgconfigdir}/sword.pc
%{_includedir}/sword
%{_libdir}/libsword*.*a

%clean
rm -rf $RPM_BUILD_ROOT
