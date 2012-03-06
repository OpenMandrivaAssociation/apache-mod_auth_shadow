#Module-Specific definitions
%define apache_version 2.4.0
%define mod_name mod_auth_shadow
%define load_order 183

Summary:	Shadow password authentication for the apache web server
Name:		apache-%{mod_name}
Version:	2.3
Release:	4
Group:		System/Servers
License:	GPL
URL:		http://mod-auth-shadow.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/mod-auth-shadow/%{mod_name}-%{version}.tar.gz
Patch0:		%{mod_name}-2.1-register.diff
Patch1:		%{mod_name}-2.1-makefile.diff
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
Epoch:		1

%description
mod_auth_shadow is an apache module which authenticates against the /etc/shadow
file. You may use this module with a mode 400 root:root /etc/shadow file, while
your web daemons are running under a non-privileged user.

%prep

%setup -q -n %{mod_name}_%{version}
%patch0 -p0
%patch1 -p0

%build
%serverbuild

export PATH="$PATH:/usr/sbin"
%make CFLAGS="$CFLAGS" APXS="%{_bindir}/apxs" -f makefile

%install

install -d %{buildroot}%{_libdir}/apache
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache/

cat > %{buildroot}%{_sysconfdir}/httpd/modules.d/%{load_order}_%{mod_name}.conf << EOF
LoadModule auth_shadow_module %{_libdir}/apache/%{mod_name}.so
EOF

install -d %{buildroot}%{_sbindir}
install -m0755 validate %{buildroot}%{_sbindir}/

%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :

%postun
if [ "$1" = "0" ]; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%files
%doc CHANGES INSTALL README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/*.conf
%attr(0755,root,root) %{_libdir}/apache/*.so
%attr(4755,root,root) %{_sbindir}/validate
