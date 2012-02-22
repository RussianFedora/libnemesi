%define git 20110215

Summary: RTSP/RTP client library
Name: libnemesi
Version: 0.7.0
Release: 0.1.%{?git}git%{?dist}.R
License: LGPLv2+
Group: Development/Libraries
%if %{?git:1}0
# http://cgit.lscube.org/cgit.cgi/libnemesi/snapshot/libnemesi-0.6.tar.gz
Source0: libnemesi-%{version}-%{git}.tar.bz2
%else
Source0: http://www.lscube.org/files/downloads/libnemesi/%{name}-%{version}-rc2.tar.bz2
%endif
URL: http://www.lscube.org/projects/libnemesi
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: lksctp-tools-devel
BuildRequires: netembryo-devel >= 0.1.1


%description
Libnemesi let you add multimedia streaming playback in your applications in
a quick and straightforward way. This software, derived from the experience
matured with NeMeSi is fully compliant with IETF's standards for real-time
streaming of multimedia contents over Internet. libnemesi implements RTSP –
Real-Time Streaming Protocol (RFC2326) and RTP/RTCP – Real-Time Transport
Protocol/RTP Control Protocol (RFC3550) supporting the RTP Profile for
Audio and Video Conferences with Minimal Control (RFC3551).

The library provides two different API:

    * high level: the simplest abstraction to get the demuxed streams out
      of a resource uri
    * low level: provides access to all the rtp, rtcp, rtsp primitives in
      order to develop advanced applications.

Libnemesi leverages the netembryo network support and provides hooks to
register custom depacketizers (rtp parsers) to have a good compromises
between ease of use and flexibility.

%package devel
Summary: Nemesi development library and headers
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: netembryo-devel >= 0.1.1
Requires: pkgconfig

%description devel
The libnemesi-devel package contains the header files and some
documentation needed to develop application with libnemesi.

%package tools
Summary: Simple dump/info programs that use libnemesi
Group: Applications/Multimedia

%description tools
Simple programs that use libnemesi to show network streams' information
and dump them.

%prep
%setup -q

#Bug in upstream configure option
sed -i -e 's/-Werror=return-type//g' configure configure.ac

%build
%configure \
 --disable-dependency-tracking \
 --disable-static \
 --enable-errors=none \
 --program-prefix=nemesi_ \

%if %{!?git:1}0
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} DESTDIR=%{buildroot} install
%{__rm} %{buildroot}%{_libdir}/libnemesi.la

#Remove installed docs
%{__rm} -r %{buildroot}/%{_docdir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{_libdir}/libnemesi.so.*

%files devel
%defattr(-,root,root,-)
%doc CodingStyle
%{_includedir}/nemesi
%{_libdir}/libnemesi.so
%{_libdir}/pkgconfig/libnemesi.pc

%files tools
%defattr(-,root,root,-)
%{_bindir}/nemesi_dump_info
%{_bindir}/nemesi_dump_stream
%{_bindir}/nemesi_loop_stream

%changelog
* Wed Feb 16 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.0-0.1.20110215git
- Update to lastest git

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.9-0.2.20090422git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 25 2009 Dominik Mierzejewski <rpm at greysector.net> 0.6.9-0.1.20090422git
- updated to latest stable branch snapshot
- dropped obsolete patch

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-0.6.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Feb 27 2009 Dominik Mierzejewski <rpm at greysector.net> 0.6.4-0.5.rc2
- fix source and project URLs

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.4-0.4.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 21 2008 Dominik Mierzejewski <rpm at greysector.net> 0.6.4-0.3.rc2
- work around linking problem on ppc64 (bug #433845)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.6.4-0.2.rc2
- Autorebuild for GCC 4.3

* Fri Dec 28 2007 Dominik Mierzejewski <rpm at greysector.net> 0.6.4-0.1.rc2
- update to 0.6.4-rc2
- fixes multiple buffer overflow vulnerabilities (bug #426905)
- kill rpaths

* Sun Nov 11 2007 Dominik Mierzejewski <rpm at greysector.net> 0.6.3-0.2.20071030git
- added missing Requires: netembryo-devel to -devel subpackage

* Thu Nov 01 2007 Dominik Mierzejewski <rpm at greysector.net> 0.6.3-0.1.20071030git
- updated to latest git snapshot (requested by upstream)
- fixed changelog version
- capitalized -devel Summary
- use disttag

* Thu Oct 11 2007 Dominik Mierzejewski <rpm at greysector.net> 0.6.2-0.1
- latest git snapshot (required by MPlayer-1.0rc2)
- specfile adapted to current buildsystem

* Thu Jan 11 2007 Dominik Mierzejewski <rpm at greysector.net> 0.6.0-1
- initial release based on upstream RPM
