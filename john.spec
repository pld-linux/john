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
Release:	2
License:	GPL
Group:		Applications/System
Source0:	http://www.openwall.com/john/g/%{name}-%{version}.tar.bz2
# Source0-md5:	321ac0793f1aa4f0603b33a393133756
Patch0:		%{name}-mailer.patch
Patch1:		optflags.patch
%{?with_jumbopatch:Patch1: http://www.openwall.com/john/contrib/%{name}-%{version}-jumbo-2.diff.gz}
URL:		http://www.openwall.com/john/
%{?with_jumbopatch:BuildRequires: openssl-devel >= 0.9.7}
BuildRequires:	rpmbuild(macros) >= 1.213
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
%patch1 -p1
%{?with_jumbopatch:%patch1 -p1}

rm -f doc/INSTALL

%build
cd src

cat > defs.h <<'EOF'
#define	JOHN_SYSTEMWIDE 1
#define	JOHN_SYSTEMWIDE_EXEC "%{_libdir}/john"
EOF

%if %{do_mmxfb}
%{__make} linux-x86-any \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} -include defs.h"
mv ../run/john ../run/john-non-mmx
%{__make} clean
%endif

TARG=generic
%ifarch %{ix86}
	%if %{do_mmx}
		TARG=linux-x86-mmx
	%else
		TARG=linux-x86-any
	%endif
%endif
%ifarch alpha
	TARG=linux-alpha
%endif
%ifarch sparc sparcv9
	TARG=linux-sparc
%endif
%ifarch %{x8664}
	TARG=linux-x86-64
%endif

%{__make} $TARG \
	CC="%{__cc}" \
	OPTFLAGS='%{rpmcflags} -include defs.h %{?optmmxfb}'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/john}
cp -a run/{*.conf,*.chr,*.lst} $RPM_BUILD_ROOT%{_datadir}/john
install -p run/john $RPM_BUILD_ROOT%{_bindir}
%if %{do_mmxfb}
install -d $RPM_BUILD_ROOT%{_libdir}/john
install -p run/john-non-mmx $RPM_BUILD_ROOT%{_libdir}/john
%endif

ln -sf john $RPM_BUILD_ROOT%{_bindir}/unafs
ln -sf john $RPM_BUILD_ROOT%{_bindir}/unique
ln -sf john $RPM_BUILD_ROOT%{_bindir}/unshadow

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* run/mailer
%attr(755,root,root) %{_bindir}/john
%attr(755,root,root) %{_bindir}/unafs
%attr(755,root,root) %{_bindir}/unique
%attr(755,root,root) %{_bindir}/unshadow
%if %{do_mmxfb}
%dir %{_libdir}/john
%attr(755,root,root) %{_libdir}/john/john-non-mmx
%endif
%{_datadir}/john
