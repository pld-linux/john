Summary:	Password cracker
Summary(pl):	£amacz hase³
Name:		john
Version:	1.6
Release:	3
Copyright:	GPL
Group:		Utilities/System
Group(pl):	Narzêdzia/System
URL:		http://www.false.com/security/john/
Source:		%{name}-%{version}.tar.gz
Patch0:		%{name}-%{version}.PLD.diff
Patch1:		%{name}-%{version}.ini.diff
Patch2:		%{name}-%{version}.makefile.diff
Buildroot:	/tmp/%{name}-%{version}-root

%description
John the Ripper is a password cracker, currently available for UNIX, DOS,
WinNT/Win95. Its primary purpose is to detect weak UNIX passwords. It has
been tested with Linux x86/Alpha/SPARC, FreeBSD x86, OpenBSD x86, Solaris
2.x SPARC and x86, Digital UNIX, AIX, HP-UX, and IRIX.
  
%description -l pl
John The Ripper jest "³amaczem" hase³ dostêpnym dla systemów UNIX, DOS,
WinNT/Win95. G³ównym jego zadaniem jest wykrywanie "s³abych" hase³.
  
%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cd src
# Hmm. I don't know what is in /proc/cpuinfo on other processors than Intel MMX
if grep -q "MMX" /proc/cpuinfo; then
	make OPT="$RPM_OPT_FLAGS" linux-x86-mmx-elf
elif grep -q "K6" /proc/cpuinfo; then
	make OPT="$RPM_OPT_FLAGS" linux-x86-k6-elf
elif grep -q "Alpha" /proc/cpuinfo; then
	make OPT="$RPM_OPT_FLAGS" linux-alpha
elif grep -q "SPARC" /proc/cpuinfo; then
	make OPT="$RPM_OPT_FLAGS" linux-sparc
else
	make OPT="$RPM_OPT_FLAGS" linux-x86-any-elf
fi
	
%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr/{bin,lib/john}
install run/*.chr $RPM_BUILD_ROOT%{_libdir}/john
install run/john.ini $RPM_BUILD_ROOT%{_libdir}/john
install run/john $RPM_BUILD_ROOT%{_bindir}

gzip -9nf doc/* run/mailer

cd $RPM_BUILD_ROOT%{_bindir}
ln -s john unafs; ln -s john unique; ln -s john unshadow

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc doc/* run/mailer.gz
%attr(755,root,root) %{_bindir}/*

%dir %{_libdir}/john
%{_libdir}/john/*
