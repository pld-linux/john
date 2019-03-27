#
# TODO:
# - investigate build-time vs runtime CPU features detection
#
# Conditional build:
%bcond_without	opencl		# OpenCL support
%bcond_without	openmp		# OpenMP support

%define		snap		20190327
%define		githash		4840892d68d14ad4a28f3e6f8c2e2941e9c0a2ad
%define		rel	1

Summary:	Password cracker
Summary(pl.UTF-8):	Łamacz haseł
Name:		john
Version:	1.8.0
Release:	2.%{snap}.%{rel}
License:	GPL v2
Group:		Applications/System
Source0:	https://github.com/magnumripper/JohnTheRipper/archive/%{githash}/%{name}-%{snap}.tar.gz
# Source0-md5:	0338a3184bf5598a5b027f3ee929ba24
Patch0:		%{name}-mailer.patch
Patch1:		jumbo-optflags.patch
Patch4:		%{name}-x32.patch
URL:		http://www.openwall.com/john/
%{?with_opencl:BuildRequires:	OpenCL-devel}
BuildRequires:	autoconf >= 2.69
BuildRequires:	bzip2-devel
%{?with_openmp:BuildRequires:	gcc >= 6:4.2}
BuildRequires:	gmp-devel
%{?with_openmp:BuildRequires:	libgomp-devel}
BuildRequires:	rpmbuild(macros) >= 1.213
BuildRequires:	tar >= 1:1.22
# for SIPdump and vncpcap2john binaries, which are not packaged
#BuildRequires:	libpcap-devel
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	pkgconfig
BuildRequires:	yasm
BuildRequires:	zlib-devel
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
%setup -q -n JohnTheRipper-%{githash}
%patch0 -p1
%patch1 -p1
%ifarch x32
%patch4 -p1
%endif

%build
cd src
%{__autoconf}

%ifarch x32
ax_intel_x32=yes \
%endif
%configure \
	%{!?with_opencl:--disable-opencl} \
	%{!?with_openmp:--disable-openmp}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/john}
cp -a run/{*.conf,*.chr,*.lst} $RPM_BUILD_ROOT%{_datadir}/john
install -p run/john $RPM_BUILD_ROOT%{_bindir}

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
%{_datadir}/john
