#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
%bcond_with	tests	# do not perform "make test"

%define 	module	sleekxmpp
Summary:	Flexible XMPP client/component/server library for Python
Name:		python-%{module}
Version:	1.1.11
Release:	8
License:	MIT
Group:		Libraries/Python
Source0:	http://pypi.python.org/packages/source/s/sleekxmpp/%{module}-%{version}.tar.gz
# Source0-md5:	95f847b64fb84483acfadce425fe42cf
URL:		https://github.com/fritzy/SleekXMPP
BuildRequires:	python-distribute
BuildRequires:	python-modules
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.710
%if %{with apidocs}
BuildRequires:	sphinx-pdg
%endif
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

%package apidoc
Summary:	%{module} API documentation
Summary(pl.UTF-8):	Dokumentacja API %{module}
Group:		Documentation

%description apidoc
API documentation for %{module}.

%description apidoc -l pl.UTF-8
Dokumentacja API %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build %{?with_tests:test}
%py3_build %{?with_tests:test}

%if %{with apidocs}
%{__make} -C docs html
# remove the sphinx-build leftovers
%{__rm} docs/_build/html/.buildinfo
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/sleekxmpp/test
%py_postclean

install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python}\1,' \
      $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}/*/*.py \
      $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}/*.py

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/sleekxmpp/test

install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python3}\1,' \
      $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/*/*.py \
      $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}/*.py

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
%{_examplesdir}/python-%{module}-%{version}

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
%{_examplesdir}/python3-%{module}-%{version}

%files apidoc
%defattr(644,root,root,755)
%doc docs/_build/html/*
