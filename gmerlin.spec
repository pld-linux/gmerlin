# TODO: some plugins (like oa_jack,oa_pulse) to subpackages? (see dependencies in files)
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
%bcond_without	nmjedit		# nmjedit program
%bcond_with	esd		# EsounD support
%bcond_with	v4l1		# Video4Linux 1 support
#
Summary:	Set of multimedia libraries builded with an application suite
Summary(pl.UTF-8):	Zbiór bibliotek multimedialnych wraz z aplikacjami
Name:		gmerlin
Version:	1.2.0
Release:	15
License:	GPL v2+
Group:		Libraries
Source0:	https://downloads.sourceforge.net/gmerlin/%{name}-%{version}.tar.gz
# Source0-md5:	2f2a0880e738e71486f04c929ba067f4
Patch0:		%{name}-link.patch
Patch1:		%{name}-icons.patch
Patch2:		%{name}-info.patch
Patch3:		cdio.patch
Patch4:		%{name}-am.patch
Patch5:		%{name}-pc.patch
Patch6:		%{name}-includes.patch
URL:		https://gmerlin.sourceforge.net/
BuildRequires:	OpenGL-devel
BuildRequires:	alsa-lib-devel >= 1.0.0
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
%{?with_esd:BuildRequires:	esound-devel >= 0.2.19}
BuildRequires:	fontconfig-devel >= 2.2.3
# pkgconfig(freetype2) >= 9.7.3
BuildRequires:	freetype-devel >= 1:2.1.9
BuildRequires:	gavl-devel >= 1.4.0
BuildRequires:	gettext-tools
# inotify interface
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	jack-audio-connection-kit-devel >= 0.109.2
BuildRequires:	libcddb-devel >= 1.0.2
BuildRequires:	libcdio-devel >= 0.76
BuildRequires:	libcdio-paranoia-devel
BuildRequires:	libexif-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmusicbrainz-devel >= 2.0.2
BuildRequires:	libpng-devel
BuildRequires:	libquicktime-devel >= 1.2.4
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libv4l-devel >= 0.5.7
BuildRequires:	libvisual-devel >= 0.4.0
BuildRequires:	libxml2-devel >= 2.4.0
BuildRequires:	pkgconfig
BuildRequires:	pulseaudio-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	sed >= 4.0
%{?with_nmjedit:BuildRequires:	sqlite3-devel}
BuildRequires:	texinfo
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXtst-devel
BuildRequires:	xorg-lib-libXv-devel
BuildRequires:	xorg-lib-libX11-devel >= 1.0.0
Requires:	fontconfig-libs >= 2.2.3
Requires:	freetype >= 1:2.1.9
Requires:	gavl >= 1.4.0
Requires:	gtk+2 >= 2:2.8.0
Requires:	libcddb >= 1.0.2
Requires:	libcdio >= 0.76
Requires:	libmusicbrainz >= 2.0.2
Requires:	libquicktime >= 1.2.4
Requires:	libv4l >= 0.5.7
Requires:	libvisual >= 0.4.0
Requires:	libxml2 >= 2.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gmerlin is a set of multimedia libraries bundled with an application
suite.

This package contains the core libraries, some plugins and most
applications.

%description -l pl.UTF-8
Gmerlin to zbiór bibliotek multimedialnych wraz z aplikacjami.

Ten pakiet zawiera główne biblioteki, trochę wtyczek i więszkość
aplikacji.

%package devel
Summary:	Header files for gmerlin libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek gmerlin
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	OpenGL-devel
Requires:	fontconfig-devel >= 2.2.3
Requires:	freetype-devel >= 1:2.1.9
Requires:	gavl-devel >= 1.4.0
Requires:	gtk+2-devel >= 2:2.8.0
Requires:	libvisual-devel >= 0.4.0
Requires:	libxml2-devel >= 2.4.0
Requires:	xorg-lib-libXfixes-devel
Requires:	xorg-lib-libXinerama-devel
Requires:	xorg-lib-libXtst-devel
Requires:	xorg-lib-libXv-devel

%description devel
Header files for gmerlin libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek gmerlin.

%package static
Summary:	Static gmerlin libraries
Summary(pl.UTF-8):	Statyczne biblioteki gmerlin
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static gmerlin libraries.

%description static -l pl.UTF-8
Statyczne biblioteki gmerlin.

%package apidocs
Summary:	API documentation for gmerlin libraries
Summary(pl.UTF-8):	Dokumentacja API bibliotek gmerlin
Group:		Documentation
Conflicts:	gmerlin-devel < 1.2.0-15
BuildArch:	noarch

%description apidocs
API documentation for gmerlin libraries.

%description apidocs -l pl.UTF-8
Dokumentacja API bibliotek gmerlin.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1

