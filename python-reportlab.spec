%global cmapdir %(echo `rpm -qls ghostscript | grep CMap | awk '{print $2}'`)

Name:             python-reportlab
Version:          3.4.0
Release:          13
Summary:          ReportLab library to create PDF documents and graphic
License:          BSD
URL:              https://www.reportlab.com/
Source0:          https://pypi.python.org/packages/source/r/reportlab/reportlab-%{version}.tar.gz
Patch0001:        0fbf25e4857423f6a38ca7f5aeee1c84acaa3fc1.patch
Patch0002:        CVE-2019-17626.patch

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

%build
CFLAGS="%{optflags}" %py3_build

PYTHONPATH="`pwd`/`ls -d build/lib*`" %{__python3} docs/genAll.py

%install
%py3_install

%check
%{__python3} setup.py tests

%files -n python3-reportlab
%doc README.txt CHANGES.md
%license LICENSE.txt
%{python3_sitearch}/{reportlab/,reportlab-%{version}-py%{python3_version}.egg-info}

%files help
%doc demos/ tools/

%changelog
* Wed Jul 21 2021 yaoxin <yaoxin30@huawei.com> - 3.4.0-13
- Fix CVE-2019-17626

* Mon May 31 2021 huanghaitao <huanghaitao8@huawei.com> - 3.4.0-12
- Completing build dependencies

* Fri 11 Sep 2020 wangyue<wangyue92@huawei.com> - 3.4.0-11
- Remove python2-reportlab

* Mon Mar 02 2020 Jiangping Hu <hujp1985@foxmail.com> - 3.4.0-10
- Package init
