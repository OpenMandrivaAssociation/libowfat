%define major 0
%define libname %mklibname owfat %{major}
%define devname %mklibname owfat -d

Summary:	Reimplement libdjb under GPL
Name:		libowfat
Version:	0.29
Release:	2
License:	GPLv2+
Group:		Development/C
Url:		http://www.fefe.de/libowfat/
Source0:	http://www.fefe.de/%{name}/%{name}-%{version}.tar.bz2
Patch0:		libowfat-0.29-shared.patch
BuildRequires:	dietlibc-devel >= 0.32

%description
libowfat is a library of general purpose APIs extracted from Dan
Bernstein's software, reimplemented and covered by the GNU General
Public License Version 2 (no later versions).

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Libowfat shared libraries
Group:		System/Servers

%description -n %{libname}
This package contains libowfat shared libraries.

%files -n %{libname}
%doc CHANGES README
%{_libdir}/libowfat.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Headers and static lib for libowfat development
Group:		Development/C
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Obsoletes:	%{name}-devel < 0.29
Conflicts:	%{name}-devel < 0.29

%description -n %{devname}
Install this package if you want do compile applications using the
libowfat library.

%files -n %{devname}
%{_libdir}/libowfat.so
%{_includedir}/*.h
%{_libdir}/dietlibc/lib/libowfat.a
%{_libdir}/dietlibc/include/*.h
%{_mandir}/man3/*

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1 -b .shared

%build
make -f GNUmakefile \
	DIET=''

%install
make -f GNUmakefile \
	DIET='' \
	prefix=%{buildroot}%{_prefix} \
	MAN3DIR=%{buildroot}%{_mandir}/man3 \
	LIBDIR=%{buildroot}%{_libdir} \
	install

make -f GNUmakefile clean
rm -f Makefile
mv -f GNUmakefile.shared GNUmakefile

make -f GNUmakefile \
	prefix="%{_libdir}/dietlibc" \
	DIET="%{_bindir}/diet -Os"

install -d %{buildroot}%{_libdir}/dietlibc
make -f GNUmakefile \
	prefix="%{buildroot}%{_libdir}/dietlibc" \
	LIBDIR="%{buildroot}%{_libdir}/dietlibc/lib" \
	DIET="%{_bindir}/diet -Os" \
	MAN3DIR="%{buildroot}%{_mandir}/man3" \
	install

ln -s libowfat.so.%{version} %{buildroot}%{_libdir}/libowfat.so.%{major}
ln -s libowfat.so.%{version} %{buildroot}%{_libdir}/libowfat.so

# fix conflicting file (from openssl-devel)
mv %{buildroot}%{_mandir}/man3/buffer.3 \
	%{buildroot}%{_mandir}/man3/buffer-libowfat.3

