%define	mesaversion	3.2.1
%define glx_ver	latest

Summary:	OpenGL 1.2 compatible 3D graphics library
Summary(pl):	Bilioteka grfiki 3D kompatybilna z OpenGL 1.2
Name:		XFree86-glx
Version:	4.2.0
Release:	0.2
License:	LGPL
Vendor:		Brian Paul <brian_paul@mesa3d.org>
Group:		X11/Libraries
Source0:	ftp://ftp.mesa3d.org/pub/sourceforge/mesa3d/MesaLib-%{mesaversion}.tar.bz2
Source1:	ftp://ftp.mesa3d.org/pub/sourceforge/mesa3d/MesaDemos-%{mesaversion}.tar.bz2
Source2:	http://snow.ashlu.bc.ca/glx/snapshots/utah-glx-src-%{glx_ver}.tar.gz
URL:		http://www.mesa3d.org/
BuildRequires:	binutils >= 2.9.1.0.19a
BuildRequires:	tcl
Conflicts:	XFree86 =< 4.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	OpenGL
Obsoletes:	Mesa
Obsoletes:	XFree86-OpenGL-core
Obsoletes:	XFree86-OpenGL-libs

%define		_prefix		/usr/X11R6
%define		_sysconfdir	/etc/X11

%description
This is an implementation of the Mesa 3D library and GLX with support
for hardware acceleration. GLX was developed by SGI as an extension to
the X window system to integrate OpenGL rendering functions. This
allows the Mesa 3D library to perform its 3D rendering functions
within the X server's process, rather than within the X client
program. This offers potential performance benefits, because the
rendered image does not have to be moved from the X client program to
the X server. (Only the commands required to render the image are
sent.) It also makes 3-D hardware acceleration much more practical
(and fast). This package includes a accelerated hardware drivers for
video card based on NVIDIA Riva series and ATI Rage Pro chipsets.

The Mesa 3D graphics library is a powerful and generic toolset for
creating hardware assisted computer graphics. To the extent that Mesa
utilizes the OpenGL command syntax or state machine, it is being used
with authorization from Silicon Graphics, Inc. However, the author
(Brian Paul) makes no claim that Mesa is in any way a compatible
replacement for OpenGL or associated with Silicon Graphics, Inc. Those
who want a licensed implementation of OpenGL should contact a licensed
vendor. However, Mesa is very similar to OpenGL, and you might find
Mesa to be a valid alternative to OpenGL.

This package is based on Mesa %{mesaver} and utah glx-%{glxver}.

please see http://utah-glx.sourceforge.net/ for more information.

%package	devel
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Summary(pl):	Pliki i biblioteki nag³ówkowe dla Mesy (biblioteka 3D OpenGL)
Group:		X11/Development/Libraries
Requires:	%{name}
Provides:	OpenGL-devel
Obsoletes:	Mesa-devel
Obsoletes:	XFree86-OpenGL-devel

%description devel
Mesa is an OpenGL 1.2 compatible 3D graphics library. Headers needed
to compile Mesa programs.

%prep
%setup -q -n Mesa-%{mesaversion} -b1 -a2
[ -d glx-xf4 ] && ln -s glx-xf4 glx;

RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS| sed 's/-m486 *//g'`; export RPM_OPT_FLAGS;

perl -p -i -e "s/-O3/$RPM_OPT_FLAGS/" Make-config

%build
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS| sed 's/-m486 *//g'`; export RPM_OPT_FLAGS;
%ifarch i386 i486
CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" \
./configure	--prefix=%{_prefix} \
		--sysconfdir=%{_sysconfdir} \
		--disable-mmx \
		--disable-3dnow \
		--without-ggi \
		--enable-mga=no \
		--enable-mach64=no \
		--enable-tnt=yes \
		--enable-i810=no \
		--enable-s3virge=no \
		--enable-s3savage=no \
		--enable-sis6326=no

%endif
%ifarch i586 i686 k6 k7
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" \
./configure	--prefix=%{_prefix} \
		--sysconfdir=%{_sysconfdir} \
		--with-glide=/usr \
		--without-ggi \
		--enable-mga=no \
		--enable-mach64=no \
		--enable-tnt=yes \
		--enable-i810=no \
		--enable-s3virge=no \
		--enable-s3savage=no \
		--enable-sis6326=no
%endif
%ifnarch i386 i486 i586 i686 k6 k7
./configure	--prefix=%{_prefix} \
		--sysconfdir=%{_sysconfdir} \
		--disable-3dnow \
		--without-ggi \
		--enable-mga=no \
		--enable-mach64=no \
		--enable-tnt=yes \
		--enable-i810=no \
		--enable-s3virge=no \
		--enable-s3savage=no \
		--enable-sis6326=no
