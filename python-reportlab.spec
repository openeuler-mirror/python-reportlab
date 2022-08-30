%global cmapdir %(echo `rpm -qls ghostscript | grep CMap | awk '{print $2}'`)

%bcond_without tests

Name:             python-reportlab
Version:          3.6.10
Release:          1
Summary:          ReportLab library to create PDF documents and graphic
License:          BSD-3-Clause
URL:              https://www.reportlab.com/
Source0:          https://pypi.python.org/packages/source/r/reportlab/reportlab-%{version}.tar.gz
BuildRequires:    libart_lgpl-devel freetype-devel

%description
The ReportLab Toolkit. An Open Source Python library for generating PDFs and graphics.

%package -n     python3-reportlab
Summary:        ReportLab library to create PDF documents and graphic
BuildRequires:  python3-devel python3-pillow gcc
Requires:       dejavu-sans-fonts python3-pillow
%{?python_provide:%python_provide python3-reportlab}

%description -n python3-reportlab
The ReportLab Toolkit. An Open Source Python library for generating PDFs and graphics.

%package        help
Summary:        Documentation for python-reportlab
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Obsoletes:      %{name}-doc < %{version}-%{release} %{name}-docs < %{version}-%{release}

%description    help
Help documents for ReportLab.

%prep
%autosetup -n reportlab-%{version} -p1

find src -name '*.py' | xargs sed -i -e '/^#!\//d'

sed -i '/\~\/\.local\/share\/fonts\/CMap/i''\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ '\'"%{cmapdir}"\''\,' \
src/reportlab/rl_settings.py

rm -rf src/reportlab.egg-info

rm -rf src/rl_addons/renderPM/libart_lgpl

%build
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS} -Isrc/rl_addons/renderPM -I%{_includedir}/libart-2.0}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}"\
  %{__python3} setup.py --use-system-libart --no-download-t1-files build --executable="%{__python3} -s"

%install
CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS} -Isrc/rl_addons/renderPM -I%{_includedir}/libart-2.0}" LDFLAGS="${LDFLAGS:-${RPM_LD_FLAGS}}"\
  %{__python3} setup.py --use-system-libart --no-download-t1-files install -O1 --skip-build --root ${RPM_BUILD_ROOT}

%if %{with tests}
%check
# Tests need in-build compiled Python modules to be executed
# Tests pre-generate userguide PDF
cp -a build/lib.%{python3_platform}-%{python3_version}/reportlab tests/
cp -a build/lib.%{python3_platform}-%{python3_version}/reportlab docs/
cp -a build/lib.%{python3_platform}-%{python3_version}/reportlab docs/userguide/
%{__python3} setup.py tests
%endif

%files -n python3-reportlab
%doc README.txt CHANGES.md
%license LICENSE.txt
%{python3_sitearch}/{reportlab/,reportlab-%{version}-py%{python3_version}.egg-info}

%files help
%doc demos/ tools/

%changelog
* Mon Aug 29 2022 yaoxin <yaoxin30@h-partners.com> - 3.6.10-1
- Upgrade to 3.6.10 to fix CVE-2020-28463

* Thu Jul 22 2021 yaoxin <yaoxin30@huawei.com> - 3.4.0-13
- Fix CVE-2019-17626

* Thu Apr 22 2021 Senlin Xia <xiasenlin1@huawei.com> - 3.4.0-12
- Remove python2-reportlab for no more buildrequire: python2-pillow

* Fri Aug 21 2020 shixuantong <shixuantong@huawei.com> - 3.4.0-11
- add release version for rebuild

* Mon Mar 02 2020 Jiangping Hu <hujp1985@foxmail.com> - 3.4.0-10
- Package init
