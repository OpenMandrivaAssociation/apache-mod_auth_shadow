#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_auth_shadow
%define mod_conf 83_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Shadow password authentication for the apache web server
Name:		apache-%{mod_name}
Version:	2.3
Release:	3
Group:		System/Servers
License:	GPL
URL:		http://mod-auth-shadow.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/mod-auth-shadow/%{mod_name}-%{version}.tar.gz
Source1:	%{mod_conf}
Patch0:		%{mod_name}-2.1-register.diff
Patch1:		%{mod_name}-2.1-makefile.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mod_auth_shadow is an apache module which authenticates against the /etc/shadow
file. You may use this module with a mode 400 root:root /etc/shadow file, while
your web daemons are running under a non-privileged user.

%prep

%setup -q -n %{mod_name}_%{version}
%patch0 -p0
%patch1 -p0

cp %{SOURCE1} %{mod_conf}

%build
%serverbuild

export PATH="$PATH:/usr/sbin"
%make CFLAGS="$CFLAGS" -f makefile

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_sbindir}
install -m0755 validate %{buildroot}%{_sbindir}/

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%attr(4755,root,root) %{_sbindir}/validate


%changelog
* Sat May 21 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.3-1mdv2011.0
+ Revision: 676944
- 2.3

* Sat May 14 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-16
+ Revision: 674424
- rebuild

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-15
+ Revision: 662772
- mass rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-14mdv2011.0
+ Revision: 588278
- rebuild

* Sun Apr 18 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-13mdv2010.1
+ Revision: 536370
- P2: security fix for CVE-2010-1151 (redhat)

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-12mdv2010.1
+ Revision: 515833
- rebuilt for apache-2.2.15

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-11mdv2010.0
+ Revision: 451697
- rebuild

* Fri Jul 31 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-10mdv2010.0
+ Revision: 405135
- rebuild

* Wed Jan 07 2009 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-9mdv2009.1
+ Revision: 326482
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-8mdv2009.0
+ Revision: 235638
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-7mdv2009.0
+ Revision: 215288
- rebuild

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-6mdv2008.1
+ Revision: 181437
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1:2.2-5mdv2008.1
+ Revision: 148463
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-4mdv2008.0
+ Revision: 82358
- rebuild

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-3mdv2008.0
+ Revision: 64318
- use the new %%serverbuild macro

* Wed Jun 13 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-2mdv2008.0
+ Revision: 38410
- rebuild

* Wed May 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.2-1mdv2008.0
+ Revision: 27163
- 2.2


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1-4mdv2007.1
+ Revision: 140580
- rebuild

* Tue Feb 27 2007 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-3mdv2007.1
+ Revision: 126608
- general cleanups

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-2mdv2007.0
+ Revision: 79243
- Import apache-mod_auth_shadow

* Sun Jul 30 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-2mdv2007.0
- rebuild

* Wed Mar 29 2006 Oden Eriksson <oeriksson@mandriva.com> 1:2.1-1mdk
- 2.1 (addresses CAN-2005-2963)

* Mon Dec 12 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0-4mdk
- rebuilt against apache-2.2.0

* Sun Oct 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-3mdk
- security update for CAN-2005-2963 (P2)

* Mon Oct 17 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-2mdk
- rebuilt against correct apr-0.9.7

* Sat Oct 15 2005 Oden Eriksson <oeriksson@mandriva.com> 1:2.0-1mdk
- rebuilt for apache-2.0.55

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-4mdk
- added another work around for a rpm bug

* Sat Jul 30 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-3mdk
- added a work around for a rpm bug, "Requires(foo,bar)" don't work

* Fri Jul 01 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-2mdk
- drop the uid patch as proposed by Joshua Kugler

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 2.0.54_2.0-1mdk
- rename the package
- the conf.d directory is renamed to modules.d
- use new rpm-4.4.x pre,post magic

* Thu Mar 17 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-6mdk
- use the %%mkrel macro

* Sun Feb 27 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-5mdk
- fix %%post and %%postun to prevent double restarts

* Wed Feb 16 2005 Stefan van der Eijk <stefan@eijk.nu> 2.0.53_2.0-4mdk
- fix bug #6574

* Wed Feb 16 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-3mdk
- fix deps

* Tue Feb 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-2mdk
- spec file cleanups, remove the ADVX-build stuff

* Tue Feb 08 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.53_2.0-1mdk
- rebuilt for apache 2.0.53

* Wed Sep 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.52_2.0-1mdk
- built for apache 2.0.52

* Fri Sep 17 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.51_2.0-1mdk
- built for apache 2.0.51

* Wed Aug 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.0-3mdk
- rebuilt

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.0-2mdk
- remove redundant provides

* Thu Jul 01 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.0.50_2.0-1mdk
- built for apache 2.0.50

* Sat Jun 12 2004 Oden Eriksson <oden.eriksson@kvikkjokk.net> 2.0.49_2.0-1mdk
- built for apache 2.0.49
- added P2