%endif

%{__make}

%ifarch alpha sparc sparc64 ppc # Skip utah_glx for alpha - (fg) also skip it for
                                # sparc - (jb) also added skip for ppc
	echo 'utah_glx skipped for alpha, powerpc and sparcs'
%else
cd glx
cp -fv ../config.sub ./

CFLAGS="$RPM_OPT_FLAGS" \
	./autogen.sh	--with-chipset=both \
			--with-mesa=../ \
			--enable-extra \
			--disable-mtrr \
			--disable-agp \
			--disable-glut \
			--disable-GLU \
			--prefix=%{_prefix} \
			--sysconfdir=%{_sysconfdir} \
			--without-x86-asm \
			--without-mmx-asm \
			--without-3dnow-asm \
			--enable-mga=no \
			--enable-mach64=no \
			--enable-tnt=yes \
			--enable-i810=no \
			--enable-s3virge=no \
			--enable-s3savage=no \
			--enable-sis6326=no

# Arg docs sux ((Dadou) "are not OK", it's better ;)
cd docs
cat <<EOF > config.cache
ac_cv_path_install=${ac_cv_path_install='/usr/bin/install -c'}
ac_cv_prog_CP=${ac_cv_prog_CP='cp -f'}
ac_cv_prog_LN_S=${ac_cv_prog_LN_S='ln -s'}
ac_cv_prog_MKDIR=${ac_cv_prog_MKDIR='mkdir -p'}
ac_cv_prog_MV=${ac_cv_prog_MV='mv -f'}
ac_cv_prog_RM=${ac_cv_prog_RM='rm -f'}
ac_cv_prog_have_dvips=${ac_cv_prog_have_dvips=no}
ac_cv_prog_have_jade=${ac_cv_prog_have_jade=no}
ac_cv_prog_have_jadetex=${ac_cv_prog_have_jadetex=no}
ac_cv_prog_have_lynx=${ac_cv_prog_have_lynx=no}
ac_cv_prog_have_ps2pdf=${ac_cv_prog_have_ps2pdf=no}
ac_cv_prog_make_make_set=${ac_cv_prog_make_make_set=yes}
EOF

./configure	--enable-text \
		--enable-html \
		--enable-ps \
		--enable-pdf
cd ..

%{__make}
cd ..
%endif # Skip glx for Alpha

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/GL,%{_sysconfdir},/usr/bin}
install -d $RPM_BUILD_ROOT%{_libdir}/modules

%{__make} DESTDIR=$RPM_BUILD_ROOT install
cp include/GL/svgamesa.h $RPM_BUILD_ROOT%{_includedir}/GL/
cp glx/servGL/libglx.so $RPM_BUILD_ROOT%{_libdir}/modules/

%ifarch alpha sparc sparc64 ppc
echo 'Skipping utah_glx'
%else
cat > $RPM_BUILD_ROOT/usr/bin/glx <<EOF
#!/bin/sh
LD_PRELOAD=%{_prefix}/lib/libGL.so.1.0 "\$@"
EOF

## glx
cd glx
%{__make} DESTDIR=$RPM_BUILD_ROOT sysconfdir=%{_sysconfdir} install
cd ..
%endif # glx

cd $RPM_BUILD_ROOT/%{_prefix}/lib/
ln -sf libGL.so.1 libGL.so
ln -sf libGLU.so.1 libGLU.so
ln -sf libGLU.so.1 libGLU.so.3
ln -sf libglut.so.3 libglut.so

# (gc) add Mesa symlinks for compatibility
ln -sf libGL.so libMesaGL.so
ln -sf libGL.so.1 libMesaGL.so.1
ln -sf libGL.so.1.0 libMesaGL.so.1.0
ln -sf libGLU.so libMesaGLU.so
ln -sf libGLU.so.1 libMesaGLU.so.1

%clean
[ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{COPYRIGHT,README*,COPYING,DEVINFO,CONFORM,VERSIONS} glx/docs/README.*
%attr(755,root,root) /usr/bin/glx
%{_libdir}/*.so.*
%config %{_sysconfdir}/mesa.conf
%ifarch i386 i486 i586 i686 k6 k7
%{_prefix}/lib/modules/extensions/*.so
#%{_prefix}/lib/modules/extensions/*.so
%config %{_sysconfdir}/glx.conf
%endif

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/GL
%{_includedir}/GL/gl*.h
%{_includedir}/GL/o*.h
%{_includedir}/GL/x*.h
%ifarch i386 i486 i586 i686 k6 k7
%{_includedir}/GL/svgamesa.h
%endif
%{_prefix}/lib/lib*.so
%{_prefix}/lib/lib*.la
