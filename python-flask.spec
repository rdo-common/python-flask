%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global srcname Flask

Name:           python-flask
Version:        0.7.2
Release:        2%{?dist}
Summary:        A micro-framework for Python based on Werkzeug, Jinja 2 and good intentions

Group:          Development/Libraries
License:        BSD
URL:            http://flask.pocoo.org/
Source0:        http://pypi.python.org/packages/source/F/Flask/%{srcname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools-devel
BuildRequires:  python-jinja2 python-werkzeug python-sphinx

Requires:       python-jinja2 python-werkzeug

%description
Flask is called a “micro-framework” because the idea to keep the core
simple but extensible. There is no database abstraction layer, no form
validation or anything else where different libraries already exist
that can handle that. However Flask knows the concept of extensions
that can add this functionality into your application as if it was
implemented in Flask itself. There are currently extensions for object
relational mappers, form validation, upload handling, various open
authentication technologies and more.



%package doc
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}


%description doc
Documentation and examples for %{name}.

%prep
%setup -q -n %{srcname}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Need to install flask in the setuptools "develop" mode to build docs
# The BuildRequires on Werkzeug, Jinja2 and Sphinx is due to this as well.
export PYTHONPATH=$RPM_BUILD_ROOT%{python_sitelib}
%{__python} setup.py develop --install-dir $RPM_BUILD_ROOT%{python_sitelib}
make -C docs html

rm -rf $RPM_BUILD_ROOT%{python_sitelib}/site.py
rm -rf $RPM_BUILD_ROOT%{python_sitelib}/site.py[co]
rm -rf $RPM_BUILD_ROOT%{python_sitelib}/easy-install.pth
rm -rf docs/_build/html/.buildinfo
rm -rf examples/minitwit/*.pyc
rm -rf examples/flaskr/*.pyc
rm -rf examples/jqueryexample/*.pyc

%check
%{__python} setup.py test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE PKG-INFO CHANGES README
%{python_sitelib}/*.egg-info
%{python_sitelib}/*.egg-link
%{python_sitelib}/flask

%files doc
%defattr(-,root,root,-)
%doc docs/_build/html examples

%changelog
* Wed Nov 16 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.7.2-2
- don't own easy-install.pth

* Fri Jul 22 2011 Steve Milner <smilner@fedoraproject.org> - 0.7.2-1
- update for upstream release

* Thu Feb 24 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.6.1-2
- fix rpmlint spelling warning
- BR python2-devel rather than python-devel
- run test suite in check

* Tue Feb 22 2011 Dan Young <dyoung@mesd.k12.or.us> - 0.6.1-1
- Initial package
