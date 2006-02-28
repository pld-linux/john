#
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
Summary(pl):	£amacz hase³
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
John the Ripper is a fast password cracker, currently available for
many flavors of Unix (11 are officially supported, not counting
different architectures), DOS, Win32, BeOS, and OpenVMS (the latter
requires a contributed patch). Its primary purpose is to detect weak
Unix passwords. Besides several crypt(3) password hash types most
commonly found on various Unix flavors, supported out of the box are
Kerberos/AFS and Windows NT/2000/XP LM hashes, plus several more with
contributed patches.

%description -l pl
John The Ripper jest szybkim "³amaczem" hase³ dostêpnym dla wielu
rodzajów uniksów (oficjalnie obs³ugiwanych jest 11, nie licz±c ró¿nych
architektur), DOS-a, Win32, BeOS-a i OpenVMS-a (ten ostatni wymaga
³aty). G³ównym zastosowaniem jest wykrywanie s³abych hase³ uniksowych.
Oprócz ró¿nych rodzajów skrótów hase³ crypt(3) najczê¶ciej u¿ywanych
na ró¿nych uniksach, obs³ugiwane s± tak¿e skróty Kerberos/AFS oraz
Windows NT/2000/XP LM, a tak¿e kilka innych przy u¿yciu ³at.

%prep
%setup -q
%patch0 -p1

sed -i -e 's/CLK_TCK/CLOCKS_PER_SEC/g' src/*.c

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
