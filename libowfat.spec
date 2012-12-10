%define name libowfat
%define version 0.28
%define release %mkrel 9
%define libname %mklibname owfat 0

Summary:		Reimplement libdjb under GPL
Name:			%{name}
Version:		%{version}
Release:		%{release}
License:		GPLv2+
Group:			Development/C
URL:			http://www.fefe.de/libowfat/
Source0:		http://www.fefe.de/%{name}/%{name}-%{version}.tar.bz2
Source1:		http://www.fefe.de/%{name}/%{name}-%{version}.tar.bz2.sig
Patch0:			libowfat-0.28-shared.patch
BuildRequires:	dietlibc-devel >= 0.32
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
make -f GNUmakefile \
	DIET=''

%install
rm -rf %{buildroot}

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
%{_libdir}/dietlibc/lib/libowfat.a
%{_libdir}/dietlibc/include/*.h
%{_mandir}/man3/*


%changelog
* Sun Aug 30 2009 Raphaël Gertz <rapsys@mandriva.org> 0.28-9mdv2010.0
+ Revision: 422476
- Rebuild for x86_64
- Re-add static library

* Sat Aug 29 2009 Raphaël Gertz <rapsys@mandriva.org> 0.28-8mdv2010.0
+ Revision: 422301
- Rebuild for fixed lib major number

* Sat Aug 29 2009 Raphaël Gertz <rapsys@mandriva.org> 0.28-7mdv2010.0
+ Revision: 422299
- Fix missing symbolic links

* Sat Aug 29 2009 Raphaël Gertz <rapsys@mandriva.org> 0.28-6mdv2010.0
+ Revision: 422297
- Split in lib and lib-devel

* Sat Aug 29 2009 Raphaël Gertz <rapsys@mandriva.org> 0.28-5mdv2010.0
+ Revision: 422199
- Fix libdir path
  Rebuild for x86_64
- Rebuild for x86_64
- Should fix build on x86_64
- Re-up with 644 right
  Patch to build as shared library
- Remove for invalid 664 files right

* Tue Aug 25 2009 Oden Eriksson <oeriksson@mandriva.com> 0.28-1mdv2010.0
+ Revision: 420670
- 0.28

* Fri Aug 08 2008 Thierry Vignaud <tvignaud@mandriva.com> 0.27-3mdv2009.0
+ Revision: 267985
- rebuild early 2009.0 package (before pixel changes)

* Tue Jun 10 2008 Oden Eriksson <oeriksson@mandriva.com> 0.27-2mdv2009.0
+ Revision: 217541
- rebuilt against dietlibc-devel-0.32

* Sat Feb 02 2008 Funda Wang <fundawang@mandriva.org> 0.27-1mdv2008.1
+ Revision: 161360
- New version 0.27

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0.24-1mdv2008.1
+ Revision: 136557
- restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Dec 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.24-1mdv2007.0
+ Revision: 94247
- Import libowfat

* Sat Apr 29 2006 Oden Eriksson <oeriksson@mandriva.com> 0.24-1mdk
- 0.24

* Tue Feb 01 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 0.21-1mdk
- 0.21

* Fri Aug 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.20-1mdk
- 0.20

* Tue Jun 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 0.19.2-1mdk
- 0.19.2

