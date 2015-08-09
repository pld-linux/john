#
# Conditional build:
%bcond_without	jumbo		# Build community-enhanced version with lots of contributed
				# patches adding support for over 30
				# of additional hash types, and more.
%bcond_with	avx		# use x86 AVX instructions
%bcond_with	xop		# use x86 XOP instructions
%bcond_with	altivec		# use PPC Altivec instructions

%if %{without jumbo}
%ifarch i586 i686 athlon pentium2 pentium3 pentium4
%define do_mmx 1
%else
%define do_mmx 0
%endif
%ifarch i686 athlon pentium4
%define do_sse2 1
%else
%define do_sse2 0
%endif
%ifarch i586 i686
%define do_mmxfb 1
%define optmmxfb -DCPU_FALLBACK=1
%else
%define do_mmxfb 0
%undefine optmmxfb
%endif
%ifarch i686 athlon
%define do_ssefb 1
%define optssefb -DCPU_FALLBACK=1
%else
%define do_ssefb 0
%define optssefb %{nil}
%endif
%endif

Summary:	Password cracker
Summary(pl.UTF-8):	Łamacz haseł
Name:		john
Version:	1.8.0
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://www.openwall.com/john/j/%{name}-%{version}.tar.xz
# Source0-md5:	a4086df68f51778782777e60407f1869
Source1:	http://www.openwall.com/john/j/%{name}-%{version}-jumbo-1.tar.xz
# Source1-md5:	1d6b22ec41a12cdcd62ad6eae3e77345
Source2:	http://www.openwall.com/john/j/%{name}-extra-20130529.tar.xz
# Source2-md5:	bb191828e8cbfd5fe0779dff5d87d5f4
Patch0:		%{name}-mailer.patch
Patch1:		optflags.patch
URL:		http://www.openwall.com/john/
%{?with_jumbo:BuildRequires: openssl-devel >= 0.9.7}
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	words
%ifarch %{ix86} %{x8664}
%if %{with xop}
Requires:	cpuinfo(xop)
%endif
%if %{with xop} || %{with avx}
Requires:	cpuinfo(avx)
%endif
%if %{without jumbo}
%if %{do_sse2} && !%{do_ssefb}
Requires:	cpuinfo(sse2)
%endif
%endif
%endif
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
%setup -q -T %{?with_jumbo:-b1 -n %{name}-%{version}-jumbo-1} %{!?with_jumbo:-b0} -a2
%patch0 -p1
%{!?with_jumbo:%patch1 -p1}

mv john-extra-*/*.chr run

%{__rm} doc/INSTALL

%build
cd src

%if %{with jumbo}
%configure
%{__make}
%else
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

%if %{do_ssefb}
%{__make} linux-x86-mmx \
	CC="%{__cc}" \
	OPTFLAGS="%{rpmcflags} -include defs.h %{?optmmxfb}"
mv ../run/john ../run/john-non-sse
%{__make} clean
%endif

TARG=generic
%ifarch %{x8664}
	TARG=linux-x86-64%{?with_xop:-xop}%{!?with_xop:%{?with_avx:-avx}}
%endif
%ifarch	%{ix86}
	%if %{with xop} || %{with avx}
		TARG=linux-x86%{?with_xop:-xop}%{!?with_xop:%{?with_avx:-avx}}
	%else
		%if %{do_sse2}
			TARG=linux-x86-sse2
		%else
			%if %{do_mmx}
				TARG=linux-x86-mmx
			%else
				TARG=linux-x86-any
			%endif
		%endif
	%endif
%endif
%ifarch ppc
	TARG=linux-ppc32%{?with_altivec:-altivec}
%endif
%ifarch ppc64
	TARG=linux-ppc64%{?with_altivec:-altivec}
%endif
%ifarch alpha
	TARG=linux-alpha
%endif
%ifarch ia64
	TARG=linux-ia64
%endif
%ifarch sparc sparcv9
	TARG=linux-sparc
%endif

%{__make} $TARG \
	CC="%{__cc}" \
	OPTFLAGS='%{rpmcflags} -include defs.h %{?optmmxfb}'
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/john}
cp -a run/{*.conf,*.chr,*.lst} $RPM_BUILD_ROOT%{_datadir}/john
install -p run/john $RPM_BUILD_ROOT%{_bindir}

%if %{do_mmxfb}
install -D -p run/john-non-mmx $RPM_BUILD_ROOT%{_libdir}/john/john-non-mmx
%endif
%if %{do_ssefb}
install -D -p run/john-non-sse $RPM_BUILD_ROOT%{_libdir}/john/john-non-sse
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
%if %{do_mmxfb} || %{do_ssefb}
%dir %{_libdir}/john
%if %{do_mmxfb}
%attr(755,root,root) %{_libdir}/john/john-non-mmx
%endif
%if %{do_ssefb}
%attr(755,root,root) %{_libdir}/john/john-non-sse
%endif
%endif
%{_datadir}/john
