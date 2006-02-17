#
# Conditional build:
%bcond_with	mmx	# MMX optimization
# Optimization must be chosen at compile time :(
# Maybe some patch...? But not yet.
#
%ifarch athlon
%define with_mmx 1
%endif
Summary:	Password cracker
Summary(pl):	�amacz hase�
Name:		john
Version:	1.7
Release:	0.2
License:	GPL
Group:		Applications/System
Source0:	http://www.openwall.com/john/d/%{name}-%{version}.tar.bz2
# Source0-md5:	615b912caa677eec790e28745a12b2ae
Patch0:		%{name}-mailer.patch
URL:		http://www.openwall.com/john/
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	sed >= 4.0
Requires:	words
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
John the Ripper is a password cracker, currently available for UNIX,
DOS, WinNT/Win95. Its primary purpose is to detect weak UNIX
passwords. It has been tested with Linux x86/Alpha/SPARC, FreeBSD x86,
OpenBSD x86, Solaris 2.x SPARC and x86, Digital UNIX, AIX, HP-UX, and
IRIX.

%description -l pl
John The Ripper jest "�amaczem" hase� dost�pnym dla system�w UNIX,
DOS, WinNT/Win95. G��wnym jego zadaniem jest wykrywanie "s�abych"
hase�. By� testowany z Linux x86/Alpha/SPARC, FreeBSD x86, OpenBSD x86,
Solaris 2.x SPARC i x86, Digital UNIX, AIX, HP-UX oraz IRIX.

%prep
%setup -q 
%patch0 -p1

sed -i -e 's/CLK_TCK/CLOCKS_PER_SEC/g' src/*.c

%build
cd src

# bleh... MMX code must be chosen at compile time :(
# cannot use MMX for generic i586 nor i686 (Pentium/Pentium Pro have no MMX)
# K6 optimization exists only in Makefile
%ifarch %{ix86}
	%if %{with mmx}
		TARG=linux-x86-mmx
	%else
		TARG=linux-x86-any
	%endif
%else
	%ifarch alpha
		TARG=linux-alpha
	%else
		%ifarch sparc64
			TARG=linux-sparc
		%else
			%ifarch %{x8664}
				TARG=linux-x86-64
			%else
				TARG=generic
			%endif	
		%endif
	%endif
%endif

%{__make} $TARG \
	CFLAGS="-c -Wall -fomit-frame-pointer %{rpmcflags} -DJOHN_SYSTEMWIDE=1" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/john}
install run/{*.conf,*.chr,*.lst} $RPM_BUILD_ROOT%{_datadir}/john
install run/john $RPM_BUILD_ROOT%{_bindir}

rm -f doc/INSTALL


cd $RPM_BUILD_ROOT%{_bindir}
ln -sf john unafs
ln -sf john unique
ln -sf john unshadow

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* run/mailer
%attr(755,root,root) %{_bindir}/*
%{_datadir}/john