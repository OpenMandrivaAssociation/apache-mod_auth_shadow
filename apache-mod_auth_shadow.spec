#Module-Specific definitions
%define apache_version 2.2.4
%define mod_name mod_auth_shadow
%define mod_conf 83_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Shadow password authentication for the apache web server
Name:		apache-%{mod_name}
Version:	2.2
Release:	%mkrel 14
Group:		System/Servers
License:	GPL
URL:		http://mod-auth-shadow.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/mod-auth-shadow/%{mod_name}-%{version}.tar.bz2
Source1:	%{mod_conf}
Patch0:		%{mod_name}-2.1-register.diff
Patch1:		%{mod_name}-2.1-makefile.diff
Patch2:		mod_auth_shadow-2.2-CVE-2010-1151.patch
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

%setup -q -n %{mod_name}-%{version}
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .CVE-2010-1151

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
