%define name libowfat
%define version 0.28
%define release %mkrel 8
%define libname %mklibname owfat 0

Summary:	Reimplement libdjb under GPL
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Development/C
URL:		http://www.fefe.de/libowfat/
Source0:	http://www.fefe.de/%{name}/%{name}-%{version}.tar.bz2
Source1:	http://www.fefe.de/%{name}/%{name}-%{version}.tar.bz2.sig
Patch0:		libowfat-0.28-shared.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
libowfat is a library of general purpose APIs extracted from Dan
Bernstein's software, reimplemented and covered by the GNU General
Public License Version 2 (no later versions).

The API has been slightly extended (for example, I provide a
uint32_read function, and I extended the socket API to support
IPv6) where I found it necessary or beneficial in a specific
project.

Many of the functions I implement here have since been placed in
the public domain, so there are other sources to get this code
(except for my extensions obviously).  The implementations here
may not be as portable as the original versions; I tend to focus
on the Single Unix Specification and not on some obsolete legacy
systems found in the basements of some vintage hardware clubs.

I also provide man pages for many functions, mostly extracted from
Dan's web documentation or documentation found in earlier versions
of his software.  For some reason, he abandoned man pages in favor
of HTML recently.

On July 4 2002, Dan also placed his DNS routines and supporting
low level functions in the public domain, so I copy them here
instead of reimplementing them.

http://online.securityfocus.com/archive/1/280642
has an online version of the bugtraq posting.

%package -n %{libname}
Summary:	Libowfat shared libraries
Group:		System/Servers

%description -n %{libname}
This package contains libowfat shared libraries.

%package -n	%{name}-devel
Group:		Development/C
Summary:	Headers and static lib for libowfat development
Requires:	%{libname} = %{version}-%{release}

%description -n	%{name}-devel
Install this package if you want do compile applications using the
libowfat library.

%prep
%setup -q
%patch0 -p1 -b .shared

%build
make -f GNUmakefile

%install
rm -rf %{buildroot}

make -f GNUmakefile \
	prefix=%{buildroot}%{_prefix} \
	MAN3DIR=%{buildroot}%{_mandir}/man3 \
	LIBDIR=%{buildroot}%{_libdir} \
    install
ln -s libowfat.so.%{version} %{buildroot}%{_libdir}/libowfat.so.0 
ln -s libowfat.so.%{version} %{buildroot}%{_libdir}/libowfat.so

# fix conflicting file (from openssl-devel)
mv %{buildroot}%{_mandir}/man3/buffer.3 \
    %{buildroot}%{_mandir}/man3/buffer-libowfat.3

%clean
rm -rf %{buildroot}

%files -n %{libname}
%doc CHANGES README
%defattr(-,root,root)
%{_libdir}/libowfat.so.0
%{_libdir}/libowfat.so.0.28

%files -n %{name}-devel
%defattr(-,root,root)
%{_libdir}/libowfat.so
%{_includedir}/*.h
%{_mandir}/man3/*
