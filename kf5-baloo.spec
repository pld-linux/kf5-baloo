#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	5.116
%define		kf_ver		%{version}
%define		qt_ver		5.15.2
%define		kfname		baloo
Summary:	A file indexing and file search framework
Summary(pl.UTF-8):	Szkielet indeksowania i wyszukiwania plików
Name:		kf5-%{kfname}
Version:	5.116.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	41fd11dfe5af84d2bbd214e4e04d41e9
Patch0:		kf5-baloo-absolute-path.patch
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5DBus-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	Qt5Network-devel >= %{qt_ver}
BuildRequires:	Qt5Qml-devel >= %{qt_ver}
BuildRequires:	Qt5Quick-devel >= %{qt_ver}
BuildRequires:	Qt5Test-devel >= %{qt_ver}
BuildRequires:	Qt5Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.16
BuildRequires:	gettext-tools
BuildRequires:	kf5-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf5-kconfig-devel >= %{kf_ver}
BuildRequires:	kf5-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf5-kcrash-devel >= %{kf_ver}
BuildRequires:	kf5-kdbusaddons-devel >= %{kf_ver}
BuildRequires:	kf5-kfilemetadata-devel >= %{kf_ver}
BuildRequires:	kf5-ki18n-devel >= %{kf_ver}
BuildRequires:	kf5-kidletime-devel >= %{kf_ver}
BuildRequires:	kf5-kio-devel >= %{kf_ver}
BuildRequires:	kf5-solid-devel >= %{kf_ver}
BuildRequires:	lmdb-devel
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5DBus >= %{qt_ver}
Requires:	Qt5Gui >= %{qt_ver}
Requires:	Qt5Qml >= %{qt_ver}
Requires:	kf5-dirs
Requires:	kf5-kconfig >= %{kf_ver}
Requires:	kf5-kcoreaddons >= %{kf_ver}
Requires:	kf5-kcrash >= %{kf_ver}
Requires:	kf5-kdbusaddons >= %{kf_ver}
Requires:	kf5-kfilemetadata >= %{kf_ver}
Requires:	kf5-ki18n >= %{kf_ver}
Requires:	kf5-kidletime >= %{kf_ver}
Requires:	kf5-kio >= %{kf_ver}
Requires:	kf5-solid >= %{kf_ver}
Conflicts:	kde4-baloo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Baloo is the file indexing and file search framework for KDE.

Baloo focuses on providing a very small memory footprint along with
with extremely fast searching. It internally uses a mixture of SQLite
along with Xapian to store the file index.

%description -l pl.UTF-8
Baloo to szkielet indeksowania i wyszukiwania plików dla KDE.

Skupia się na połączeniu bardzo małego zużycia pamięci wraz z bardzo
szybkim wyszukiwaniem. Wewnętrznie używa połączenia rozwiązań SQLite i
Xapian do przchowywania indeksu plików.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	kf5-kcoreaddons-devel >= %{kf_ver}
Requires:	kf5-kfilemetadata-devel >= %{kf_ver}

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

%find_lang %{kfname}5 --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/baloo_file
%attr(755,root,root) %{_bindir}/baloo_file_extractor
%attr(755,root,root) %{_bindir}/balooctl
%attr(755,root,root) %{_bindir}/baloosearch
%attr(755,root,root) %{_bindir}/balooshow
%attr(755,root,root) %{_libexecdir}/baloo_file
%attr(755,root,root) %{_libexecdir}/baloo_file_extractor
%attr(755,root,root) %{_libdir}/libKF5Baloo.so.*.*.*
%ghost %{_libdir}/libKF5Baloo.so.5
%attr(755,root,root) %{_libdir}/libKF5BalooEngine.so.*.*.*
%ghost %{_libdir}/libKF5BalooEngine.so.5
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kded/baloosearchmodule.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/baloosearch.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/tags.so
%attr(755,root,root) %{_libdir}/qt5/plugins/kf5/kio/timeline.so
%dir %{_libdir}/qt5/qml/org/kde/baloo
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/baloo/libbalooplugin.so
%{_libdir}/qt5/qml/org/kde/baloo/qmldir
%dir %{_libdir}/qt5/qml/org/kde/baloo/experimental
%attr(755,root,root) %{_libdir}/qt5/qml/org/kde/baloo/experimental/libbaloomonitorplugin.so
%{_libdir}/qt5/qml/org/kde/baloo/experimental/qmldir
%{_datadir}/dbus-1/interfaces/org.kde.BalooWatcherApplication.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.file.indexer.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.fileindexer.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.main.xml
%{_datadir}/dbus-1/interfaces/org.kde.baloo.scheduler.xml
%{_datadir}/qlogging-categories5/baloo.categories
%{_datadir}/qlogging-categories5/baloo.renamecategories
%{systemduserunitdir}/kde-baloo.service
/etc/xdg/autostart/baloo_file.desktop

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5Baloo.so
%{_includedir}/KF5/Baloo
%{_libdir}/cmake/KF5Baloo
%{_pkgconfigdir}/Baloo.pc
%{_libdir}/qt5/mkspecs/modules/qt_Baloo.pri
