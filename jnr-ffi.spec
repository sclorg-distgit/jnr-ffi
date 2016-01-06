%{?scl:%scl_package jnr-ffi}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

Name:     %{?scl_prefix}jnr-ffi
Version:  2.0.3
Release:  4.2%{?dist}
Summary:  Java Abstracted Foreign Function Layer
License:  ASL 2.0
URL:      http://github.com/jnr/%{pkg_name}/
Source0:  https://github.com/jnr/%{pkg_name}/archive/%{version}.tar.gz
Source1:  MANIFEST.MF
Patch0:   add-manifest.patch

BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}mvn(com.github.jnr:jffi)
BuildRequires:  %{?scl_prefix}mvn(com.github.jnr:jffi::native:)
BuildRequires:  %{?scl_prefix}mvn(com.github.jnr:jnr-x86asm)
BuildRequires:  %{?scl_prefix_java_common}mvn(junit:junit)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-antrun-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-release-plugin)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.ow2.asm:asm:5)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.ow2.asm:asm-analysis:5)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.ow2.asm:asm-commons:5)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.ow2.asm:asm-tree:5)
BuildRequires:  %{?scl_prefix_java_common}mvn(org.ow2.asm:asm-util:5)
BuildRequires:  %{?scl_prefix_maven}sonatype-oss-parent


BuildArch:     noarch

# don't obsolete/provide jaffl, gradle is using both jaffl and jnr-ffi...

%description
An abstracted interface to invoking native functions from java

%package javadoc
Summary:        Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
cp %{SOURCE1} .
sed -i -e's/@VERSION/%{version}/g' MANIFEST.MF
%patch0

# remove all builtin jars
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;

# don't fail on unused parameters... (TODO: send patch upstream)
sed -i 's|-Werror||' libtest/GNUmakefile

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_file :{*} %{pkg_name}/@1 @1
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Thu Aug 20 2015 Mat Booth <mat.booth@redhat.com> - 2.0.3-4.2
- Fix unowned directories

* Thu Jul 30 2015 Roland Grunberg <rgrunber@redhat.com> - 2.0.3-4.1
- Add missing Import-Package statements to manifest.

* Wed Jul 1 2015 akurtakov <akurtakov@localhost.localdomain> 2.0.3-2.1
- BR compat asm 5.x.

* Mon Jun 29 2015 Jeff Johnston <jjohnstn@redhat.com> - 2.0.3-2
- SCL-ize package.

* Mon Jun 29 2015 Jeff Johnston <jjohnstn@redhat.com> - 2.0.3-1
- Initial import from rawhide.
