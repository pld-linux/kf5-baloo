#
# Conditional build:
%bcond_with	tests		# build without tests

# TODO:
# - runtime Requires if any

%define		kdeframever	5.13
%define		qtver		5.3.2
%define		kfname		baloo
Summary:	A  file indexing and file search framework
Name:		kf5-%{kfname}
Version:	5.13.0
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	67bceaf70f9da493161c0eb94a214099
Patch0:		kf5-baloo-absolute-path.patch
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 2.8.12
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	kf5-kidletime-devel >= %{version}
BuildRequires:	kf5-kfilemetadata-devel >= %{version}
BuildRequires:	lmdb-devel
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Conflicts:	kde4-baloo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Baloo is the file indexing and file search framework for KDE.

Baloo focuses on providing a very small memory footprint along with
with extremely fast searching. It internally uses a mixture of sqlite
along with Xapian to store the file index.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}
%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/baloo-monitor
%attr(755,root,root) %{_bindir}/baloo_file
%attr(755,root,root) %{_bindir}/baloo_file_extractor
%attr(755,root,root) %{_bindir}/balooctl
%attr(755,root,root) %{_bindir}/baloosearch
%attr(755,root,root) %{_bindir}/balooshow
%attr(755,root,root) %{_libdir}/kauth/kde_baloo_filewatch_raiselimit
/etc/dbus-1/system.d/org.kde.baloo.filewatch.conf
/etc/xdg/autostart/baloo_file.desktop
%{_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml
%{_datadir}/dbus-1/system-services/org.kde.baloo.filewatch.service
%attr(755,root,root) %{_libdir}/libKF5Baloo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5Baloo.so.5
%attr(755,root,root) %{_libdir}/libKF5BalooEngine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5BalooEngine.so.5
%attr(755,root,root) %{_libdir}/qt5/plugins/kded_baloosearch_kio.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/baloosearch.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/tags.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/timeline.so
%dir %{_libdir}/qt5/qml/org/kde/baloo
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/baloo/libbalooplugin.so
%{_iconsdir}/hicolor/128x128/apps/baloo.png
%{_datadir}/kservices5/baloosearch.protocol
%{_datadir}/kservices5/kded/baloosearchfolderupdater.desktop
%{_datadir}/kservices5/tags.protocol
%{_datadir}/kservices5/timeline.protocol
%{_datadir}/polkit-1/actions/org.kde.baloo.filewatch.policy

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5Baloo.so
%attr(755,root,root) %{_libdir}/libKF5BalooEngine.so
%{_includedir}/KF5/Baloo
%{_includedir}/KF5/baloo_version.h
%{_libdir}/cmake/KF5Baloo
%{_pkgconfigdir}/Baloo.pc
#%{_libdir}/qt5/mkspecs/modules/qt_Attica.pri
