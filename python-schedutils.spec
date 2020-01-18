%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%{!?python_ver: %define python_ver %(%{__python} -c "import sys ; print sys.version[:3]")}

Summary: Linux scheduler python bindings
Name: python-schedutils
Version: 0.4
Release: 6%{?dist}
License: GPLv2
URL: http://git.kernel.org/?p=linux/kernel/git/acme/python-schedutils.git
Source: http://userweb.kernel.org/~acme/python-schedutils/%{name}-%{version}.tar.bz2
Group: System Environment/Libraries
BuildRequires: python-devel
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: python-schedutils-Correct-typos-in-usage-messages.patch
Patch2: python-schedutils-Add-man-pages-for-pchrt-and-ptasks.patch
Patch3: Update-spec-file-to-install-man-pages-for-pchrt-and-.patch
Patch4: schedutils.c-added-support-for-SCHED_DEADLINE.patch
Patch5: python-schedutils-Update-URL-in-python-schedutils.sp.patch

%description
Python interface for the Linux scheduler sched_{get,set}{affinity,scheduler}
functions and friends.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_bindir}
cp -p pchrt.py %{buildroot}%{_bindir}/pchrt
cp -p ptaskset.py %{buildroot}%{_bindir}/ptaskset
mkdir -p %{buildroot}%{_mandir}/man1
gzip -c pchrt.1 > %{buildroot}%{_mandir}/man1/pchrt.1.gz
gzip -c ptaskset.1 > %{buildroot}%{_mandir}/man1/ptaskset.1.gz

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/pchrt
%{_bindir}/ptaskset
%{python_sitearch}/schedutils.so
%if "%{python_ver}" >= "2.5"
%{python_sitearch}/*.egg-info
%endif
%{_mandir}/man1/pchrt.1.gz
%{_mandir}/man1/ptaskset.1.gz

%changelog
* Tue Jul 05 2016 John Kacur <jkacur@redhat.com> - 0.4-6
- python-schedutils-Update-URL-in-python-schedutils.sp.patch
- schedutils.c-added-support-for-SCHED_DEADLINE.patch
Resolves: rhbz#1298388

* Tue May 10 2016 John Kacur <jkacur@redhat.com> - 0.4-5
- Add man pages for pchrt and ptaskset
- Fix and update usage messages for pchrt and ptaskset
- Resolves:rhbz#948381

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.4-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.4-3
- Mass rebuild 2013-12-27

* Thu Aug 22 2013 John Kacur <jkacur@redhat.com> - 0.4-1
- Rebuilding for rhel7.0

* Mon Aug  1 2011 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.4-1
- New upstream release.

* Tue May 17 2011 Clark Williams <williams@redhat.com> - 0.3-1
- reworked get_affinity() and set_affinity() to use dynamic CPU_* macros

* Thu Aug 28 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.2-2
- Fix build and install sections as suggested by the fedora rewiewer
  (BZ #460387)

* Wed Aug 27 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.2-1
- Add get_priority_{min,max} methods
- Add constants for SCHED_{BATCH,FIFO,OTHER,RR}
- Implement get_priority method
- Add pchrt utility for testing the bindings, chrt clone
- Add ptaskset utility for testing the bindings, taskset clone

* Tue Jun 10 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-3
- add dist to the release tag

* Wed Dec 19 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-2
- First build into rhel5-rt

* Wed Dec 19 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 0.1-1
- Initial package
