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
Summary(pl):	£amacz hase³
Name:		john
Version:	1.6.37
Release:	7
License:	GPL
Group:		Applications/System
Source0:	http://www.openwall.com/john/a/%{name}-%{version}.tar.gz
# Source0-md5:	9403233b640927295c05b0564ff1f678
# needed for docs and charset files
Source1:	http://www.openwall.com/john/%{name}-1.6.tar.gz
# Source1-md5:	aae782f160041b2bdc624b0a84054e32
Patch0:		%{name}-1.6.PLD.diff
Patch1:		%{name}-1.6.ini.diff
Patch2:		%{name}-1.6.makefile.diff
Patch3:		ftp://ftp.banquise.net/users/bandecon/john-patch/john-1.6.37-bigpatch-11.diff.gz
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
John The Ripper jest "³amaczem" hase³ dostêpnym dla systemów UNIX,
DOS, WinNT/Win95. G³ównym jego zadaniem jest wykrywanie "s³abych"
hase³. By³ testowany z Linux x86/Alpha/SPARC, FreeBSD x86, OpenBSD x86,
Solaris 2.x SPARC i x86, Digital UNIX, AIX, HP-UX oraz IRIX.

%prep
%setup -q -a1
%patch0 -p1
#%patch1 -p1
#%patch2 -p1
# or move it to /var maybe?
%patch3 -p1
sed -i -e 's,/usr/lib,%{_libdir},' src/params.h run/john.conf

%build
cd src
COPT="%{rpmcflags}"

# bleh... MMX code must be chosen at compile time :(
# cannot use MMX for generic i586 nor i686 (Pentium/Pentium Pro have no MMX)
# K6 optimization exists only in Makefile
%ifarch %{ix86}
	%if %{with mmx}
		TARG=linux-x86-mmx-elf
	%else
		TARG=linux-x86-any-elf
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
	OPT="$COPT" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/john}
install run/john.conf john-1.6/run/*.chr $RPM_BUILD_ROOT%{_libdir}/john
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
%doc doc/* john-1.6/doc/{CONFIG,EXAMPLES,EXTERNAL,FAQ,MODES,NEWS,OPTIONS,RULES} run/mailer
%attr(755,root,root) %{_bindir}/*
%{_libdir}/john
