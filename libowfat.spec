Summary:	Reimplement libdjb under GPL
Name:		libowfat
Version:	0.27
Release:	%mkrel 1
License:	GPLv2+
Group:		Development/C
URL:		http://www.fefe.de/libowfat/
Source0:	http://www.fefe.de/%{name}/%{name}-%{version}.tar.bz2
Source1:	http://www.fefe.de/%{name}/%{name}-%{version}.tar.bz2.sig
BuildRequires:	dietlibc-devel >= 0.20
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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

%package -n	%{name}-devel
Summary:	Static library and header files for the %{name} library
Group:		Development/C
Requires:	dietlibc-devel >= 0.20

%description -n	%{name}-devel
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

%prep

%setup -q

%build
make -f GNUmakefile \
    prefix="%{_libdir}/dietlibc" \
    DIET="%{_bindir}/diet -Os"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/dietlibc

make -f GNUmakefile \
    prefix="%{buildroot}%{_libdir}/dietlibc" \
    LIBDIR="%{buildroot}%{_libdir}/dietlibc/lib" \
    DIET="%{_bindir}/diet -Os" \
    MAN3DIR="%{buildroot}%{_mandir}/man3" \
    install

# fix conflicting file (from openssl-devel)
mv %{buildroot}%{_mandir}/man3/buffer.3 \
    %{buildroot}%{_mandir}/man3/buffer-libowfat.3

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n %{name}-devel
%defattr(-,root,root)
%doc CHANGES README
%{_libdir}/dietlibc/lib/libowfat.a
%{_libdir}/dietlibc/include/*.h
%{_mandir}/man3/*


