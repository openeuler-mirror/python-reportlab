%global cmapdir %(echo `rpm -qls ghostscript | grep CMap | awk '{print $2}'`)

Name:             python-reportlab
Version:          3.4.0
Release:          11
Summary:          ReportLab library to create PDF documents and graphic
License:          BSD
URL:              https://www.reportlab.com/
Source0:          https://pypi.python.org/packages/source/r/reportlab/reportlab-%{version}.tar.gz
Patch0001:        0fbf25e4857423f6a38ca7f5aeee1c84acaa3fc1.patch

%description
The ReportLab Toolkit. An Open Source Python library for generating PDFs and graphics.

%package -n       python2-reportlab
Summary:          ReportLab library to create PDF documents and graphic
BuildRequires:    gcc freetype-devel ghostscript python2-devel python2-pillow libart_lgpl-devel
Requires:         dejavu-sans-fonts python2-pillow
%{?python_provide:%python_provide python2-reportlab}

%description -n python2-reportlab
The ReportLab Toolkit. An Open Source Python library for generating PDFs and graphics.

%package -n     python3-reportlab
Summary:        ReportLab library to create PDF documents and graphic
BuildRequires:  python3-devel python3-pillow
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

rm -rf %{py3dir}
cp -a . %{py3dir}
%build
CFLAGS="%{optflags}" %py2_build
pushd %{py3dir}
CFLAGS="%{optflags}" %py3_build
popd

PYTHONPATH="`pwd`/`ls -d build/lib*`" %{__python2} docs/genAll.py

%install
%py2_install
pushd %{py3dir}
%py3_install
popd

%check
%{__python2} setup.py tests
pushd %{py3dir}
%{__python3} setup.py tests
popd

%files -n python2-reportlab
%doc README.txt CHANGES.md
%license LICENSE.txt
%{python2_sitearch}/{reportlab/,reportlab-%{version}-py%{python2_version}.egg-info}
%exclude %{python2_sitearch}/reportlab/fonts

%files -n python3-reportlab
%doc README.txt CHANGES.md
%license LICENSE.txt
%{python3_sitearch}/{reportlab/,reportlab-%{version}-py%{python3_version}.egg-info}

%files help
%doc demos/ tools/

%changelog
* Fri Aug 21 2020 shixuantong <shixuantong@huawei.com> - 3.4.0-11
- add release version for rebuild

* Mon Mar 02 2020 Jiangping Hu <hujp1985@foxmail.com> - 3.4.0-10
- Package init
