Summary:	Graphical client for PostgreSQL
Name:		pgadmin3
Version:	1.8.4
Release:	5%{?dist}
License:	Artistic
Group:		Applications/Databases
URL:		http://www.pgadmin.org/
Source:		ftp://ftp.postgresql.org/pub/%{name}/release/v%{version}/src/%{name}-%{version}.tar.gz
Patch0:		pgadmin3-1.8.4-optflags.patch
Requires:	wxGTK
BuildRequires:	wxGTK-devel, postgresql-devel, desktop-file-utils, openssl-devel, libxslt-devel
Obsoletes:	pgadmin3-docs <= 1.8.4-4
Provides:	pgadmin3-docs <= 1.8.4-4
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
pgAdmin III is a powerful administration and development
platform for the PostgreSQL database, free for any use. It
is designed to answer the needs of all users, from writing
simple SQL queries to developing complex databases. The
graphical interface supports all PostgreSQL features and
makes administration easy.

The application also includes a syntax highlighting SQL
editor, a server-side code editor, a SQL/batch/shell job
scheduling agent, support for the Slony-I replication
engine and much more. No additional drivers are required
to communicate with the database server.

%prep
%setup -q
# Touch to avoid autotools re-run
for f in configure{,.ac}; do touch -r $f $f.stamp; done
%patch0 -p1
for f in configure{,.ac}; do touch -r $f.stamp $f; done

%build
export LIBS="-lwx_gtk2u_core-2.8"
%configure --disable-debug --disable-dependency-tracking --with-wx-version=2.8 --with-wx=%{_prefix}
make %{?_smp_mflags} all

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install

install -p -m 644 pkg/debian/pgadmin3.xpm $RPM_BUILD_ROOT%{_datadir}/%{name}/%{name}.xpm

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications

desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications \
%if 0%{?rhel}
        --vendor="" \
%endif
        --add-category Development pkg/%{name}.desktop

# Convert changelog, fix incorrect end-of-line encoding
iconv -f iso-8859-1 -t utf-8 -o CHANGELOG.utf8 CHANGELOG
sed -i 's/\r$//' CHANGELOG.utf8
touch -c -r CHANGELOG CHANGELOG.utf8
mv -f CHANGELOG.utf8 CHANGELOG

# Fix incorrect end-of-line encoding
for file in docs/*/tips.txt; do
  cp -p $file $file.old; sed -i 's/\r$//' $file
  touch -c -r $file.old $file; rm -f $file.old
done

# Remove unwanted and double files
rm -f docs/{Docs.vcproj,builddocs.bat,en_US/pgadmin3.hhp.cached}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/{branding,docs}
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/i18n/{*,.}/wxstd.mo

# Correct permissions to solve rpmlint debuginfo noise
chmod 644 pgadmin/include/images/{package,synonym}{,s}.xpm

# Move locales to their correct place
mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale
mv -f $RPM_BUILD_ROOT%{_datadir}/%{name}/i18n/??_?? $RPM_BUILD_ROOT%{_datadir}/locale

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc BUGS CHANGELOG LICENSE README docs/*
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*

%changelog
* Mon Jan 05 2009 Robert Scheck <robert@fedoraproject.org> 1.8.4-5
- Removed useless -docs package, main package shipped it anyway
- Many spec file and package cleanups to get rpmlint very silent

* Sun Jan 04 2009 Robert Scheck <robert@fedoraproject.org> 1.8.4-4
- Moving from Fedora to RPM Fusion (#300, RHBZ #473748)

* Wed Dec 31 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.4-3
- Rebuilt for Fedora 10

* Mon Jul 14 2008 Ville Skyttä <ville.skytta at iki.fi> - 1.8.4-2
- Use $RPM_OPT_FLAGS, build with dependency tracking disabled (#229054).

* Wed Jun 4 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.4-1
- Update to 1.8.4

* Tue Jun 3 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.3-1
- Update to 1.8.3

* Fri Feb 1 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.2-1
- Update to 1.8.2

* Fri Jan 4 2008 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.1-1
- Update to 1.8.1

* Wed Dec 05 2007 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.0-2
- Rebuild for openssl bump

* Wed Nov 14 2007 Devrim GUNDUZ <devrim@commandprompt.com> 1.8.0-1
- Update to 1.8.0
- Fix requires and buildrequires
- Improve description
- Added -docs subpackage
- add 2 new configure options, per upstream
- Fix path for xpm file

* Wed Apr 04 2007 Warren Togami <wtogami@redhat.com> - 1.6.3-1
- 1.6.3

* Thu Dec 28 2006 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.6.1-2
- A couple of minor fixes to get things building in rawhide.

* Tue Dec 05 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.6.1-1
- Update for 1.6.1. Now needs wxGTK 2.7+

* Mon Oct 09 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-6
- Rebuild for FC6

* Tue Aug 29 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-5
- Should have Developement and keeping this version one ahead for
  upgrading in FC-6

* Mon Aug 28 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-3
- Moved icon to Devel and updated for FC-6

* Sat Jul 30 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-2
- Removed gcc41 patch

* Sat Jul 29 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.3-1
- Updated to latest 
- Sorry for delay

* Wed Feb 16 2006 Gavin Henry <ghenry@suretecsystems.com> - 1.4.1-2
- Applied Dennis' fixes according to Bug #181632

* Wed Feb 15 2006 Dennis Gilmore <dennis@ausil.us> - 1.4.1-1
- update to 1.4.1

* Thu Dec 8 2005 Gavin Henry <ghenry@suretecsystems.com> - 1.4.0-2
- Removed specific lib includes, not needed anymore 

* Wed Dec 7 2005 Gavin Henry <ghenry@suretecsystems.com> - 1.4.0-1
- Updated to latest release

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 1.0.2-5
- rebuild on all arches

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Thu Oct 07 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.3
- include LICENCE.txt BUGS.txt README.txt
- Use master location in Source
- Don't --delete-original .desktop file.

* Thu Oct 07 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.2
- Don't own _datadir/applications/
- Fedora -> fedora for .desktop file
- Use _smp_mflags for make

* Wed Oct 06 2004 Nils O. Selåsdal <NOS|at|Utel.no> - 0:1.0.2-0.fdr.1
- Initial RPM
