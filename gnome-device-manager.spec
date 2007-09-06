%define alphatag 20070906

%define lib_major 0
%define lib_name %mklibname gnome-device-manager %{lib_major}
%define develname %mklibname gnome-device-manager -d

Summary: Device manager for the GNOME desktop
Name: gnome-device-manager
Version: 0.2
Release: %mkrel 0.%{alphatag}.1
License: GPL
URL: http://
Group: Graphical desktop/GNOME
Source0: %{name}-%{version}.tar.bz2
# (fc) 0.2-0.20070906.1mdv fix error in Makefile.am
Patch0: gnome-device-manager-0.2-fixbuild.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: hal-devel >= 0.5.5 gtk2-devel >= 2.8.0 dbus-devel >= 0.62
BuildRequires: gettext
BuildRequires: scrollkeeper
Requires: hal >= 0.5.7
Requires: dbus >= 0.62
Requires: dbus-glib >= 0.62
Obsoletes: hal-gnome <= 0.5.9.1
Provides: hal-gnome

%description
Device manager for the GNOME desktop that uses HAL to do all the heavy lifting.

%package -n %{lib_name}
Summary: Shared library for gnome-device-manager
Group: System/Libraries

%description -n %{lib_name}
gnome-device-manager shared library.

%package -n %{develname}
Summary: Libraries and headers for gnome-device-manager
Group: Development/C
Requires: %{name} = %{version}
Requires: %{lib_name} = %{version}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname}
Headers and static libraries for gnome-device-manager.

%prep
rm -rf $RPM_BUILD_ROOT

%setup -q
%patch0 -p1 -b .fixbuild

#needed by patch0
autoreconf

%build
%configure2_5x --disable-scrollkeeper
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

rm -f $RPM_BUILD_ROOT%{_libdir}/*.a

%find_lang %name --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_scrollkeeper
%update_icon_cache hicolor

%postun
%clean_scrollkeeper
%clean_icon_cache hicolor

%post -n %{lib_name} -p /sbin/ldconfig

%postun -n %{lib_name} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README
%{_bindir}/gnome-device-manager
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/gnome-device-manager.desktop
%{_datadir}/omf/gnome-device-manager

%files -n %{lib_name}
%defattr(-,root,root)
%{_libdir}/libgnome-device-manager.so.%{lib_major}*


%files -n %{develname}
%defattr(-,root,root)
%{_libdir}/libgnome-device-manager.so
%{_libdir}/libgnome-device-manager.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/gnome-device-manager
