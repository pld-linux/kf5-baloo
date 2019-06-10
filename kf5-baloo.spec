#
# Conditional build:
%bcond_with	tests		# build without tests

# TODO:
# - runtime Requires if any

%define		kdeframever	5.59
%define		qtver		5.9.0
%define		kfname		baloo
Summary:	A  file indexing and file search framework
Name:		kf5-%{kfname}
Version:	5.59.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	http://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	74088b26525af31670f0d4e42c7f6757
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
BuildRequires:	kf5-kfilemetadata-devel >= %{version}
BuildRequires:	kf5-kidletime-devel >= %{version}
BuildRequires:	kf5-kio-devel >= %{version}
BuildRequires:	lmdb-devel
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
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
Requires:	kf5-kfilemetadata-devel >= %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
install -d build
cd build
%cmake -G Ninja \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	..
%ninja_build

%{?with_tests:%ninja_build test}

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5 --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
#%%attr(755,root,root) %{_bindir}/baloo-monitor
%attr(755,root,root) %{_bindir}/baloo_file
%attr(755,root,root) %{_bindir}/baloo_file_extractor
%attr(755,root,root) %{_bindir}/balooctl
%attr(755,root,root) %{_bindir}/baloosearch
%attr(755,root,root) %{_bindir}/balooshow
#%%attr(755,root,root) %{_libdir}/kauth/kde_baloo_filewatch_raiselimit
#/etc/dbus-1/system.d/org.kde.baloo.filewatch.conf
/etc/xdg/autostart/baloo_file.desktop
/etc/xdg/baloo.categories
%{_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.fileindexer.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.main.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.scheduler.xml
#%%{_datadir}/dbus-1/system-services/org.kde.baloo.filewatch.service
%attr(755,root,root) %{_libdir}/libKF5Baloo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5Baloo.so.5
%attr(755,root,root) %{_libdir}/libKF5BalooEngine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libKF5BalooEngine.so.5
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kded/baloosearchmodule.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/baloosearch.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/tags.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/timeline.so
%dir %{_libdir}/qt5/qml/org/kde/baloo
%dir %{_libdir}/qt5/qml/org/kde/baloo/experimental
%{_libdir}/qt5/qml/org/kde/baloo/qmldir
%{_libdir}/qt5/qml/org/kde/baloo/experimental/qmldir
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/baloo/libbalooplugin.so
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/baloo/experimental/libbaloomonitorplugin.so
%{_iconsdir}/hicolor/128x128/apps/baloo.png
%{_datadir}/kservices5/baloosearch.protocol
#%%{_datadir}/kservices5/kded/baloosearchfolderupdater.desktop
%{_datadir}/kservices5/tags.protocol
%{_datadir}/kservices5/timeline.protocol
#%%{_datadir}/polkit-1/actions/org.kde.baloo.filewatch.policy
%{_datadir}/dbus-1/interfaces/org.kde.BalooWatcherApplication.xml

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5Baloo.so
#%%attr(755,root,root) %{_libdir}/libKF5BalooEngine.so
%{_includedir}/KF5/Baloo
%{_includedir}/KF5/baloo_version.h
%{_libdir}/cmake/KF5Baloo
%{_pkgconfigdir}/Baloo.pc
%{_libdir}/qt5/mkspecs/modules/qt_Baloo.pri
