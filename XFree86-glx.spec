%define	mesaversion	3.2.1
%define glx_ver	latest

Summary:	OpenGL 1.2 compatible 3D graphics library
Summary(pl):	Biblioteka grafiki 3D kompatybilna z OpenGL 1.2
Name:		XFree86-glx
Version:	4.2.0
Release:	0.2
License:	LGPL
Vendor:		Brian Paul <brian_paul@mesa3d.org>
Group:		X11/Libraries
Source0:	http://dl.sf.net/mesa3d/MesaLib-%{mesaversion}.tar.bz2
# Source0-md5:	dcd5a6aa77b3bdb400c8179419473e58
Source1:	http://dl.sf.net/mesa3d/MesaDemos-%{mesaversion}.tar.bz2
# Source1-md5:	621bd95ed9f93467f4dfa615e2f27c16
Source2:	http://snow.ashlu.bc.ca/glx/snapshots/utah-glx-src-%{glx_ver}.tar.gz
# Source2-md5:	654ae59e0603d71c18a88737e9f954c6
URL:		http://www.mesa3d.org/
BuildRequires:	binutils >= 2.9.1.0.19a
BuildRequires:	tcl
Provides:	OpenGL
Conflicts:	XFree86 =< 4.1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
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

This package is based on Mesa %{mesaver} and utah-glx-%{glxver}.

please see http://utah-glx.sourceforge.net/ for more information.

%description -l pl
To jest implementacja biblioteki Mesa 3D oraz GLX z obs³ug± sprzêtowej
akceleracji. GLX zosta³ stworzony przez SGI jako rozszerzenie systemu
X Window w celu integracji funkcji renderuj±cych OpenGL. Pozwala to
bibliotece Mesa 3D na wykonywanie funkcji renderujacych 3D wewn±trz
procesu X serwera zamiast po stronie X klienta. Daje to potencjalne
zyski wydajno¶ci, poniewa¿ wyrenderowany obraz nie musi byæ przesy³any
z programu X klienta do X serwera (przesy³ane s± tylko polecenia
potrzebne do renderowania). Daje to tak¿e mo¿liwo¶æ u¿ycia sprzêtowej
akceleracji 3D. Ten pakiet zawiera sterowniki wykorzystuj±ce
akceleracjê dla kart graficznych opartych na uk³adach z serii NVIDIA
Riva i ATI Rage Pro.

Biblioteka graficzna Mesa 3D jest potê¿nym i ogólnym zestawem narzêdzi
do tworzenia grafiki komputerowej przy wsparciu sprzêtu. Mesa u¿ywa
sk³adni poleceñ i maszyny stanów OpenGL za zgod± Silicon Graphics,
Inc. Nie jest to jednak licencjonowana implementacja OpenGL.

Ten pakiet bazuje na Mesie %{mesaver} oraz utah-glx-%{glxver}.

Wiêcej informacji na stronie http://utah-glx.sourceforge.net/.

%package devel
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Summary(pl):	Pliki nag³ówkowe dla Mesy (biblioteki 3D zgodnej z OpenGL)
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}
Provides:	OpenGL-devel
Obsoletes:	Mesa-devel
Obsoletes:	XFree86-OpenGL-devel

%description devel
Mesa is an OpenGL 1.2 compatible 3D graphics library. This package
contains the header files needed to compile Mesa programs.

%description devel -l pl
Mesa jest bibliotek± 3D zgodn± z OpenGL 1.2. Ten pakiet zawiera pliki
nag³ówkowe potrzebne do kompilowania programów u¿ywaj±cych Mesy.

%prep
%setup -q -n Mesa-%{mesaversion} -b1 -a2
[ -d glx-xf4 ] && ln -s glx-xf4 glx;

perl -pi -e "s/-O3/%{rpmcflags}/" Make-config

%build
RPM_OPT_FLAGS="%{rpmcflags}"; export RPM_OPT_FLAGS
%ifarch i386 i486
CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" \
./configure \
	--prefix=%{_prefix} \
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
%ifarch i586 i686 k6 athlon
CFLAGS="%{rpmcflags}" CXXFLAGS="%{rpmcflags}" \
./configure \
	--prefix=%{_prefix} \
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
%ifnarch %{ix86}
./configure \
	--prefix=%{_prefix} \
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
cp -fv ../config.sub .

CFLAGS="%{rpmcflags}" \
./autogen.sh \
	--with-chipset=both \
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

./configure \
	--enable-text \
	--enable-html \
	--enable-ps \
	--enable-pdf
cd ..

%{__make}
cd ..
%endif # Skip glx for Alpha

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir}/GL,%{_sysconfdir},/usr/bin} \
	$RPM_BUILD_ROOT%{_libdir}/modules

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install include/GL/svgamesa.h $RPM_BUILD_ROOT%{_includedir}/GL
install glx/servGL/libglx.so $RPM_BUILD_ROOT%{_libdir}/modules

%ifarch alpha sparc sparc64 ppc
echo 'Skipping utah_glx'
%else
cat > $RPM_BUILD_ROOT/usr/bin/glx <<EOF
#!/bin/sh
LD_PRELOAD=%{_prefix}/lib/libGL.so.1.0 "\$@"
EOF

## glx
cd glx
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	sysconfdir=%{_sysconfdir}
cd ..
%endif # glx

cd $RPM_BUILD_ROOT%{_prefix}/lib
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
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc docs/{COPYRIGHT,README*,DEVINFO,CONFORM,VERSIONS} glx/docs/README.*
%attr(755,root,root) /usr/bin/glx
%{_libdir}/*.so.*
%config %{_sysconfdir}/mesa.conf
%ifarch %{ix86}
%{_prefix}/lib/modules/extensions/*.so
%config %{_sysconfdir}/glx.conf
%endif

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/GL
%{_includedir}/GL/gl*.h
%{_includedir}/GL/o*.h
%{_includedir}/GL/x*.h
%ifarch %{ix86}
%{_includedir}/GL/svgamesa.h
%endif
%{_prefix}/lib/lib*.so
%{_prefix}/lib/lib*.la
