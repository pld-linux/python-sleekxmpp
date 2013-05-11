#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	sleekxmpp
Summary:	Flexible XMPP client/component/server library for Python
Name:		python-%{module}
Version:	1.1.11
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/s/sleekxmpp/%{module}-%{version}.tar.gz
# Source0-md5:	95f847b64fb84483acfadce425fe42cf
URL:		https://github.com/fritzy/SleekXMPP
BuildRequires:	python-devel
BuildRequires:	python3-devel
BuildRequires:	rpmbuild(macros) >= 1.219
%if %{with tests}
BuildRequires:	gnupg
%endif
Requires:	python-dns
Requires:	python-pyasn1
Requires:	python-pyasn1_modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SleekXMPP is a flexible XMPP library for python that allows you to
create clients, components or servers for the XMPP protocol. Plug-ins
can be create to cover every current or future XEP.

%package -n python3-sleekxmpp
Summary:	Flexible XMPP client/component/server library for Python
Group:		Libraries/Python
Requires:	python3-dns

%description -n python3-sleekxmpp
SleekXMPP is a flexible XMPP library for python that allows you to
create clients, components or servers for the XMPP protocol. Plug-ins
can be create to cover every current or future XEP.

%prep
%setup -q -n %{module}-%{version}
set -- *
install -d py3
cp -a "$@" py3

%build
%{__python} setup.py build
cd py3
%{__python3} setup.py build
cd ..

%if %{with tests}
%{__python} testall.py
cd py3
%{__python3} testall.py
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%py_postclean

cd py3
%{__python3} setup.py install \
	--optimize=2 \
	--skip-build \
	--root $RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/sleekxmpp/test
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/sleekxmpp/test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py_sitescriptdir}/sleekxmpp
%{py_sitescriptdir}/sleekxmpp/*.py[co]
%{py_sitescriptdir}/sleekxmpp-%{version}-*.egg-info
%{py_sitescriptdir}/sleekxmpp/features
%{py_sitescriptdir}/sleekxmpp/plugins
%{py_sitescriptdir}/sleekxmpp/roster
%{py_sitescriptdir}/sleekxmpp/stanza
%{py_sitescriptdir}/sleekxmpp/thirdparty
%{py_sitescriptdir}/sleekxmpp/util
%{py_sitescriptdir}/sleekxmpp/xmlstream

%files -n python3-sleekxmpp
%defattr(644,root,root,755)
%doc LICENSE README.rst
%dir %{py3_sitescriptdir}/sleekxmpp
%{py3_sitescriptdir}/sleekxmpp/*.py
%{py3_sitescriptdir}/sleekxmpp/__pycache__
%{py3_sitescriptdir}/sleekxmpp/features
%{py3_sitescriptdir}/sleekxmpp/plugins
%{py3_sitescriptdir}/sleekxmpp/roster
%{py3_sitescriptdir}/sleekxmpp/stanza
%{py3_sitescriptdir}/sleekxmpp/thirdparty
%{py3_sitescriptdir}/sleekxmpp/util
%{py3_sitescriptdir}/sleekxmpp/xmlstream
%{py3_sitescriptdir}/sleekxmpp-%{version}-*.egg-info
