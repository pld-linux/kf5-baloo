#
# Conditional build:
%bcond_with	tests		# build without tests

# TODO:
# - runtime Requires if any

%define		kdeframever	5.115
%define		qtver		5.15.2
%define		kfname		baloo
Summary:	A  file indexing and file search framework
Name:		kf5-%{kfname}
Version:	5.115.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	d145b146adf0ae1d3c104d17a79e156a
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
BuildRequires:	cmake >= 3.16
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
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


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
%attr(755,root,root) %{_bindir}/baloo_file
%attr(755,root,root) %{_bindir}/baloo_file_extractor
%attr(755,root,root) %{_bindir}/balooctl
%attr(755,root,root) %{_bindir}/baloosearch
%attr(755,root,root) %{_bindir}/balooshow
/etc/xdg/autostart/baloo_file.desktop
%{_datadir}/qlogging-categories5/baloo.categories
%{_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.fileindexer.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.main.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.scheduler.xml
%attr(755,root,root) %{_libdir}/libKF5Baloo.so.*.*.*
%ghost %{_libdir}/libKF5Baloo.so.5
%attr(755,root,root) %{_libdir}/libKF5BalooEngine.so.*.*.*
%ghost %{_libdir}/libKF5BalooEngine.so.5
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
%{_datadir}/dbus-1/interfaces/org.kde.BalooWatcherApplication.xml
%{_datadir}/qlogging-categories5/baloo.renamecategories
%{systemduserunitdir}/kde-baloo.service
%attr(755,root,root) %{_prefix}/libexec/baloo_file
%attr(755,root,root) %{_prefix}/libexec/baloo_file_extractor

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5Baloo.so
%{_includedir}/KF5/Baloo
%{_libdir}/cmake/KF5Baloo
%{_pkgconfigdir}/Baloo.pc
%{_libdir}/qt5/mkspecs/modules/qt_Baloo.pri
