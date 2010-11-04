#
# Conditional build:
%bcond_with jumbopatch	# This patch integrates lots of contributed
			# patches adding support for over 30 
			# of additional hash types, and more. 

%ifarch i586 i686 athlon pentium2 pentium3 pentium4
%define do_mmx 1
%else
%define	do_mmx 0
%endif
%ifarch i586 i686
%define do_mmxfb 1
%define	optmmxfb	-DCPU_FALLBACK=1
%else
%define do_mmxfb 0
%undefine optmmxfb
%endif
Summary:	Password cracker
Summary(pl.UTF-8):	Łamacz haseł
Name:		john
Version:	1.7.6
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.openwall.com/john/g/%{name}-%{version}.tar.bz2
# Source0-md5:	321ac0793f1aa4f0603b33a393133756
Patch0:		%{name}-mailer.patch
%{?with_jumbopatch:Patch1:		http://www.openwall.com/john/contrib/john-%{version}-jumbo-2.diff.gz}
URL:		http://www.openwall.com/john/
BuildRequires:	rpmbuild(macros) >= 1.213
%{?with_jumbopatch:BuildRequires:        openssl-devel >= 0.9.7}
Requires:	words
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
John the Ripper is a fast password cracker, currently available for
many flavors of Unix (11 are officially supported, not counting
different architectures), DOS, Win32, BeOS, and OpenVMS (the latter
requires a contributed patch). Its primary purpose is to detect weak
Unix passwords. Besides several crypt(3) password hash types most
commonly found on various Unix flavors, supported out of the box are
Kerberos/AFS and Windows NT/2000/XP LM hashes, plus several more with
contributed patches.

%description -l pl.UTF-8
John The Ripper jest szybkim "łamaczem" haseł dostępnym dla wielu
rodzajów uniksów (oficjalnie obsługiwanych jest 11, nie licząc różnych
architektur), DOS-a, Win32, BeOS-a i OpenVMS-a (ten ostatni wymaga
łaty). Głównym zastosowaniem jest wykrywanie słabych haseł uniksowych.
Oprócz różnych rodzajów skrótów haseł crypt(3) najczęściej używanych
na różnych uniksach, obsługiwane są także skróty Kerberos/AFS oraz
Windows NT/2000/XP LM, a także kilka innych przy użyciu łat.

%prep
%setup -q
%patch0 -p1
%{?with_jumbopatch:%patch1 -p1}

%build
cd src

%if %{do_mmxfb}
%{__make} linux-x86-any \
	CFLAGS="-c -Wall -fomit-frame-pointer %{rpmcflags} -DJOHN_SYSTEMWIDE=1" \
	CC="%{__cc}"
mv ../run/john ../run/john-non-mmx
%{__make} clean
%endif

%ifarch %{ix86}
	%if %{do_mmx}
		TARG=linux-x86-mmx
	%else
		TARG=linux-x86-any
	%endif
%else
	%ifarch alpha
		TARG=linux-alpha
	%else
		%ifarch sparc sparcv9
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
	CFLAGS="-c -Wall -fomit-frame-pointer %{rpmcflags} -DJOHN_SYSTEMWIDE=1 -DJOHN_SYSTEMWIDE_EXEC=\\\"%{_libdir}/john\\\" %{?optmmxfb}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/john}
install run/{*.conf,*.chr,*.lst} $RPM_BUILD_ROOT%{_datadir}/john
install run/john $RPM_BUILD_ROOT%{_bindir}
%if %{do_mmxfb}
install -d $RPM_BUILD_ROOT%{_libdir}/john
install run/john-non-mmx $RPM_BUILD_ROOT%{_libdir}/john
%endif

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
%if %{do_mmxfb}
%dir %{_libdir}/john
%attr(755,root,root) %{_libdir}/john/john-non-mmx
%endif
%{_datadir}/john
