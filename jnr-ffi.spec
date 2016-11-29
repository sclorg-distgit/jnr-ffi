%{?scl:%scl_package jnr-ffi}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 1

Name:     %{?scl_prefix}jnr-ffi
Version:  2.0.6
Release:  1.%{baserelease}%{?dist}
Summary:  Java Abstracted Foreign Function Layer
License:  ASL 2.0
URL:      http://github.com/jnr/%{pkg_name}/
Source0:  https://github.com/jnr/%{pkg_name}/archive/%{version}.tar.gz

BuildRequires:  %{?scl_prefix_maven}maven-local
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
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -n %{pkg_name}-%{version} -q

# remove all builtin jars
find -name '*.jar' -o -name '*.class' -exec rm -f '{}' \;

# don't fail on unused parameters... (TODO: send patch upstream)
sed -i 's|-Werror||' libtest/GNUmakefile

%mvn_file :{*} %{pkg_name}/@1 @1
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_build -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%dir %{_javadir}/%{pkg_name}
%doc LICENSE

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Fri Jul 22 2016 Mat Booth <mat.booth@redhat.com> - 2.0.6-1.1
- Auto SCL-ise package for rh-eclipse46 collection

* Fri Feb 5 2016 Alexander Kurtakov <akurtako@redhat.com> 2.0.6-1
- Update to upstream 2.0.6 release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 23 2015 Alexander Kurtakov <akurtako@redhat.com> 2.0.4-1
- Update to upstream 2.0.4 and drop unneeded osgification patch/source.

* Tue Jun 23 2015 Roland Grunberg <rgrunber@redhat.com> - 2.0.3-4
- Add missing Import-Package statements to manifest.

* Wed Jun 17 2015 Jeff Johnston <jjohnstn@redhat.com> - 2.0.3-3
- Add proper MANIFEST.MF.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Alexander Kurtakov <akurtako@redhat.com> 2.0.3-1
- Update to upstream 2.0.3.
- Skip tests.

* Thu Apr 30 2015 Alexander Kurtakov <akurtako@redhat.com> 2.0.2-1
- Update to upstream 2.0.2.

* Thu Feb 19 2015 Michal Srb <msrb@redhat.com> - 2.0.1-3
- Skip tests on arm

* Wed Feb 18 2015 Michal Srb <msrb@redhat.com> - 2.0.1-2
- Build with jffi-native

* Mon Jan 05 2015 Mo Morsi <mmorsi@redhat.com> - 2.0.1-1
- Update to 2.0.1

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 25 2013 Michal Srb <msrb@redhat.com> - 0.7.10-4
- Adapt to current guidelines
- Remove unneeded patch
- Enable tests
- Fix BR

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.10-2
- Depend on objectweb-asm4, not objectweb-asm.

* Tue Feb 05 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.10-1
- Update to version 0.7.10.
- Switch from ant to maven.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-3
- more updates to conform to fedora guidelines

* Wed Aug 10 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-2
- updated to conform to fedora guidelines

* Tue Aug 02 2011 Mo Morsi <mmorsi@redhat.com> - 0.5.10-1
- initial package