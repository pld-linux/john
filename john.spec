#
# Conditional build:
# _with_mmx	- MMX optimization
# Optimization must be chosen at compile time :(
# Maybe some patch...? But not yet.
#
%ifarch athlon
%define _with_mmx 1
%endif
Summary:	Password cracker
Summary(pl):	�amacz hase�
Name:		john
Version:	1.6.37
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.openwall.com/john/%{name}-1.6.tar.gz
# Source0-md5:	aae782f160041b2bdc624b0a84054e32
Patch0:		%{name}-1.6.34.patch
Patch1:		%{name}-1.6.PLD.diff
Patch2:		%{name}-1.6.ini.diff
Patch3:		%{name}-1.6.makefile.diff
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
%setup -q -n %{name}-1.6
%patch0 -p1
%patch1 -p1
#%patch2 -p1
#%patch3 -p1

%build
cd src
COPT="%{rpmcflags}"

# bleh... MMX code must be chosen at compile time :(
# cannot use MMX for generic i586 nor i686 (Pentium/Pentium Pro have no MMX)
# K6 optimization exists only in Makefile
%ifarch %{ix86}
	%if %{?_with_mmx:1}%{!?_with_mmx:0}
		TARG=linux-x86-mmx-elf
	%else
		TARG=linux-x86-any-elf
	%endif
%else
	%ifarch alpha
		TARG=linux-alpha
	%else
		%ifarch sparc sparc64
			TARG=linux-sparc
		%else
			TARG=generic
		%endif
	%endif
%endif

%{__make} OPT="$COPT" CC="%{__cc}" $TARG

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/john}
install run/{*.chr,john.conf} $RPM_BUILD_ROOT%{_libdir}/john
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
%{_libdir}/john