# evil, sets CFLAGS basing on /proc/cpuinfo, overrides our optflags
# (--with-cpuflags=none disables using /proc/cpuinfo, but not overriding)
sed -i -e '19,$d;18aAC_DEFUN([LQT_OPT_CFLAGS],[OPT_CFLAGS="$CFLAGS"])' m4/lqt_opt_cflags.m4

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_esd:--disable-esd} \
	%{!?with_v4l1:--disable-v4l} \
	%{?with_nmjedit:--enable-nmjedit} \
	%{?with_static_libs:--enable-static} \
	--with-cpuflags=none
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

# dlopened plugins
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gmerlin/plugins/*.{la,a}
# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgmerlin*.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/sbin/ldconfig
-/usr/sbin/fix-info-dir -c %{_infodir}

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%if %{with v4l1}
%attr(755,root,root) %{_bindir}/camelot
%endif
%attr(755,root,root) %{_bindir}/album2m3u
%attr(755,root,root) %{_bindir}/album2pls
%attr(755,root,root) %{_bindir}/gmerlin
%if %{with nmjedit}
%attr(755,root,root) %{_bindir}/gmerlin-nmjedit
%endif
%attr(755,root,root) %{_bindir}/gmerlin-record
%attr(755,root,root) %{_bindir}/gmerlin-video-thumbnailer
%attr(755,root,root) %{_bindir}/gmerlin_alsamixer
%attr(755,root,root) %{_bindir}/gmerlin_imgconvert
%attr(755,root,root) %{_bindir}/gmerlin_imgdiff
%attr(755,root,root) %{_bindir}/gmerlin_kbd
%attr(755,root,root) %{_bindir}/gmerlin_kbd_config
%attr(755,root,root) %{_bindir}/gmerlin_launcher
%attr(755,root,root) %{_bindir}/gmerlin_play
%attr(755,root,root) %{_bindir}/gmerlin_plugincfg
%attr(755,root,root) %{_bindir}/gmerlin_psnr
%attr(755,root,root) %{_bindir}/gmerlin_recorder
%attr(755,root,root) %{_bindir}/gmerlin_remote
%attr(755,root,root) %{_bindir}/gmerlin_ssim
%attr(755,root,root) %{_bindir}/gmerlin_transcoder
%attr(755,root,root) %{_bindir}/gmerlin_transcoder_remote
%attr(755,root,root) %{_bindir}/gmerlin_vanalyze
%attr(755,root,root) %{_bindir}/gmerlin_visualize
%attr(755,root,root) %{_bindir}/gmerlin_visualizer
%attr(755,root,root) %{_bindir}/gmerlin_visualizer_slave
%attr(755,root,root) %{_bindir}/gmerlin_vpsnr
%{_libdir}/libgmerlin.so.*.*.*
%ghost %{_libdir}/libgmerlin.so.0
%{_libdir}/libgmerlin_gtk.so.*.*.*
%ghost %{_libdir}/libgmerlin_gtk.so.0
%dir %{_libdir}/gmerlin
%dir %{_libdir}/gmerlin/plugins
# R: libquicktime
%{_libdir}/gmerlin/plugins/e_lqt.so
%{_libdir}/gmerlin/plugins/e_pp_cdrdao.so
%{_libdir}/gmerlin/plugins/e_pp_vcdimager.so
# R: libpng
%{_libdir}/gmerlin/plugins/e_spumux.so
%{_libdir}/gmerlin/plugins/e_subtext.so
%{_libdir}/gmerlin/plugins/e_wav.so
%{_libdir}/gmerlin/plugins/fa_sampleformat.so
%{_libdir}/gmerlin/plugins/fa_volume.so
%{_libdir}/gmerlin/plugins/fv_bitshift.so
%{_libdir}/gmerlin/plugins/fv_blur.so
%{_libdir}/gmerlin/plugins/fv_colorbalance.so
%{_libdir}/gmerlin/plugins/fv_colormatrix_rgb.so
%{_libdir}/gmerlin/plugins/fv_colormatrix_yuv.so
%{_libdir}/gmerlin/plugins/fv_cropscale.so
%{_libdir}/gmerlin/plugins/fv_decimate.so
%{_libdir}/gmerlin/plugins/fv_deinterlace.so
%{_libdir}/gmerlin/plugins/fv_equalizer.so
%{_libdir}/gmerlin/plugins/fv_flip.so
%{_libdir}/gmerlin/plugins/fv_framerate.so
%{_libdir}/gmerlin/plugins/fv_interlace.so
%{_libdir}/gmerlin/plugins/fv_invert_rgb.so
%{_libdir}/gmerlin/plugins/fv_oldcolor.so
%{_libdir}/gmerlin/plugins/fv_pixelformat.so
%{_libdir}/gmerlin/plugins/fv_swapfields.so
%{_libdir}/gmerlin/plugins/fv_tcdisplay.so
%{_libdir}/gmerlin/plugins/fv_tctweak.so
%{_libdir}/gmerlin/plugins/fv_textlogo.so
%{_libdir}/gmerlin/plugins/fv_tlp.so
%{_libdir}/gmerlin/plugins/fv_transform.so
%{_libdir}/gmerlin/plugins/fv_zoom.so
# R: alsa-lib
%{_libdir}/gmerlin/plugins/i_alsa.so
# R: libcdio, libcdio-paranoia
%{_libdir}/gmerlin/plugins/i_cdaudio.so
%{_libdir}/gmerlin/plugins/i_edl.so
%if %{with esd}
# R: esound-libs
%{_libdir}/gmerlin/plugins/i_esd.so
%endif
# R: jack-audio-connection-kit-libs
%{_libdir}/gmerlin/plugins/i_jack.so
# R: libquicktime
%{_libdir}/gmerlin/plugins/i_lqt.so
%{_libdir}/gmerlin/plugins/i_mikmod.so
%{_libdir}/gmerlin/plugins/i_oss.so
# R: pulseaudio-libs
%{_libdir}/gmerlin/plugins/i_pulse.so
%if %{with v4l1}
%{_libdir}/gmerlin/plugins/i_v4l.so
%endif
# R: libv4l
%{_libdir}/gmerlin/plugins/i_v4l2.so
# R: libXinerama libXv
%{_libdir}/gmerlin/plugins/i_x11.so
%{_libdir}/gmerlin/plugins/ir_bmp.so
%{_libdir}/gmerlin/plugins/ir_gavl.so
# R: libjpeg
%{_libdir}/gmerlin/plugins/ir_jpeg.so
# R: libpng
%{_libdir}/gmerlin/plugins/ir_png.so
%{_libdir}/gmerlin/plugins/ir_pnm.so
%{_libdir}/gmerlin/plugins/ir_tga.so
# R: libtiff
%{_libdir}/gmerlin/plugins/ir_tiff.so
%{_libdir}/gmerlin/plugins/iw_bmp.so
%{_libdir}/gmerlin/plugins/iw_gavl.so
# R: libjpeg
%{_libdir}/gmerlin/plugins/iw_jpeg.so
# R: libpng
%{_libdir}/gmerlin/plugins/iw_png.so
%{_libdir}/gmerlin/plugins/iw_pnm.so
%{_libdir}/gmerlin/plugins/iw_tga.so
# R: libtiff
%{_libdir}/gmerlin/plugins/iw_tiff.so
# R: alsa-lib
%{_libdir}/gmerlin/plugins/oa_alsa.so
%if %{with esd}
# R: esound-libs
%{_libdir}/gmerlin/plugins/oa_esd.so
%endif
# R: jack-audio-connection-kit-libs
%{_libdir}/gmerlin/plugins/oa_jack.so
%{_libdir}/gmerlin/plugins/oa_oss.so
# R: pulseaudio-libs
%{_libdir}/gmerlin/plugins/oa_pulse.so
# R: libv4l
%{_libdir}/gmerlin/plugins/ov_v4l2.so
# R: libXinerama libXv
%{_libdir}/gmerlin/plugins/ov_x11.so
%{_libdir}/gmerlin/plugins/vis_scope.so
%{_datadir}/gmerlin
%doc %dir %{_docdir}/gmerlin
%doc %{_docdir}/gmerlin/img
%doc %{_docdir}/gmerlin/userguide
%{_infodir}/gmerlin.info*
%{_mandir}/man1/gmerlin.1*
%{_mandir}/man1/gmerlin-record.1*
%{_mandir}/man1/gmerlin_play.1*
%{_mandir}/man1/gmerlin_remote.1*
%{_mandir}/man1/gmerlin_transcoder.1*
%{_mandir}/man1/gmerlin_transcoder_remote.1*
%{_desktopdir}/gmerlin-alsamixer.desktop
%{_desktopdir}/gmerlin-kbd.desktop
%{_desktopdir}/gmerlin-player.desktop
%{_desktopdir}/gmerlin-plugincfg.desktop
%{_desktopdir}/gmerlin-recorder.desktop
%{_desktopdir}/gmerlin-transcoder.desktop
%{_desktopdir}/gmerlin-visualizer.desktop
%{_iconsdir}/hicolor/48x48/apps/gmerlin-alsamixer.png
%{_iconsdir}/hicolor/48x48/apps/gmerlin-camelot.png
%{_iconsdir}/hicolor/48x48/apps/gmerlin-kbd.png
%{_iconsdir}/hicolor/48x48/apps/gmerlin-player.png
%{_iconsdir}/hicolor/48x48/apps/gmerlin-plugincfg.png
%{_iconsdir}/hicolor/48x48/apps/gmerlin-recorder.png
%{_iconsdir}/hicolor/48x48/apps/gmerlin-transcoder.png
%{_iconsdir}/hicolor/48x48/apps/gmerlin-visualizer.png

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgmerlin.so
%{_libdir}/libgmerlin_gtk.so
%{_includedir}/gmerlin
%{_pkgconfigdir}/gmerlin.pc
%{_pkgconfigdir}/gmerlin-gtk.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgmerlin.a
%{_libdir}/libgmerlin_gtk.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_docdir}/gmerlin/apiref
