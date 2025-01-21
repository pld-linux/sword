# TODO:
# - Package icu-sword and add bcond for it here
#
# Conditional build:
%bcond_without	clucene		# Lucene searching support
%bcond_without	curl		# manager support using libcurl
%bcond_without	cxx11		# C++11 regex support
%bcond_without	icu		# ICU for Unicode
%bcond_with	icusword	# custom SWORD ICU
%bcond_without	utilities	# sword utilities

%define debug_package 0

Summary:	The SWORD Project framework for manipulating Bible texts
Summary(pl.UTF-8):	Szkielet projektu SWORD do pracy nad tekstami biblijnymi
Name:		sword
Version:	1.9.0
Release:	6
License:	GPL v2
Group:		Libraries
Source0:	http://www.crosswire.org/ftpmirror/pub/sword/source/v1.9/%{name}-%{version}.tar.gz
# Source0-md5:	7b86ab627993ef295307e3729d8edef2
Patch0:		icu76.patch
URL:		http://www.crosswire.org/sword
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	cppunit-devel >= 1.8.0
%{?with_clucene:BuildRequires:	clucene-core-devel >= 2.3}
%{?with_curl:BuildRequires:	curl-devel}
#%{?with_icu:BuildRequires:	icu}
%{?with_icusword:BuildRequires:	icu-sword}
%{?with_icu:BuildRequires:	libicu-devel}
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	libtool >= 2:1.5
BuildRequires:	pakchois-devel
BuildRequires:	pkgconfig >= 1:0.14
BuildRequires:	sqlite3-devel
BuildRequires:	zlib-devel
%{?with_clucene:Requires:	clucene-core >= 2.3}
%{?with_curl:Requires:	curl}
%{?with_icu:Requires:	icu}
%{?with_icusword:Requires:	icu-sword}
Requires:	wwwbrowser
Requires:	zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The SWORD Project creates cross-platform open-source tools that allow
programmers and Bible societies to write new Bible software more
quickly and easily. The SWORD Bible Framework allows easy manipulation
of Bible texts, commentaries, lexicons, dictionaries, etc. Many
frontends are built using this framework. An installed module set may
be shared between any frontend using the framework.

%description -l pl.UTF-8
Projekt SWORD tworzy wieloplatformowe, mające otwarte źródła narzędzia
pozwalające programistom oraz badaczom biblijnym pisać nowe
oprogramowanie biblijne szybciej i łatwiej. Szkielet biblijny SWORD
pozwala na łatwe operowanie na biblijnych tekstach, komentarzach,
leksykonach, słownikach itp. W oparciu o ten szkielet powstaje wiele
interfejsów użytkownika. Zainstalowany zestaw modułów może być łatwo
współdzielony między interfejsami.

%package utilities
Summary:	Utility programs that use the sword library
Summary(pl.UTF-8):	Programy narzędziowe wykorzystujące bibliotekę sword
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}
Provides:	diatheke

%description utilities
Utility programs that use the sword library.

%description utilities -l pl.UTF-8
Programy narzędziowe wykorzystujące bibliotekę sword.

%package devel
Summary:	Include files for developing sword applications
Summary(pl.UTF-8):	Pliki nagłówkowe do rozwijania aplikacji sword
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	curl-devel >= 7.10.5
Requires:	zlib-devel

%description devel
Include files for developing sword applications. This package is
required to compile Sword frontends, too.

%description devel -l pl.UTF-8
Pliki nagłówkowe do rozwijania plikacji sword. Ten pakiet jest
wymagany także do kompilowania interfejsów użytkownika sword.

%package static
Summary:	Static library for developing sword applications
Summary(pl.UTF-8):	Biblioteka statyczna do rozwijania aplikacji sword
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static library for developing sword applications.

%description static -l pl.UTF-8
Biblioteka statyczna do rozwijania aplikacji sword.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--with-conf \
	--with-clucene%{!?with_clucene:=no} \
	--with-curl%{!?with_curl:=no} \
	%{?with_cxx11:--with-cxx11regex} \
	--with-icu%{!?with_icu:=no} \
	%{?with_icusword:--with-icusword} \
	--disable-debug \
	--disable-dependency-tracking \
	--disable-examples \
	--disable-tests \
	--enable-utilities%{!?with_utilities:=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install-strip \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} install_config \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libsword.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog INSTALL README
%attr(755,root,root) %{_libdir}/libsword-%{version}.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sword.conf
%dir %{_datadir}/sword
%dir %{_datadir}/sword/mods.d
%dir %{_datadir}/sword/locales.d
%{_datadir}/sword/mods.d/globals.conf
%{_datadir}/sword/locales.d/*.conf

%files utilities
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/diatheke
%attr(755,root,root) %{_bindir}/emptyvss
%attr(755,root,root) %{_bindir}/imp2gbs
%attr(755,root,root) %{_bindir}/imp2ld
%attr(755,root,root) %{_bindir}/imp2vs
%attr(755,root,root) %{_bindir}/installmgr
%attr(755,root,root) %{_bindir}/mkfastmod
%attr(755,root,root) %{_bindir}/mod2imp
%attr(755,root,root) %{_bindir}/mod2osis
%attr(755,root,root) %{_bindir}/mod2vpl
%attr(755,root,root) %{_bindir}/mod2zmod
%attr(755,root,root) %{_bindir}/osis2mod
%attr(755,root,root) %{_bindir}/tei2mod
%attr(755,root,root) %{_bindir}/vpl2mod
%attr(755,root,root) %{_bindir}/vs2osisref
%attr(755,root,root) %{_bindir}/vs2osisreftxt
%attr(755,root,root) %{_bindir}/xml2gbs

%files devel
%defattr(644,root,root,755)
%doc doc/*
%attr(755,root,root) %{_libdir}/libsword.so
%{_includedir}/sword
%{_pkgconfigdir}/sword.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsword.a
